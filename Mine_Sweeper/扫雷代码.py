import sys
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import QtCore

import random

_SPACE_ = ''
_FLAG_ = '.\pic\\flag.png'
_MINE_ = '.\pic\\bomb-1.png'
_WindowIcon_ = '.\pic\\Window_Icon'
_COVER_= '.\pic\\cover.png'
_Boom_ = '.\pic\\Boom.png'

Win_H = 417
Win_W = 417


_COLUMN_EASY = 10
_ROW_EASY = 10
_NUM_MINE_EASY = 10

_COLUMN_NORMAL = 15
_ROW_NORMAL = 15
_NUM_MINE_NORMAL = 20

_COLUMN_HARD = 20
_ROW_HARD = 20
_NUM_MINE_HARD = 30


class Main_Window(QWidget):
    #singleton: 'Main_Window' = None
    def __init__(self):
        super(Main_Window, self).__init__()
        self.Menu()


    def Menu(self):
        self.resize(Win_W,Win_H)
        self.setWindowTitle("MineSweeper")
        self.setWindowIcon(QIcon(_WindowIcon_))

        self.image = QPixmap(".\pic\\Banner.png")

        self.Banner = QLabel(self)
        self.Banner.setPixmap(self.image)

        self.Button_field = QLabel(self.Banner)
        self.Button_field.resize(Win_W,int(Win_H/2))
        self.Button_field.move(0,int(Win_H/2))

        self.button_easy = QPushButton(self.Button_field)
        self.button_easy.setText("Easy")
        self.button_easy.setFont(QFont("Arial, 30"))
        self.button_easy.setFixedSize(100,30)
        self.button_easy.clicked.connect(lambda:self.StartGame(_ROW_EASY,_COLUMN_EASY,_NUM_MINE_EASY))

        self.button_normal = QPushButton(self.Button_field)
        self.button_normal.setText("Normal")
        self.button_normal.setFont(QFont("Arial, 30"))
        self.button_normal.clicked.connect(lambda:self.StartGame(_ROW_NORMAL,_COLUMN_NORMAL,_NUM_MINE_NORMAL))
        self.button_normal.setFixedSize(100,30)

        self.button_hard = QPushButton(self.Button_field)
        self.button_hard.setText("Hard")
        self.button_hard.setFont(QFont("Arial, 30"))
        self.button_hard.clicked.connect(lambda:self.StartGame(_ROW_HARD,_COLUMN_HARD,_NUM_MINE_HARD))
        self.button_hard.setFixedSize(100,30)

        self.grid = QGridLayout(self.Button_field)
        self.grid.addWidget(self.button_easy,0,1)
        self.grid.addWidget(self.button_normal,1,1)
        self.grid.addWidget(self.button_hard,2,1)
        self.Button_field.setLayout(self.grid)

    def StartGame(self,row,col,num):
        self.Banner.close()
        self.Grid = [[0 for i in range(row)] for j in range(col)]
        self.Mine = [[0 for i in range(row)] for j in range(col)]
        self.Init(self.Grid,row,col)
        self.Init(self.Mine,row,col)
        self.SetMine(row,col,num)
        self.ShwoBoard(row,col,num)

    def PlayGame(self,button,row,col,num):
        button.setEnabled(False)
        x = self.GetPosition(button)[0]
        y = self.GetPosition(button)[1]
        if self.Mine[x][y] == _MINE_:
            button.setIcon(QIcon(_Boom_))
            self.ShowMine(x,y,row,col)
            self.Message("Mine Sweeper","Game Over")
        # num or space
        else:
            button.setIcon(QIcon(_SPACE_))
            self.Num(x,y,row,col)
            if self.Grid[x][y] == _SPACE_:
                self.Autoreveal(x,y,row,col)
        # win 
        if self.Win(row,col) == num:
            self.Message("Mine Sweeper","You Win!")

    def Init(self,list,row,col):
        for i in range(row):
            for j in range(col):
                list[i][j] = _COVER_
    
    def SetMine(self,row,col,num):
        count = 0
        while(count<num):
            x_mine = random.randint(0,row-1)
            y_mine = random.randint(0,col-1)
            if self.Mine[x_mine][y_mine] != _MINE_:
                self.Mine[x_mine][y_mine] = _MINE_
                count = count + 1

    def ShwoBoard(self,row,col,num):
        self.grid = QGridLayout(self)
        self.grid.setSpacing(1)
        self.setLayout(self.grid)
        for i in range(row):
            for j in range(col):
                self.button = QPushButton()
                self.button.setFixedSize(30,30)
                #self.button.setObjectName(str((i,j)))
                self.button.setIcon(QIcon(self.Grid[i][j]))
                btn = self.button
                self.button.clicked.connect(lambda play, button = btn: self.PlayGame(button,row,col,num))
                self.grid.addWidget(self.button,i,j)

    def GetPosition (self,button):
        btn_index = self.grid.indexOf(button)
        position = self.grid.getItemPosition(btn_index)
        
        return position

    def ShowMine(self,x,y,row,col):
        for i in range(row):
            for j in range(col):
                if i == x and j == y:
                    continue
                elif self.Mine[i][j] == _MINE_:
                    mine_button = self.grid.itemAtPosition(i,j).widget()
                    mine_button.setIcon(QIcon(_MINE_))


    def Num(self,x,y,row,col):
        count = 0
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                if i < 0 or i>row-1 or j < 0 or j > col-1:
                    continue
                else:
                    if self.Mine[i][j] == _MINE_:
                        count = count + 1
                num_button = self.grid.itemAtPosition(x,y).widget()
        if count == 0:
            num_button.setIcon(QIcon(_SPACE_))
            self.Grid[x][y] = _SPACE_
        else:
            num_button.setIcon(QIcon(_SPACE_))
            num_button.setText(str(count))
            self.Grid[x][y] = count

    def Autoreveal(self,x,y,row,col):
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                if i < 0 or i>row-1 or j < 0 or j > col-1:
                    continue
                elif self.Grid[i][j] == _SPACE_:
                    continue
                else:
                    self.Num(i,j,row,col)
                    if self.Grid[i][j] == _SPACE_:
                        self.Autoreveal(i,j,row,col)

    def Win(self,row,col):
            count = 0
            for i in range(row):
                for j in range(col):
                    if self.Grid[i][j] == _COVER_:
                        count = count + 1
            return count

    def Message(self,title,content):
        button = QMessageBox.question(self, str(title), str(content))

        if button == QMessageBox.StandardButton.Yes:
            self.restart()
        else:
            self.close()

    def restart(self):
        os.execl(sys.executable, sys.executable, *sys.argv)

def main():
    app = QApplication(sys.argv)
    Window = Main_Window()
    Window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
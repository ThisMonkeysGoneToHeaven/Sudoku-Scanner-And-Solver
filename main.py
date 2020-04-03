import sys
from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt5.QtGui import QIcon
import os
from sudoku import Board
from detection import Detection


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku")
        self.setWindowIcon(QIcon('favicon.png'))
        self.displayWidth = 300
        self.displayHeight = 400
        self.setGeometry(200, 200, self.displayWidth, self.displayHeight)
        self.setFixedSize(self.size())

        self.choose()

    def choose(self):
        self.manBtn = QPushButton("Enter Grid Manually", self)
        self.manBtn.move(self.displayWidth//2-70, self.displayHeight//2-60)
        self.manBtn.resize(150, 40)
        self.manBtn.clicked.connect(self.manualInput)

        self.fileBtn = QPushButton("Choose File", self)
        self.fileBtn.resize(150, 40)
        self.fileBtn.move(self.displayWidth//2-70, self.displayHeight//2)
        self.fileBtn.clicked.connect(self.fileInput)

    def manualInput(self):
        self.close()
        Board()

    def fileInput(self):
        global the_file
        the_chosen_image = QFileDialog.getOpenFileName(
            self, "Select File", "", "*.png *.jpg")
        the_file = the_chosen_image[0]
        Detection(the_file)
        for i in range(9):
        	for j in range(9):
        		Board.matrix[j][i] = Detection.board[i][j]
        self.close()
        Board()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(app.exec_())

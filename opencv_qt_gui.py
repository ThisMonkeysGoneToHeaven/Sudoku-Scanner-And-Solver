import numpy
import cv2
from PyQt5.QtGui import QImage, QKeyEvent, QPainter
from PyQt5.QtWidgets import QDialog, QApplication


class MyDialog(QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)

        self.cvImage = cv2.imread(r'image.jpg')
        self.cvImage = cv2.resize(self.cvImage, (400, 400))
        height, width, byteValue = self.cvImage.shape
        byteValue = byteValue * width

        self.setWindowTitle("Sudoku")
        self.displayWidth = 400
        self.displayHeight = 400
        self.setGeometry(200, 200, self.displayWidth, self.displayHeight)
        self.setFixedSize(self.size())

        cv2.cvtColor(self.cvImage, cv2.COLOR_BGR2RGB, self.cvImage)

        self.mQImage = QImage(self.cvImage, width, height,
                              byteValue, QImage.Format_RGB888)

    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        painter.drawImage(0, 0, self.mQImage)
        painter.end()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = MyDialog()
    w.resize(600, 400)
    w.show()
    app.exec_()

from GameLogics import Game
import colors as c
from Game_interface import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox



class MyWin(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.g = Game()
        self.rect = self.g.getLup()
        self.cell = self.g.get_select_cell()
        self.score = self.g.get_score()

        self.StartButton.clicked.connect(self.start)
        self.btn_info.clicked.connect(self.information)

    def keyPressEvent(self, event):
        dict = {
            QtCore.Qt.Key_W: self.up,
            QtCore.Qt.Key_S: self.down,
            QtCore.Qt.Key_A: self.left,
            QtCore.Qt.Key_D: self.right,
            QtCore.Qt.Key_F: self.update
        }
        try:
            dict[event.key()]()
        except:
            pass

    def show_matrix_in_table(self):
        self.cell = self.g.get_select_cell()
        for row in range(self.g.GameHeight):
            for col in range(self.g.GameWidth):
                item = self.g[row, col]
                cellinfo = QTableWidgetItem(' ')
                if item > 0:
                    cellinfo = QTableWidgetItem(str(item))

                # Только для чтения
                cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                cellinfo.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                cellinfo.setFont(QtGui.QFont('SansSerif', 60))
                self.tableWidget.setItem(row, col, cellinfo)
                color = c.my_color[item]
                self.tableWidget.item(row, col).setBackground(QtGui.QColor(color[0], color[1], color[2]))

                if row == self.rect[0] and col == self.rect[1]:
                    color_moving = c.my_color['moving']
                    self.tableWidget.item(row, col).setBackground(
                        QtGui.QColor(color_moving[0], color_moving[1], color_moving[2]))

                if len(self.cell) > 0:
                    a = self.cell[0]
                    if row == a[0] and col == a[1]:
                        color_moving = c.my_color['selected']
                        self.tableWidget.item(row, col).setBackground(
                            QtGui.QColor(color_moving[0], color_moving[1], color_moving[2]))


        self.score = self.g.get_score()
        self.labelScore.setText("Score: " + str(self.score))
        self.labelScore.setFont(QtGui.QFont('SansSerif', 16))


    def decor_update_view(func):
        def wrapped(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.show_matrix_in_table(*args, **kwargs)
        return wrapped

    # Описываем функции
    @decor_update_view
    def update(self):
        self.g.update()
        if self.g.check_end_game():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("You Win!")
            msg.setInformativeText("Score: " + str(self.score))
            msg.setWindowTitle("Game")
            msg.addButton('Новая игра', QMessageBox.AcceptRole)
            msg.exec()
            self.start()


    @decor_update_view
    def up(self):
        self.g.move_border('up')
        self.rect = self.g.getLup()


    @decor_update_view
    def down(self):
        self.g.move_border('down')
        self.rect = self.g.getLup()


    @decor_update_view
    def left(self):
        self.g.move_border('left')
        self.rect = self.g.getLup()


    @decor_update_view
    def right(self):
        self.g.move_border('right')
        self.rect = self.g.getLup()


    def start(self):
        self.g = Game()
        self.g.create_level()
        self.rect = self.g.getLup()
        self.show_matrix_in_table()


    def information(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Цель игры: (аналог 2048) собрать число 12.\n"
                    "Соединяясь, пара фишек с одинаковыми числами образуют одну с числом, на единицу большим, чем у соединяющихся.")
        msg.setInformativeText("Управление: (WASDF)\n"
                               "W, S, A, D - передвигаемся по сетке вверх/вниз/влево/вправо соответственно;\n"
                               "F - по первому нажатию выбираем фишку, по второму производим их соединение, если это возможно.")
        msg.setWindowTitle("Game")
        msg.addButton('Ok', QMessageBox.AcceptRole)
        msg.exec()

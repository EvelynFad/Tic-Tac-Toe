from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QMenu, QWidget, QLabel, QStatusBar
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QAction
from PyQt6 import uic
import numpy as np

# Д/З
# (1) Придумать и реализовать красивый интерфейс +
# (2) Подумать, что можно улучшить
# (3) Реализовать случай, когда ничья +
# (4) Сделать режим игры с ботом, где тот будет играть с вами
# (5) Оформить ВСЕ КОММЕНТАРИИ (ТЫ ИХ НЕ ЛЮБИШЬ) +
# (6) Выложи на GitHUB, пока без оформления...

# Класс окна
class Window(QMainWindow):

    # Магия для подсказок с функциями
    StatusBar: QStatusBar
    __Message = QLabel

    B_1: QPushButton
    B_2: QPushButton
    B_3: QPushButton
    B_4: QPushButton
    B_5: QPushButton
    B_6: QPushButton
    B_7: QPushButton
    B_8: QPushButton
    B_9: QPushButton

    M_Game: QMenu

    Field: QWidget

    # Конструктор
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi("window.ui", self)

        # Создание массива с игровым полем
        self.__field = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]])

        # Переменная для смены хода
        self.__move = True

        # Переменная свободного места
        self.__free = True

        # Добавление текста сообщения в строку состояния
        self.__Message = QLabel("The game has started....")
        self.StatusBar.addWidget(self.__Message)

        # Связка кнопок
        self.B_1.clicked.connect(self.__onClick_B1)
        self.B_2.clicked.connect(self.__onClick_B2)
        self.B_3.clicked.connect(self.__onClick_B3)
        self.B_4.clicked.connect(self.__onClick_B4)
        self.B_5.clicked.connect(self.__onClick_B5)
        self.B_6.clicked.connect(self.__onClick_B6)
        self.B_7.clicked.connect(self.__onClick_B7)
        self.B_8.clicked.connect(self.__onClick_B8)
        self.B_9.clicked.connect(self.__onClick_B9)

        # Связка меню
        self.M_Game.triggered.connect(self.__onClick_Menu)

    # Обработка нажатия меню
    def __onClick_Menu(self, action: QAction):
        # Конкретная кнопка, которую нажали в меню
        text = action.text()
        # Если этой кнопкой оказалась "Новая игра"
        if text == "New game":
            self.__clear()                  # Очищаем поле
            self.Field.setEnabled(True)     # Разблокируем поле
        # Если этой кнопкой оказалась "Выход"
        elif text == "Exit":
            self.close()                    # Закрываем окно

    # Очистка поля
    def __clear(self):
        # Удаление ноликов и крестиков
        self.B_1.setText("")
        self.B_2.setText("")
        self.B_3.setText("")
        self.B_4.setText("")
        self.B_5.setText("")
        self.B_6.setText("")
        self.B_7.setText("")
        self.B_8.setText("")
        self.B_9.setText("")

        # Очистка массива поля
        self.__field = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]])

        # Установка хода
        self.__move = True
        # Изменение текста на строке состояния
        QMessageBox.warning(None, "Game", "The game has started!")
        self.__Message.setText("The game has started!")

    # Обработка нажатия кнопки
    def __onClick_Button(self, button: QPushButton, index_x: int, index_y: int):
        # Если ход крестиков и эта кнопка свободна
        if self.__move and button.text() == "":
            button.setText("X")                         # Ставим крестик
            self.__field[index_x][index_y] = 1          # Меняем значение в массиве поля
            self.__move = not self.__move               # Меняем ход
        # Если ход ноликов и эта кнопка свободна
        elif not self.__move and button.text() == "":
            button.setText("O")                         # Ставим нолик
            self.__move = not self.__move               # Меняем ход
            self.__field[index_x][index_y] = 2          # Меняем значение в массиве поля

        # Проверка на выигрыш/проигрыш в одну строку
        for line in self.__field:
            # Если в одной строке 3 крестика подряд
            if list(line).count(1) == 3:
                QMessageBox.information(None, "Game", "Crosses has won!")
                self.__Message.setText("Crosses has won!")
                self.Field.setEnabled(False)
            # Если в одной строке 3 нолика подряд
            if list(line).count(2) == 3:
                self.__Message.setText("Zeros has won!")
                QMessageBox.information(None, "Game", "Zeros has won!")
                self.Field.setEnabled(False)

        for line in self.__field.transpose():
            # Если в одной строке 3 крестика подряд
            if list(line).count(1) == 3:
                QMessageBox.information(None, "Game", "Crosses has won!")
                self.__Message.setText("Crosses has won!")
                self.Field.setEnabled(False)
            # Если в одной строке 3 нолика подряд
            if list(line).count(2) == 3:
                self.__Message.setText("Zeros has won!")
                QMessageBox.information(None, "Game", "Zeros has won!")
                self.Field.setEnabled(False)

        # Проверка на выигрыш/проигрыш по диагонали
        Diag_1, Diag_2 = [], []
        # Добавляем в переменные значения диагоналей
        for id in range(3):
            Diag_1.append(self.__field[id][id])
            Diag_2.append(self.__field[id][2-id])

        # Проверка с помощью счёта нулей/крестиков
        if Diag_1.count(1) == 3:
            QMessageBox.information(None, "Game", "Crosses has won!")
            self.__Message.setText("Crosses has won!")
            self.Field.setEnabled(False)
        if Diag_2.count(1) == 3:
            self.__Message.setText("Crosses has won!")
            QMessageBox.information(None, "Game", "Crosses has won!")
            self.Field.setEnabled(False)
        if Diag_1.count(2) == 3:
            self.__Message.setText("Zeros has won!")
            QMessageBox.information(None, "Game", "Zeros has won!")
            self.Field.setEnabled(False)
        if Diag_2.count(2) == 3:
            self.__Message.setText("Zeros has won!")
            QMessageBox.information(None, "Game", "Zeros has won!")
            self.Field.setEnabled(False)

        # Проверка на ничью
        self.__free = False                 # Устанавливаем значение переменной
        # Перебор линий на поле
        for line in self.__field:
            # Если присутствует свободное место
            if 0 in line:
                self.__free = True          # Меняем значение переменной
        # Если после этого переменная осталась отрицательной
        if not self.__free:
            self.__Message.setText("It's a tie!")        # Меняем текст в строке состояния
            QMessageBox.information(None, "Game", "It's a tie!")
            self.Field.setEnabled(False)            # Блокируем поле

    # Обработка нажатия кнопок
    def __onClick_B1(self):
        self.__onClick_Button(self.B_1, 2, 0)

    def __onClick_B2(self):
        self.__onClick_Button(self.B_2, 2, 1)

    def __onClick_B3(self):
        self.__onClick_Button(self.B_3, 2, 2)

    def __onClick_B4(self):
        self.__onClick_Button(self.B_4, 1, 0)

    def __onClick_B5(self):
        self.__onClick_Button(self.B_5, 1, 1)

    def __onClick_B6(self):
        self.__onClick_Button(self.B_6, 1, 2)

    def __onClick_B7(self):
        self.__onClick_Button(self.B_7, 0, 0)

    def __onClick_B8(self):
        self.__onClick_Button(self.B_8, 0, 1)

    def __onClick_B9(self):
        self.__onClick_Button(self.B_9, 0, 2)

# Основная функция
def Main():
    # Запуск QT ядра
    app = QApplication([])
    # Окно
    window = Window()
    # Открытие окна
    window.show()
    # Запуск
    app.exec()


if __name__ == "__main__": Main()

from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QMenu, QWidget, QLabel, QStatusBar
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QAction
from PyQt6 import uic
import numpy as np
import random
import sys


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
    M_FAO: QMenu

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

        # включён ли бот
        self.__bot = True
        # бот играет ноликами
        self.__bot_symbol = 2

        # Список кнопок
        self.__buttons = [
            [self.B_7, self.B_8, self.B_9],
            [self.B_4, self.B_5, self.B_6],
            [self.B_1, self.B_2, self.B_3]
        ]

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
        self.M_FAO.triggered.connect(self.__onClick_Menu)

    # Обработка нажатия меню
    def __onClick_Menu(self, action: QAction):
        # Конкретная кнопка, которую нажали в меню
        text = action.text()
        # Если этой кнопкой оказалась "Новая игра"
        if text == "New game":
            self.__modeChoiceWindow()
        # Если этой кнопкой оказалась "Выход"
        elif text == "Exit":
            self.close() # Закрываем окно
        elif text == "Help": QMessageBox.about(self, "Help", "No one will help you")

    # Метод для бота
    def __botMove(self):
        # Поиск всех свободных мест
        free = []
        for i in range(3):
            for j in range(3):
                if self.__field[i][j] == 0:
                    free.append((i, j))

        # Если свободного места нет -> ничего не делать
        if len(free) == 0:
            return

        # Случайный выбор координат
        x, y = random.choice(free)

        # Кнопка, соответствующая этим координатам
        button = self.__buttons[x][y]

        # Нажатие этой кнопки
        self.__onClick_Button(button, x, y)

    # Диалоговое окно с выбором режима
    def __modeChoiceWindow(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Mode selection")
        msg_box.setText("In what mode would you like to play?")
        msg_box.setIcon(QMessageBox.Icon.Question)

        # Добавляем кастомные кнопки с нужным текстом
        btn_user = msg_box.addButton("On my PC", QMessageBox.ButtonRole.AcceptRole)
        btn_bot = msg_box.addButton("With a bot", QMessageBox.ButtonRole.AcceptRole)
        btn_cancel = msg_box.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)

        # Отображаем окно (программа ждет ответа — это нормальное поведение exec())
        msg_box.exec()

        # Проверяем, какая именно кнопка была нажата
        clicked_button = msg_box.clickedButton()

        if clicked_button == btn_bot:
            self.__bot = True
            self.__clear()  # Очищаем поле
            self.Field.setEnabled(True)  # Разблокируем поле
        elif clicked_button == btn_user:
            self.__bot = False
            self.__clear()  # Очищаем поле
            self.Field.setEnabled(True)  # Разблокируем поле
        else:
            # Нажата кнопка Cancel или окно закрыли на крестик
            print("Действие отменено")

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

            # Ход бота, если это его ход
            if self.__bot and not self.__move:
                self.__botMove()
        # Если ход ноликов и эта кнопка свободна
        elif not self.__move and button.text() == "":
            button.setText("O")                         # Ставим нолик
            self.__move = not self.__move               # Меняем ход
            self.__field[index_x][index_y] = 2          # Меняем значение в массиве поля

            # Ход бота, если это его ход
            if self.__bot and not self.__move:
                self.__botMove()

        # Проверка на выигрыш/проигрыш в одну строку
        for line in self.__field:
            # Если в одной строке 3 крестика подряд
            if list(line).count(1) == 3:
                #QMessageBox.information(None, "Game", "Crosses has won!")
                self.__Message.setText("Crosses has won!")
                self.Field.setEnabled(False)
            # Если в одной строке 3 нолика подряд
            if list(line).count(2) == 3:
                self.__Message.setText("Zeros has won!")
                #QMessageBox.information(None, "Game", "Zeros has won!")
                self.Field.setEnabled(False)

        for line in self.__field.transpose():
            # Если в одной строке 3 крестика подряд
            if list(line).count(1) == 3:
                #QMessageBox.information(None, "Game", "Crosses has won!")
                self.__Message.setText("Crosses has won!")
                self.Field.setEnabled(False)
            # Если в одной строке 3 нолика подряд
            if list(line).count(2) == 3:
                self.__Message.setText("Zeros has won!")
                #QMessageBox.information(None, "Game", "Zeros has won!")
                self.Field.setEnabled(False)

        # Проверка на выигрыш/проигрыш по диагонали
        Diag_1, Diag_2 = [], []
        # Добавляем в переменные значения диагоналей
        for id in range(3):
            Diag_1.append(self.__field[id][id])
            Diag_2.append(self.__field[id][2-id])

        # Проверка с помощью счёта нулей/крестиков
        if Diag_1.count(1) == 3:
            #QMessageBox.information(None, "Game", "Crosses has won!")
            self.__Message.setText("Crosses has won!")
            self.Field.setEnabled(False)
        if Diag_2.count(1) == 3:
            self.__Message.setText("Crosses has won!")
            #QMessageBox.information(None, "Game", "Crosses has won!")
            self.Field.setEnabled(False)
        if Diag_1.count(2) == 3:
            self.__Message.setText("Zeros has won!")
            #QMessageBox.information(None, "Game", "Zeros has won!")
            self.Field.setEnabled(False)
        if Diag_2.count(2) == 3:
            self.__Message.setText("Zeros has won!")
            #QMessageBox.information(None, "Game", "Zeros has won!")
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
            #QMessageBox.information(None, "Game", "It's a tie!")
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

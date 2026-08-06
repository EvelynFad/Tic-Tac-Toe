from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QMenu, QWidget, QLabel, QStatusBar
from PyQt6.QtCore import pyqtSignal, pyqtSlot, QUrl
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtGui import QAction
from PyQt6 import uic
import numpy as np
import random
import sys


# Window class
class Window(QMainWindow):
    # Type Annotation
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

    # Constructor
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi("window.ui", self)

        # Game field
        self.__field = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]])
        # Game buttons field
        self.__buttons = [
            [self.B_7, self.B_8, self.B_9],
            [self.B_4, self.B_5, self.B_6],
            [self.B_1, self.B_2, self.B_3]
        ]

        # Change moves (crosses and zeros)
        self.__move = True

        # Is there empty places
        self.__free = True

        # Bot mode flag
        self.__bot = True
        # Bot is playing with zeros
        self.__bot_symbol = 2

        # Adding text to status bar
        self.__Message = QLabel("The game has started....")
        self.StatusBar.addWidget(self.__Message)

        # Connecting buttons
        self.B_1.clicked.connect(self.__onClick_B1)
        self.B_2.clicked.connect(self.__onClick_B2)
        self.B_3.clicked.connect(self.__onClick_B3)
        self.B_4.clicked.connect(self.__onClick_B4)
        self.B_5.clicked.connect(self.__onClick_B5)
        self.B_6.clicked.connect(self.__onClick_B6)
        self.B_7.clicked.connect(self.__onClick_B7)
        self.B_8.clicked.connect(self.__onClick_B8)
        self.B_9.clicked.connect(self.__onClick_B9)

        # Connecting menu
        self.M_Game.triggered.connect(self.__onClick_Menu)
        self.M_FAO.triggered.connect(self.__onClick_Menu)

        # Sound effects
        self.__clickSound = QSoundEffect()
        self.__clickSound.setSource(QUrl.fromLocalFile("sounds/mouseClick.wav"))
        self.__clickSound.setVolume(0.2)

        self.__winSound = QSoundEffect()
        self.__winSound.setSource(QUrl.fromLocalFile("sounds/victory.wav"))
        self.__winSound.setVolume(0.9)

    # Clicking menu
    def __onClick_Menu(self, action: QAction):
        # Button that was clicked
        text = action.text()
        # If this button turned out to be "New game"
        if text == "New game":
            self.__modeChoiceWindow()
        # If this button turned out to be "Exit"
        elif text == "Exit":
            self.close()    # Closing window
        # If this button turned out to be "Help"
        elif text == "Help": QMessageBox.about(self, "Help", "No one will help you")

    # Method for bot
    def __botMove(self):
        # Searching for free place
        free = []
        for i in range(3):
            for j in range(3):
                if self.__field[i][j] == 0:
                    free.append((i, j))

        # If there isn't any free place -> do not do anything
        if len(free) == 0:
            return

        # Randomized coordinates choice
        x, y = random.choice(free)
        button = self.__buttons[x][y]

        # Clicking this button
        self.__onClick_Button(button, x, y)

    # Window with mode choice
    def __modeChoiceWindow(self):
        # Creating message box
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Mode selection")
        msg_box.setText("In what mode would you like to play?")
        msg_box.setIcon(QMessageBox.Icon.Question)

        # Custom buttons
        btn_user = msg_box.addButton("On my PC", QMessageBox.ButtonRole.AcceptRole)
        btn_bot = msg_box.addButton("With a bot", QMessageBox.ButtonRole.AcceptRole)
        btn_cancel = msg_box.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)

        # Displaying window
        msg_box.exec()

        # Clicked button
        clicked_button = msg_box.clickedButton()

        # Changing modes
        if clicked_button == btn_bot:
            self.__bot = True
            self.__clear()               # Clearing field
            self.Field.setEnabled(True)  # Disabling field
        elif clicked_button == btn_user:
            self.__bot = False
            self.__clear()               # Clearing field
            self.Field.setEnabled(True)  # Enabling field
        # Closing window
        else:
            print("Action was cancelled")

    # Field clearance
    def __clear(self):
        # Removing crosses and zeros
        self.B_1.setText("")
        self.B_2.setText("")
        self.B_3.setText("")
        self.B_4.setText("")
        self.B_5.setText("")
        self.B_6.setText("")
        self.B_7.setText("")
        self.B_8.setText("")
        self.B_9.setText("")

        # Clearing matrix of field
        self.__field = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]])

        # Enabling move
        self.__move = True
        # Changing text in status bar
        QMessageBox.warning(None, "Game", "The game has started!")
        self.__Message.setText("The game has started!")

    # Check for zeros' win
    def __checkZeroWin(self):
        # 0 0 0
        for line in self.__field:
            # Если в одной строке 3 нолика подряд
            if list(line).count(2) == 3:
                return True
        # 0
        # 0
        # 0
        for line in self.__field.transpose():
            # Если в одной строке 3 нолика подряд
            if list(line).count(2) == 3:
                return True

        # Diagonal win
        Diag_1, Diag_2 = [], []
        for id in range(3):
            Diag_1.append(self.__field[id][id])
            Diag_2.append(self.__field[id][2 - id])

        if Diag_1.count(2) == 3 or Diag_2.count(2) == 3:
            return True

        return False


    # Check for crosses' win
    def __checkCrossWin(self):
        # X X X
        for line in self.__field:
            if list(line).count(1) == 3:
                return True

        # X
        # X
        # X
        for line in self.__field.transpose():
            if list(line).count(1) == 3:
                return True

        # Diagonal win
        Diag_1, Diag_2 = [], []
        for id in range(3):
            Diag_1.append(self.__field[id][id])
            Diag_2.append(self.__field[id][2 - id])

        if Diag_1.count(1) == 3 or Diag_2.count(1) == 3:
            return True

        return False

    # Check for a tie
    def __checkTie(self):
        self.__free = False
        # Checking every line on the field
        for line in self.__field:
            # If there's empty place
            if 0 in line:
                self.__free = True  # Changing flag

        return not self.__free

    # Clicking button
    def __onClick_Button(self, button: QPushButton, index_x: int, index_y: int):
        # If it's crosses' move
        if self.__move and button.text() == "":
            self.__clickSound.play()
            button.setText("X")                         # Putting cross
            self.__field[index_x][index_y] = 1          # Changing it in matrix
            self.__move = not self.__move               # Changing move

            # Bot's move
            if self.__bot and not self.__move:
                self.__botMove()
        # If it's zeros' move
        elif not self.__move and button.text() == "":
            self.__clickSound.play()
            button.setText("O")                         # Putting zero
            self.__move = not self.__move               # Changing move
            self.__field[index_x][index_y] = 2          # Changing it in matrix

            # Bot's move
            if self.__bot and not self.__move:
                self.__botMove()

        # Check for zeros' win
        if self.__checkZeroWin():
            self.__winSound.play()

            self.__Message.setText("Zeros has won!")
            # QMessageBox.information(None, "Game", "Zeros has won!")
            self.Field.setEnabled(False)
        # Check for crosses' win
        if self.__checkCrossWin():
            self.__winSound.play()

            # QMessageBox.information(None, "Game", "Crosses has won!")
            self.__Message.setText("Crosses has won!")
            self.Field.setEnabled(False)
        # Check for a tie
        if self.__checkTie():
            self.__Message.setText("It's a tie!")        # Меняем текст в строке состояния
            #QMessageBox.information(None, "Game", "It's a tie!")
            self.Field.setEnabled(False)            # Блокируем поле

    # Clicking buttons
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

# Main function
def Main():
    # Qt core
    app = QApplication([])
    # Window
    window = Window()
    # Opening window
    window.show()
    # Start
    app.exec()


if __name__ == "__main__": Main()

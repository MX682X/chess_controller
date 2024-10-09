import sys
import queue
import time
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPalette, QColor, QKeyEvent
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QGridLayout,
    QWidget,
    QSizePolicy,
)



class BoardSimulator(QMainWindow):
    def __init__(self, ledQ:queue.Queue, reedQ:queue.Queue):
        super().__init__()

        self.setWindowTitle("Widgets App")

        board_layout = QGridLayout()
        window_layout = QGridLayout()

        self.ledQ = ledQ
        self.reedQ = reedQ

        self.startPos = {
            0: " R",
            1: " N",
            2: " B",
            3: " Q",
            4: " K",
            5: " B",
            6: " N",
            7: " R"
        }
        self.col_to_let = {
            0: "a",
            1: "b",
            2: "c",
            3: "d",
            4: "e",
            5: "f",
            6: "g",
            7: "h",
        }
        self.let_to_col = {
            "a": 0,
            "A": 0,
            "b": 1,
            "B": 1,
            "c": 2,
            "C": 2,
            "d": 3,
            "D": 3,
            "e": 4,
            "E": 4,
            "f": 5,
            "F": 5,
            "g": 6,
            "G": 6,
            "h": 7,
            "H": 7,
        }

        self.black_palette = QPalette(QColor(131, 88, 5))
        self.white_palette = QPalette(QColor(160, 160, 160))
        self.current_field = None
        self.in_hand = "  "

        self.fields = [[],[],[],[],[],[],[],[]]
        for row in range(8):
            for column in range(8):
                button = QPushButton()
                button.setFixedSize(42, 42)
                button.pressed.connect(self.button_on_click)
                if ((column % 2) == (row % 2)):
                    button.setPalette(self.white_palette)
                else:
                    button.setPalette(self.black_palette)
                
                if (row == 0):
                    button.setText(self.startPos[column])
                elif (row == 7):
                    button.setText(self.startPos[column].lower())
                elif (row == 1):
                    button.setText(" P")
                elif (row == 6):
                    button.setText(" p")
                else:
                    button.setText("  ")

                self.fields[row].append([button, row, column])
                board_layout.addWidget(button, 7-row, column)

        for i in range (8):
            board_layout.setRowMinimumHeight(i, 50)
            board_layout.setColumnMinimumWidth(i, 50)

        board_widget = QWidget()
        board_widget.setLayout(board_layout)

        window_widget = QWidget()
        window_widget.setLayout(window_layout)
        window_layout.addWidget(board_widget, 0, 0)
        
        self.reset_button = QPushButton()
        self.reset_button.setFixedSize(250, 50)
        self.reset_button.setText("Reset Positions")
        self.reset_button.pressed.connect(self.reset_positions)
        window_layout.addWidget(self.reset_button, 1, 0)

        self.piece_button = QPushButton()
        self.piece_button.setFixedSize(250, 50)
        self.piece_button.setText("In Hand:  ")
        #piece_button.pressed.connect(self.button_on_click)
        window_layout.addWidget(self.piece_button, 2, 0)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(window_widget)

        app = QApplication(sys.argv)
        app.exec()

        while(1):
            if (ledQ.empty() == False):
                msg = ledQ.get(False)
                if (len(msg) in range(2,4)): #at least a letter or 3 symbols plus new line   
                    if (msg[0] == 's'):
                        col = self.let_to_col[msg[1]]
                        row = int(msg[2])
                        self.set_led("*", row, col)
                    elif (msg[0] == 'k'):
                        col = self.let_to_col[msg[1]]
                        row = int(msg[2])
                        self.set_led(" ", row, col)
                    elif (msg[0] == 'o'):
                        for row in range(8):
                            for col in range(8):
                                self.set_led(" ", row, col)
            time.sleep(0.1)
    
    def set_led(self, val, row, col):
        old_text = self.fields[row][col][0].text()
        old_text[0] = val
        self.fields[row][col][0].setText(old_text)
    
    def button_on_click(self):
        for row in self.fields:
            for field in row:
                if field[0].isDown() is True:
                    piece = field[0].text()
                    if (len(piece) < 2):
                        piece = " "
                    else:
                        piece = piece[1]

                    if (self.in_hand == "  "):
                        if (piece != " "):
                            field[0].setText("  ")
                            command = "t{0}{1}".format(self.column_to_letter[field[1]], field[2])
                            print(command)
                            self.reedQ.put(command + "\n")
                            self.in_hand = " " + piece
                            self.piece_button.setText("In Hand: " + piece)
                    else:
                        if (piece == " "):  # empty field
                            field[0].setText(self.in_hand)
                            self.in_hand = "  "
                            self.piece_button.setText("In Hand: ")
                            command = "p{0}{1}".format(self.column_to_letter[field[1]], field[2])
                            print(command)
                            self.reedQ.put(command + "\n")
                        else:               # capturing figure
                            command = "t{0}{1}".format(self.column_to_letter[field[1]], field[2])
                            print(command)
                            self.reedQ.put(command + "\n")
                            time.sleep(0.1)
                            field[0].setText(self.in_hand)
                            self.in_hand = "  "
                            self.piece_button.setText("In Hand: ")
                            command = "p{0}{1}".format(self.column_to_letter[field[1]], field[2])
                            print(command)
                            self.reedQ.put(command + "\n")
                    
        pass

    def reset_positions(self):
        for row in range(8):
            for column in range(8):
                button = self.fields[row][column][0]
                if (row == 0):
                    button.setText(self.startPos[column])
                elif (row == 7):
                    button.setText(self.startPos[column].lower())
                elif (row == 1):
                    button.setText(" P")
                elif (row == 6):
                    button.setText(" p")
                else:
                    button.setText("  ")



#ledQ = queue.Queue()
#reedQ = queue.Queue()
#window = BoardSimulator(ledQ, reedQ)
#window.show()

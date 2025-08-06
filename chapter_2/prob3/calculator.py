import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

form_class = uic.loadUiType("calculator.ui")[0]


class main_window(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.current_input = "0"
        self.setupUi(self)
        self.btn_0.clicked.connect(lambda: self.add_number("0"))
        self.btn_1.clicked.connect(lambda: self.add_number("1"))
        self.btn_2.clicked.connect(lambda: self.add_number("2"))
        self.btn_3.clicked.connect(lambda: self.add_number("3"))
        self.btn_4.clicked.connect(lambda: self.add_number("4"))
        self.btn_5.clicked.connect(lambda: self.add_number("5"))
        self.btn_6.clicked.connect(lambda: self.add_number("6"))
        self.btn_7.clicked.connect(lambda: self.add_number("7"))
        self.btn_8.clicked.connect(lambda: self.add_number("8"))
        self.btn_9.clicked.connect(lambda: self.add_number("9"))
        self.btn_dot.clicked.connect(lambda: self.add_dot())
        self.btn_all_clear.clicked.connect(lambda: self.all_clear())
        self.btn_pos_neg.clicked.connect(lambda: self.flip_pos_neg())

    def add_number(self, num):
        print(self.current_input)

        if len(self.current_input) >= 12 and self.current_input != "0":
            return

        if self.current_input == '0':
            self.current_input = num
        else:
            self.current_input += num

        self.lcdNumber.display(self.current_input)

    def all_clear(self):
        self.lcdNumber.display(0)
        self.current_input = "0"
        self.label_pos_neg.setText('')

    def add_dot(self):
        if self.current_input.find('.') == -1:
            self.current_input += '.'
            self.lcdNumber.display(self.current_input)

    def flip_pos_neg(self):
        if self.label_pos_neg.text() == '' or self.label_pos_neg.text() == '+':
            self.label_pos_neg.setText('-')
        elif self.label_pos_neg.text() == '-':
            self.label_pos_neg.setText('+')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = main_window()
    main_window.show()
    sys.exit(app.exec_())

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

form_class = uic.loadUiType("calculator.ui")[0]


def parse_input(n: str):
    try:
        return int(n)
    except ValueError:
        try:
            return float(n)
        except ValueError:
            return False


class main_window(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.precedence = {
            '+' : 1, '-': 1,
            '*' : 2, '/': 2,
            '(': 0
        }
        self.infix_stack = []
        self.postfix_stack = []
        self.operator_stack = []
        self.calculator_stack = []

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
        self.btn_add.clicked.connect(lambda: self.add())
        self.btn_subtract.clicked.connect(lambda: self.subtract())
        self.btn_multiply.clicked.connect(lambda: self.multyply())
        self.btn_divide.clicked.connect(lambda: self.divide())
        self.btn_equal.clicked.connect(lambda: self.equal())
        self.btn_dot.clicked.connect(lambda: self.add_dot())
        self.btn_all_clear.clicked.connect(lambda: self.all_clear())
        self.btn_pos_neg.clicked.connect(lambda: self.flip_pos_neg())

    def add_number(self, num):
        if len(self.current_input) >= 12 and self.current_input != "0":
            return

        if self.current_input == '0':
            self.current_input = num
        else:
            self.current_input += num

        self.lineEdit.setText(self.current_input)
        print(self.current_input)

    def all_clear(self):
        self.lineEdit.setText("")
        self.current_input = "0"
        print("All cleared")

    def add_dot(self):
        if self.current_input.find('.') == -1:
            self.current_input += '.'
            self.lineEdit.setText(self.current_input)

    def flip_pos_neg(self):
        self.current_input = str(float(self.current_input) * -1)
        self.lineEdit.setText(self.current_input)

    def add(self):
        self.infix_stack.append(self.lineEdit.text())
        print(f"numeric {self.lineEdit.text()} added")
        self.infix_stack.append('+')
        print("operator + added ")
        self.lineEdit.setText("")
        self.current_input = "0"
        print(f'{self.infix_stack}')

    def subtract(self):
        self.infix_stack.append(self.lineEdit.text())
        print(f"numeric {self.lineEdit.text()} added")
        self.infix_stack.append('-')
        print("operator - added ")
        self.lineEdit.setText("")
        self.current_input = "0"
        print(f'{self.infix_stack}')

    def multyply(self):
        self.infix_stack.append(self.lineEdit.text())
        print(f"numeric {self.lineEdit.text()} added")
        self.infix_stack.append('*')
        print("operator * added ")
        self.lineEdit.setText("")
        self.current_input = "0"
        print(f'{self.infix_stack}')

    def divide(self):
        self.infix_stack.append(self.lineEdit.text())
        print(f"numeric {self.lineEdit.text()} added")
        self.infix_stack.append('/')
        print("operator / added ")
        self.lineEdit.setText("")
        self.current_input = "0"
        print(f'{self.infix_stack}')

    def equal(self):
        print("start calculating...")
        if self.lineEdit.text():
            self.infix_stack.append(self.lineEdit.text())
            print(f"numeric {self.lineEdit.text()} added")

        print(f"infix_stack : {self.infix_stack}")
        print(f"-------------------------------------")

        for i in self.infix_stack:
            # i 가 연산자일경우
            if parse_input(i) is False:
                # 스택이 비어있으면 바로 append
                if len(self.operator_stack) == 0:
                    self.operator_stack.append(i)

                else:
                    while self.operator_stack and \
                            self.precedence.get(self.operator_stack[-1], -1) >= \
                            self.precedence.get(i, -1):

                        self.postfix_stack.append(self.operator_stack.pop())
                        print('postfix_stack : ', self.postfix_stack)
                        print('operator_stack : ', self.operator_stack)

                    self.operator_stack.append(i)
                    print('operator_stack : ', self.operator_stack)
            else:
                self.postfix_stack.append(parse_input(i))
                print('postfix_stack : ', self.postfix_stack)

        while self.operator_stack:
            self.postfix_stack.append(self.operator_stack.pop())
            print('postfix_stack : ', self.postfix_stack)

        for p in self.postfix_stack:
            if parse_input(p) is False:
                print(f'calculator stack before calculating : {self.calculator_stack}')

                if len(self.calculator_stack) < 2:
                    self.lineEdit.setText("Error")
                    print("ERROR : Not enough operands")
                    # 스택 초기화 후 함수 종료
                    self.operator_stack = []
                    self.infix_stack = []
                    self.postfix_stack = []
                    self.calculator_stack = []  # 계산 스택도 비워줘야 합니다.
                    self.current_input = "0"
                    return

                # tmp2가 첫번째 피연산자, tmp1가 두번째 피연산자임(스택 구조상 그렇게 됨)
                tmp1 = self.calculator_stack.pop()
                tmp2 = self.calculator_stack.pop()
                tmp_total = 0

                if p == '+':
                    tmp_total = tmp2 + tmp1
                elif p == '-':
                    tmp_total = tmp2 - tmp1
                elif p == '*':
                    tmp_total = tmp2 * tmp1
                elif p == '/':
                    if tmp1 == 0:
                        self.lineEdit.setText("Error: Div by 0")
                        # 스택 초기화 후 함수 종료
                        self.operator_stack = []
                        self.infix_stack = []
                        self.postfix_stack = []
                        self.calculator_stack = []
                        self.current_input = "0"
                        return

                    tmp_total = tmp2 / tmp1

                print(f'{tmp2} {p} {tmp1} = {tmp_total}')
                self.calculator_stack.append(tmp_total)
                print(f'calculator stack after calculating : {self.calculator_stack}')

            else:
                self.calculator_stack.append(p)
                print(f'{self.calculator_stack}')

        if self.calculator_stack:
            self.lineEdit.setText(str(self.calculator_stack.pop()))
            print("calculator stack popped")
        else:
            self.lineEdit.setText("")

        self.operator_stack = []
        self.infix_stack = []
        self.postfix_stack = []
        self.current_input = "0"
        print("initializing stack")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = main_window()
    main_window.show()
    sys.exit(app.exec_())

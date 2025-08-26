# engineering_calculator.py

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic

# 1. 계산 로직이 담긴 클래스를 다른 파일에서 불러옵니다.
from engineering_logic import EngineeringCalculator

# 2. .ui 파일로부터 UI 클래스를 로드합니다.
# 파일 이름은 실제 .ui 파일 이름과 일치해야 합니다.
form_class = uic.loadUiType("engineering_calculator.ui")[0]


class MainApp(QWidget, form_class):
    """
    UI 제어와 이벤트 처리를 담당하는 메인 애플리케이션 클래스.
    계산 로직(EngineeringCalculator)과 UI(engineering_calculator.ui)를 연결하는 다리 역할을 합니다.
    """

    def __init__(self):
        super().__init__()
        # .ui 파일에 정의된 위젯들을 초기화합니다.
        self.setupUi(self)

        # 3. 계산기 로직 클래스의 인스턴스를 생성합니다.
        self.logic = EngineeringCalculator()

        # 4. 모든 버튼의 클릭 이벤트를 적절한 메소드에 연결합니다.
        self.connect_buttons()
        self.show()

    def connect_buttons(self):
        """UI의 모든 버튼 시그널을 핸들러 메소드에 연결합니다."""
        # 숫자 버튼 (0-9)
        self.btn_0.clicked.connect(lambda: self.append_to_display('0'))
        self.btn_1.clicked.connect(lambda: self.append_to_display('1'))
        self.btn_2.clicked.connect(lambda: self.append_to_display('2'))
        self.btn_3.clicked.connect(lambda: self.append_to_display('3'))
        self.btn_4.clicked.connect(lambda: self.append_to_display('4'))
        self.btn_5.clicked.connect(lambda: self.append_to_display('5'))
        self.btn_6.clicked.connect(lambda: self.append_to_display('6'))
        self.btn_7.clicked.connect(lambda: self.append_to_display('7'))
        self.btn_8.clicked.connect(lambda: self.append_to_display('8'))
        self.btn_9.clicked.connect(lambda: self.append_to_display('9'))
        self.btn_decimal.clicked.connect(lambda: self.append_to_display('.'))

        # 연산자 버튼 (+, -, *, /, ^)
        self.btn_add.clicked.connect(lambda: self.append_to_display('+'))
        self.btn_subtract.clicked.connect(lambda: self.append_to_display('-'))
        self.btn_multiply.clicked.connect(lambda: self.append_to_display('*'))  # '×' 기호 대신 '*' 사용
        self.btn_divide.clicked.connect(lambda: self.append_to_display('/'))  # '÷' 기호 대신 '/' 사용
        self.btn_pow_y.clicked.connect(lambda: self.append_to_display('^'))  # x^y 버튼

        # 괄호 버튼
        self.btn_lparen.clicked.connect(lambda: self.append_to_display('('))
        self.btn_rparen.clicked.connect(lambda: self.append_to_display(')'))

        # 함수 버튼 (함수 이름 뒤에 여는 괄호를 붙여줌)
        self.btn_sin.clicked.connect(lambda: self.append_to_display('sin('))
        self.btn_cos.clicked.connect(lambda: self.append_to_display('cos('))
        self.btn_tan.clicked.connect(lambda: self.append_to_display('tan('))
        self.btn_sinh.clicked.connect(lambda: self.append_to_display('sinh('))
        self.btn_cosh.clicked.connect(lambda: self.append_to_display('cosh('))
        self.btn_tanh.clicked.connect(lambda: self.append_to_display('tanh('))
        self.btn_log10.clicked.connect(lambda: self.append_to_display('log('))  # log10 대신 log 사용
        self.btn_ln.clicked.connect(lambda: self.append_to_display('ln('))

        # 제곱/세제곱 버튼
        self.btn_sqr.clicked.connect(lambda: self.append_to_display('^2'))
        self.btn_cub.clicked.connect(lambda: self.append_to_display('^3'))

        # 기능 버튼
        self.btn_equals.clicked.connect(self.calculate_result)  # '=' 버튼
        self.btn_ac.clicked.connect(self.clear_display)  # 'AC' 버튼 (All Clear)

        # TODO: 아직 구현되지 않은 기능들
        self.btn_plusminus.clicked.connect(self.toggle_sign)
        # self.btn_percent.clicked.connect(self.apply_percent)
        # ...

    def append_to_display(self, text: str):
        """디스플레이 창에 텍스트를 추가합니다."""
        current_text = self.display.text()

        # 현재 디스플레이에 '0'만 있거나 오류 메시지가 표시된 경우, 새로 입력된 텍스트로 대체
        if current_text == '0' or "오류" in current_text or "없음" in current_text:
            self.display.setText(text)
        else:
            self.display.setText(current_text + text)

    def toggle_sign(self):
        """'±' 버튼을 눌렀을 때, 로직 클래스를 호출하여 부호 반전을 처리합니다."""
        current_text = self.display.text()

        # 로직 객체에 현재 수식을 전달하고, 처리된 결과를 받습니다.
        new_text = self.logic.toggle_last_number_sign(current_text)

        # 처리된 결과로 디스플레이를 업데이트합니다.
        self.display.setText(new_text)

    def calculate_result(self):
        """'=' 버튼을 눌렀을 때, 디스플레이의 수식을 계산하고 결과를 표시합니다."""
        try:
            expression = self.display.text()
            # 로직 클래스의 calculate 메소드를 호출하여 결과만 받음
            result = self.logic.calculate(expression)
            # 결과값을 다시 디스플레이에 설정
            self.display.setText(str(result))

        except Exception as e:
            self.display.setText("계산 오류")

    def clear_display(self):
        """'AC' 버튼을 눌렀을 때, 디스플레이를 '0'으로 초기화합니다."""
        self.display.setText('0')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    sys.exit(app.exec_())
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic

form_class = uic.loadUiType("sci_cal.ui")[0]


class MainApp(QWidget, form_class):
    def __init__(self):
        super().__init__()
        # .ui 파일에 정의된 위젯들을 초기화합니다.
        self.setupUi(self)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    sys.exit(app.exec_())
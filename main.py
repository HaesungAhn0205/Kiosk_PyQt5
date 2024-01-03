import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("Kiosk_draft.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.menu = {'김밥': 2000, '라면': 4000, '떡볶이': 4000, '순대': 3000 }
        for i in range(1, 5):
            button_object_name = f"Button_menu{i}"
            menu_button = getattr(self, button_object_name, None)
            if menu_button:
                menu_button.clicked.connect(self.create_menu_button_handler(menu_button))
            else:
                print(f"Button '{button_object_name}' not found!")

    def create_menu_button_handler(self, menu_button) :
        def handler():
            cart_list_widget = self.findChild(QListWidget, 'CartList')
            menu_text = menu_button.text()
            price = self.menu.get(menu_text, 0)  # 메뉴의 가격 가져오기
            item_text = f"{menu_text} - {price}원"
            item = QListWidgetItem(item_text)
            cart_list_widget.addItem(item)
        return handler

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)
    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    #프로그램 화면을 보여주는 코드
    myWindow.show()
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()

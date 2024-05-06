import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from os import environ

# def suppress_qt_warnings():  #해상도별 글자크기 강제 고정함수
#     environ["QT_DEVICE_PIXEL_RATIO"] = "0"
#     environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
#     environ["QT_SCREEN_SCALE_FACTORS"] = "1"
#     environ["QT_SCALE_FACTOR"] = "1"

# 메인 윈도우 UI파일 연결
form_class = uic.loadUiType("Kiosk_draft.ui")[0]

# 화면을 띄우는데 사용되는 Class 선언
class Second(QDialog, form_class): # 최종 주문창 ui를 불러오는 클래스
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("Kiosk_final.ui", self)
        self.show()

class WindowClass(QMainWindow, form_class):

    def Second_window(self):  # Second 클래스를 호출하는 함수 정의
        window_2 = Second()
        window_2.exec()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.Payment_Button.clicked.connect(self.Second_window) # 최종 주문 버튼을 클릭하면 Second Window 창 띄움
        self.show()

        self.menu = {'김밥': 2000, '라면': 4000, '떡볶이': 4000, '순대': 3000, '튀김': 4000, '어묵': 1000, '콜라': 1500, '사이다': 1500}
        self.cart_items = []  # 장바구니에 각 메뉴의 가격과 개수를 저장하는 리스트
        self.order_items = []  # 최종 주문내역에 들어갈 메뉴, 개수, 가격을 저장하는 리스트

        self.Total_Button.clicked.connect(self.Total_button_Function)
        self.Clear_Button.clicked.connect(self.Clear_button_Function)

        self.Button_menu1.clicked.connect(self.create_menu_button_handler('김밥', 2000))
        self.Button_menu2.clicked.connect(self.create_menu_button_handler('라면', 4000))
        self.Button_menu3.clicked.connect(self.create_menu_button_handler('떡볶이', 4000))
        self.Button_menu4.clicked.connect(self.create_menu_button_handler('순대', 3000))
        self.Button_menu5.clicked.connect(self.create_menu_button_handler('튀김', 4000))
        self.Button_menu6.clicked.connect(self.create_menu_button_handler('어묵', 1000))
        self.Button_menu7.clicked.connect(self.create_menu_button_handler('콜라', 1500))
        self.Button_menu8.clicked.connect(self.create_menu_button_handler('사이다', 1500))

    def create_menu_button_handler(self, menu_name, price):
        def handler():
            cart_list_widget = self.findChild(QListWidget, 'CartList')

            for i in range(cart_list_widget.count()):
                item = cart_list_widget.item(i)
                if item.text().startswith(menu_name):
                    count = int(item.text().split(' - ')[1].split('개')[0]) + 1
                    new_item_text = f"{menu_name} - {count}개 - {price * count}원"
                    item.setText(new_item_text)
                    return

            item_text = f"{menu_name} - 1개 - {price}원"
            item = QListWidgetItem(item_text)
            cart_list_widget.addItem(item)

        return handler

    def Total_button_Function(self):
        cart_list_widget = self.findChild(QListWidget, 'CartList')
        order_list_widget = self.findChild(QListWidget, 'OrderList')

        total_price = 0

        for index in range(cart_list_widget.count()):
            item = cart_list_widget.item(index)

            price = int(item.text().split(' - ')[2].replace('원', ''))
            total_price += price

        for index in range(order_list_widget.count()):
            item = order_list_widget.item(index)
            if item.text().startswith("총 가격"):
                order_list_widget.takeItem(index)
                break
        total_price_text = f"총 가격 - {total_price}원"
        total_price_item = QListWidgetItem(total_price_text)
        order_list_widget.addItem(total_price_item)

    def Clear_button_Function(self):
        self.findChild(QListWidget, 'CartList').clear()
        self.findChild(QListWidget, 'OrderList').clear()

if __name__ == "__main__":
    # suppress_qt_warnings()
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)
    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    # 프로그램 화면을 보여주는 코드
    myWindow.show()
    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()

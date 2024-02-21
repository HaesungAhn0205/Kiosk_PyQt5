import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

#UI파일 연결
form_class = uic.loadUiType("Kiosk_draft.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.menu = {'김밥': 2000, '라면': 4000, '떡볶이': 4000, '순대': 3000, '튀김': 4000, '어묵': 1000, '콜라': 1500, '사이다': 1500 }
        self.cart_items = [] #장바구니에 각 메뉴의 가격과 개수를 저장하는 리스트
        self.order_items = []  #최종 주문내역에 들어갈 메뉴, 개수, 가격을 저장하는 리스트

        self.Total_Button.clicked.connect(self.Total_button_Function)
        self.Clear_Button.clicked.connect(self.Clear_button_Function)

        for i in range(1, 9):
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

            for i in range(cart_list_widget.count()):
                item = cart_list_widget.item(i)
                if item.text().startswith(menu_text):
                    count = int(item.text().split(' - ')[1].split('개')[0]) + 1
                    new_item_text = f"{menu_text} - {count}개 - {price * count}원"
                    item.setText(new_item_text)
                    return

            item_text = f"{menu_text} - 1개 - {price}원"
            item = QListWidgetItem(item_text)
            cart_list_widget.addItem(item)

        return handler

    def Total_button_Function(self) :
        cart_list_widget = self.findChild(QListWidget, 'CartList')
        order_list_widget = self.findChild(QListWidget, 'OrderList')

        total_price = 0

        for index in range(cart_list_widget.count()):
            item = cart_list_widget.item(index)
            # order_list_widget.addItem(item.text())  주석처리하면 주문내역에 총 가격만 뜸

            price = int(item.text().split(' - ')[2].replace('원', ''))
            total_price += price

        total_price_text = f"총 가격 - {total_price}원"
        total_price_item = QListWidgetItem(total_price_text)
        order_list_widget.addItem(total_price_item)

        # self.findChild(QListWidget, 'CartList').clear()  장바구니 내용 삭제

    def Clear_button_Function(self):
        self.findChild(QListWidget, 'CartList').clear()
        self.findChild(QListWidget, 'OrderList').clear()

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)
    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    #프로그램 화면을 보여주는 코드
    myWindow.show()
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()

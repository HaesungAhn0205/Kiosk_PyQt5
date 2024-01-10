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

        self.menu = {'김밥': 2000, '라면': 4000, '떡볶이': 4000, '순대': 3000 }
        self.cart_items = [] #장바구니에 각 메뉴의 가격과 개수를 저장하는 리스트
        # self.order_items = []  #최종 주문내역에 들어갈 메뉴, 개수, 가격을 저장하는 리스트

        # self.Total_Button.clicked.connect(self.Total_button_Function)

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

            cart_item = {'menu_text': menu_text, 'price': price, 'quantity': 1}
            self.cart_items.append(cart_item)

            # 장바구니 리스트 위젯 업데이트
            self.update_cart_list(cart_list_widget)
            # item_text = f"{menu_text} - {price}원"
            # item = QListWidgetItem(item_text)
            # cart_list_widget.addItem(item)



        return handler

    def update_cart_list(self, cart_list_widget):
        # 장바구니 리스트 위젯 초기화
        cart_list_widget.clear()

        # 장바구니 아이템 정보를 합산하여 표시
        total_price = 0
        for item in self.cart_items:
            total_price += item['price'] * item['quantity']
            item_text = f"{item['menu_text']} - {item['quantity']}개 - {item['price'] * item['quantity']}원"
            cart_list_widget.addItem(item_text)

        # 총 가격 항목 추가
        total_text = f"총 가격: {total_price}원"
        cart_list_widget.addItem(total_text)
    # def Total_button_Function(self) :
    #     cart_list_widget = self.findChild(QListWidget, 'CartList')
    #     Order_list_widget = self.findChild(QListWidget, 'OrderList')
    #
    #
    #     self.findChild(QListWidget, 'CartList').clear()

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)
    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    #프로그램 화면을 보여주는 코드
    myWindow.show()
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()

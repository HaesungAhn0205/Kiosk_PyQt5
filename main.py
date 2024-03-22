import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import RPi.GPIO as GPIO
from time import sleep

# 점자 출력에 필요한 GPIO 설정
data_pins = [17, 18, 27]  # 데이터 핀 번호 리스트
latch_pin = 22  # 래치 핀 번호
clock_pin = 23  # 클럭 핀 번호
GPIO.setmode(GPIO.BCM)
for pin in data_pins:
    GPIO.setup(pin, GPIO.OUT)
GPIO.setup(latch_pin, GPIO.OUT)
GPIO.setup(clock_pin, GPIO.OUT)

# 점자 출력 함수 정의
def toggle_switch(pin, state):
    GPIO.output(pin, state)

def refresh():
    GPIO.output(latch_pin, 1)
    GPIO.output(latch_pin, 0)

def print_braille(character):
    braille_dict = {
        '김밥': [
            [[0, 1, 0, 0, 0, 0]],  # '⠈'
            [[1, 0, 1, 0, 1, 0]],  # '⠕'
            [[0, 0, 1, 0, 0, 1]],  # '⠢'
            [[0, 1, 0, 1, 0, 0]],  # '⠈'
            [[1, 0, 1, 0, 0, 0]],  # '⠕'
        ],
        '떡볶이': [
            [[0, 0, 0, 0, 0, 1]],  # '⠈'
            [[0, 1, 1, 0, 0, 0]],  # '⠕'
            [[1, 1, 0, 1, 0, 1]],  # '⠢'
            [[0, 1, 0, 1, 0, 0]],  # '⠈'
            [[1, 1, 0, 0, 1, 0]],  # '⠕'
            [[1, 0, 1, 0, 1, 0]]  # '⠢'
        ],
        '라면': [
            [[0, 0, 0, 1, 0, 0]],  # '⠇'
            [[1, 0, 1, 0, 0, 1]],  # '⠁'
            [[1, 0, 0, 1, 0, 0]],  # '⠁'
            [[1, 0, 0, 0, 0, 1]]  # '⠁'
        ],
        '순대': [
            [[0, 0, 0, 0, 0, 1]],  # '⠇'
            [[1, 1, 1, 1, 0, 0]],  # '⠁'
            [[0, 1, 1, 0, 0, 0]],  # '⠁'
            [[1, 0, 1, 1, 1, 0]]  # '⠁'
        ],
        '튀김': [
            [[1, 0, 1, 1, 0, 0]],  # '⠇'
            [[1, 1, 0, 0, 1, 0]],  # '⠁'
            [[1, 0, 1, 1, 1, 0]],  # '⠇'
            [[0, 1, 0, 0, 0, 0]],  # '⠁'
            [[1, 0, 0, 1, 1, 0]],  # '⠇'
            [[0, 0, 1, 0, 0, 1]]  # '⠁'
        ],
        '어묵': [
            [[0, 1, 1, 0, 1, 0]],  # '⠇'
            [[1, 0, 0, 1, 0, 0]],  # '⠁'
            [[1, 1, 0, 0, 1, 0]],  # '⠇'
            [[1, 0, 0, 0, 0, 0]]  # '⠁'
        ],
        '콜라': [
            [[1, 1, 1, 0, 0, 0]],  # '⠇'
            [[1, 0, 0, 0, 1, 1]],  # '⠁'
            [[0, 0, 1, 0, 0, 0]],  # '⠇'
            [[0, 0, 0, 1, 0, 0]],  # '⠁'
            [[1, 0, 1, 0, 0, 0]]  # '⠁'
        ],
        '사이다': [
            [[1, 0, 1, 0, 1, 0]],  # '⠇'
            [[1, 0, 0, 1, 1, 0]],  # '⠁'
            [[0, 1, 1, 0, 0, 0]]  # '⠁'
        ]
    }
    for i in range(len(data_pins)):
        for row in braille_dict[character][i]:
            toggle_switch(data_pins[i], row)
            refresh()

# PyQt5 UI 로드
form_class = uic.loadUiType("Kiosk_draft.ui")[0]

# 최종 주문 창 클래스
class Second(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("Kiosk_final.ui", self)
        self.show()

# 메인 창 클래스
class WindowClass(QMainWindow, form_class):
    def Second_window(self):
        window_2 = Second()
        window_2.exec()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 주문 버튼 클릭 시 최종 주문 창 띄우기
        self.Payment_Button.clicked.connect(self.Second_window)

        # 장바구니, 주문 내역 초기화 버튼과 기능 연결
        self.Total_Button.clicked.connect(self.Total_button_Function)
        self.Clear_Button.clicked.connect(self.Clear_button_Function)

        # 메뉴 버튼과 메뉴 선택 핸들러 연결
        self.Button_menu1.clicked.connect(self.create_menu_button_handler('김밥', 2000))
        self.Button_menu2.clicked.connect(self.create_menu_button_handler('라면', 4000))
        self.Button_menu3.clicked.connect(self.create_menu_button_handler('떡볶이', 4000))
        self.Button_menu4.clicked.connect(self.create_menu_button_handler('순대', 3000))
        self.Button_menu5.clicked.connect(self.create_menu_button_handler('튀김', 4000))
        self.Button_menu6.clicked.connect(self.create_menu_button_handler('어묵', 1000))
        self.Button_menu7.clicked.connect(self.create_menu_button_handler('콜라', 1500))
        self.Button_menu8.clicked.connect(self.create_menu_button_handler('사이다', 1500))

    # 메뉴 버튼 핸들러 함수
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

    # 총 주문 가격 계산 함수
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

        # 최종 주문 내역을 점자로 출력
        for index in range(cart_list_widget.count()):
            item = cart_list_widget.item(index)
            menu_name = item.text().split(' - ')[0]
            print_braille(menu_name)

    # 장바구니 비우기 함수
    def Clear_button_Function(self):
        self.findChild(QListWidget, 'CartList').clear()
        self.findChild(QListWidget, 'OrderList').clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()

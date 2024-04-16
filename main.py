import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import RPi.GPIO as GPIO
from time import sleep

# BCM 핀 번호로 라즈베리 파이의 물리적 핀에 대한 대응을 정의합니다.
gpio_map = {
    'data_pins': [17, 18, 27, 22, 23, 24, 25, 4, 5, 6, 12, 13, 19, 16, 26, 20, 21, 7],  # 데이터 핀 번호 리스트 (18개)
    'latch_pin': 8,  # 래치 핀 번호
    'clock_pin': 9,  # 클럭 핀 번호
}

# GPIO 핀 모드 설정
GPIO.setmode(GPIO.BCM)
for pin in gpio_map['data_pins']:
    GPIO.setup(pin, GPIO.OUT)
GPIO.setup(gpio_map['latch_pin'], GPIO.OUT)
GPIO.setup(gpio_map['clock_pin'], GPIO.OUT)


def toggle_switch(pin, state):
    GPIO.output(pin, state)


def refresh():
    GPIO.output(gpio_map['latch_pin'], 1)
    GPIO.output(gpio_map['latch_pin'], 0)


def print_braille(braille):
    for i in range(len(gpio_map['data_pins'])):
        for row in braille[i]:
            toggle_switch(gpio_map['data_pins'][i], row)
            refresh()


def print_braille_number(number):
    # 숫자에 해당하는 점자를 딕셔너리에 저장
    number_braille = {    #아직 완성 x
        '0': [
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        ],
        '1': [
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        ],
        '2': [
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        ],
        '3': [
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        ],
        '4': [
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        ],
        '5': [
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        ],
        '6': [
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        ],
        '7': [
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        ],
        '8': [
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        ],
        '9': [
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        ],
    }

    # 주어진 숫자를 문자열로 변환하여 한 자리씩 점자 출력
    number_str = str(number)
    for digit in number_str:
        if digit in number_braille:
            print_braille(number_braille[digit])
            sleep(0.1)


def main():
    try:
        menu_braille = {
            '김밥': [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ],
            '떡볶이': [
                [0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            '라면': [
                [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            '순대': [
                [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            '튀김': [
                [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            '사이다': [
                [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            '콜라': [
                [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
        }

        if menu_name in menu_braille:
            print_braille(menu_braille[menu_name])
            sleep(0.5)

            # 주문 개수에 해당하는 점자 출력
            print_braille_number(menu_count)

            # '개'에 해당하는 점자 출력
            count_braille = {
                '개': [
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                ],
            }

            # 0.5초 후 모든 핀을 0으로 유지
            for pin in gpio_map['data_pins']:
                GPIO.output(pin, 0)
            refresh()



    finally:
        # 점자 출력기 종료
        for pin in gpio_map['data_pins']:
            GPIO.output(pin, 0)
        GPIO.output(gpio_map['latch_pin'], 0)
        GPIO.cleanup()


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

        self.focused_button = self.Button_menu1
        #GPIO 핀 설정
        GPIO.setmode(GPIO.BCM)
        #핀번호 임의 설정
        GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #GPIO 이벤트 핸들러 설정
        GPIO.add_event_detect(19, GPIO.FALLING, callback=self.move_focus_left, bouncetime=300)
        GPIO.add_event_detect(20, GPIO.FALLING, callback=self.move_focus_right, bouncetime=300)

    # GPIO 물리버튼 코드
    def move_focus_left(self, channel):
        self.focusPreviousChild()

    def move_focus_right(self, channel):
        self.focusNextChild()

    #포커스 스타일 변경
    def setFocusToButton(self, button):
        # 현재 포커스를 가진 버튼의 스타일을 초기화
        if hasattr(self, 'focused_button'):
            self.focused_button.setStyleSheet("")

        # 새로운 포커스를 가질 버튼의 스타일을 설정
        button.setStyleSheet("background-color: yellow;")
        self.focused_button = button

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

import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import RPi.GPIO as GPIO
import time

# UI 파일 로드
main_window_ui, _ = uic.loadUiType("Kiosk_draft.ui")
second_window_ui, _ = uic.loadUiType("Kiosk_final.ui")

#메인 윈도우 정의
class WindowClass(QMainWindow, main_window_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.menu = {'김밥': 2000, '라면': 4000, '떡볶이': 4000, '순대': 3000, '튀김': 4000, '어묵': 1000, '콜라': 1500, '사이다': 1500}

        self.menu_buttons = [
            self.Button_menu1, self.Button_menu2, self.Button_menu3,
            self.Button_menu4, self.Button_menu5, self.Button_menu6,
            self.Button_menu7, self.Button_menu8
        ]
        self.set_button_styles()

        self.braille_menu = {
           '김밥': [
               [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0],
               [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
           ],
           '라면': [
               [1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1],
               [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
           ],
           '떡볶이': [
               [1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0],
               [1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1],
           ],
           '순대': [
               [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
               [0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
           ],
           '튀김': [
               [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1],
               [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0],
           ],
           '어묵': [
               [1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1],
               [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
           ],
           '콜라': [
               [0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1],
               [1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
           ],
           '사이다': [
               [0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1],
           ]
        }

        self.setup_gpio()
        self.connect_buttons()

    def setup_gpio(self):
        # 버튼 핀 설정
        BUTTON_PIN_prev = 22
        BUTTON_PIN_next = 27
        BUTTON_PIN_press = 17   # enter key
        BUTTON_PIN_braille = 4  # braille print
        BUTTON_PIN_total = 18
        BUTTON_PIN_clear = 15
        BUTTON_PIN_payment = 14

        self.solenoid_pins = [
            26, 19, 13, 6, 5, 11, 9, 10, 21, 20, 16, 12, 7, 8, 25, 24, 3, 2
        ]

        # BCM 핀 넘버링
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_PIN_payment, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # input 설정, 내부 풀업 저항 사용
        GPIO.setup(BUTTON_PIN_total, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BUTTON_PIN_clear, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BUTTON_PIN_prev, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BUTTON_PIN_next, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BUTTON_PIN_press, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BUTTON_PIN_braille, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 여기까지 버튼

        for i in self.solenoid_pins: # 솔레노이드 모터 output setup
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, GPIO.LOW)

        GPIO.add_event_detect(BUTTON_PIN_payment, GPIO.FALLING, callback=self.payment_button_callback, bouncetime=3000) #스위치 버튼 콜백 등록
        GPIO.add_event_detect(BUTTON_PIN_total, GPIO.FALLING, callback=self.total_button_callback, bouncetime=3000)
        GPIO.add_event_detect(BUTTON_PIN_clear, GPIO.FALLING, callback=self.clear_button_callback, bouncetime=3000)
        GPIO.add_event_detect(BUTTON_PIN_prev, GPIO.FALLING, callback=self.focus_previous_menu_button_callback, bouncetime=300)
        GPIO.add_event_detect(BUTTON_PIN_next, GPIO.FALLING, callback=self.focus_next_menu_button_callback, bouncetime=300)
        GPIO.add_event_detect(BUTTON_PIN_press, GPIO.FALLING, callback=self.press_current_button_callback, bouncetime=300)
        GPIO.add_event_detect(BUTTON_PIN_braille, GPIO.FALLING, callback=self.braille_output_button_callback, bouncetime=3000)



    def connect_buttons(self):
        self.Button_menu1.clicked.connect(self.add_to_cart('김밥', 2000))
        self.Button_menu2.clicked.connect(self.add_to_cart('라면', 4000))
        self.Button_menu3.clicked.connect(self.add_to_cart('떡볶이', 4000))
        self.Button_menu4.clicked.connect(self.add_to_cart('순대', 3000))
        self.Button_menu5.clicked.connect(self.add_to_cart('튀김', 4000))
        self.Button_menu6.clicked.connect(self.add_to_cart('어묵', 1000))
        self.Button_menu7.clicked.connect(self.add_to_cart('콜라', 1500))
        self.Button_menu8.clicked.connect(self.add_to_cart('사이다', 1500))
        self.Total_Button.clicked.connect(self.calculate_total)
        self.Clear_Button.clicked.connect(self.clear_cart)
        self.Payment_Button.clicked.connect(self.open_payment_window)

    #소프트웨어 버튼 구조
    def add_to_cart(self, menu_name, price):
        """메뉴 아이템을 카트에 추가하는 핸들러 함수"""
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

    def calculate_total(self):
        """총 가격 계산 및 표시"""
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

    def clear_cart(self):
        """카트와 주문 목록 비우기"""
        self.findChild(QListWidget, 'CartList').clear()
        self.findChild(QListWidget, 'OrderList').clear()

    def open_payment_window(self):
        """결제 창 열기"""
        payment_window = SecondWindow()
        payment_window.exec()

    #하드웨어 버튼
    def payment_button_callback(self, channel):
        self.Payment_Button.click()

    def total_button_callback(self, channel):
        self.Total_Button_click()

    def clear_button_callback(self, channel):
        self.Clear_Button_click()

    # 키보드에서 넘어옴
    def focus_previous_menu_button(self, channel):
        self.focusNextChild()

    def focus_next_menu_button(self, channel):
        self.focusPreviousChild()

    def press_current_button(self, channel):
        """현재 포커스된 버튼을 클릭합니다."""
        focused_widget = self.focusWidget()
        if isinstance(focused_widget, QPushButton):
            focused_widget.click()

    def braille_output_button_callback(self, channel):
        focused_widget = self.focusWidget()
        if isinstance(focused_widget, QPushButton):
            menu_item = None
            if focused_widget == self.Button_menu1:
                menu_item = '김밥'
            elif focused_widget == self.Button_menu2:
                menu_item = '라면'
            elif focused_widget == self.Button_menu3:
                menu_item = '떡볶이'
            elif focused_widget == self.Button_menu4:
                menu_item = '순대'
            elif focused_widget == self.Button_menu5:
                menu_item = '튀김'
            elif focused_widget == self.Button_menu6:
                menu_item = '어묵'
            elif focused_widget == self.Button_menu7:
                menu_item = '콜라'
            elif focused_widget == self.Button_menu8:
                menu_item = '사이다'

            if menu_item:
                self.print_braille(menu_item)

    def print_braille(self, menu_item):
        """점자 출력"""
        braille_data = self.braille_menu[menu_item]

        for char in braille_data:
            for i, state in enumerate(char):
                pin = self.solenoid_pins[i]
                if self.current_solenoid_state[i] != state:  # 현재 솔레노이드 상태를 확인
                    GPIO.output(pin, GPIO.HIGH if state else GPIO.LOW)
                    self.current_solenoid_state[i] = state
            time.sleep(2)  # 각 글자 출력 후 2초 대기

        for pin in self.solenoid_pins:  # 출력 후 모든 솔레노이드를 LOW로 초기화
            GPIO.output(pin, GPIO.LOW)
            self.current_solenoid_state[i] = 0

    def set_button_styles(self):
        button_focus_style = """
        QPushButton:focus {
            background-color: #ADD8E6;  /* 포커스된 버튼의 배경색을 연한 파란색으로 지정 */
        }
        """

        # 모든 메뉴 버튼에 스타일 시트를 적용
        for button in self.menu_buttons:
            button.setStyleSheet(button_focus_style)


def cleanup_gpio():
    GPIO.cleanup()


class SecondWindow(QDialog, second_window_ui): # 최종 주문창 ui를 불러오는 클래스
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("주문 완료")


if __name__ == "__main__":
    # suppress_qt_warnings()
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)
    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    # 프로그램 화면을 보여주는 코드
    myWindow.show()
    app.aboutToQuit.connect(cleanup_gpio)
    sys.exit(app.exec_())

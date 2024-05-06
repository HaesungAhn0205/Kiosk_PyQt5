import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import RPi.GPIO as GPIO
import time
from os import environ

# UI 파일 로드
main_window_ui, _ = uic.loadUiType("Kiosk_draft.ui")
second_window_ui, _ = uic.loadUiType("Kiosk_final.ui")

#메인 윈도우 정의
class WindowClass(QMainWindow, main_window_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.menu = {'김밥': 2000, '라면': 4000, '떡볶이': 4000, '순대': 3000, '튀김': 4000, '어묵': 1000, '콜라': 1500, '사이다': 1500}

        BUTTON_PIN_payment = 17  # GPIO핀 설정
        BUTTON_PIN_total = 18
        BUTTON_PIN_clear = 22

        GPIO.setmode(GPIO.BCM)  # BCM 핀 넘버링
        GPIO.setup(BUTTON_PIN_payment, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 입력으로 설정, 내부 풀업 저항 사용
        GPIO.setup(BUTTON_PIN_total, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BUTTON_PIN_clear, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(BUTTON_PIN_payment, GPIO.FALLING, callback=self.payment_button_callback, bouncetime=3000) #스위치 버튼 콜백 등록
        GPIO.add_event_detect(BUTTON_PIN_total, GPIO.FALLING, callback=self.total_button_callback, bouncetime=3000)
        GPIO.add_event_detect(BUTTON_PIN_total, GPIO.FALLING, callback=self.clear_button_callback, bouncetime=3000)

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
        self.Total_button_Function()
    def clear_button_callback(self, channel):
        self.Clear_button_Function()


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
    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()

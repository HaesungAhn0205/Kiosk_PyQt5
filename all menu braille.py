import RPi.GPIO as GPIO
import socket
from time import sleep

# 데이터 핀 번호 리스트
data_pins = [17, 18, 27]
# 래치 핀 번호
latch_pin = 22
# 클럭 핀 번호
clock_pin = 23

# GPIO 핀 모드 설정
GPIO.setmode(GPIO.BCM)
for pin in data_pins:
    GPIO.setup(pin, GPIO.OUT)
GPIO.setup(latch_pin, GPIO.OUT)
GPIO.setup(clock_pin, GPIO.OUT)

def toggle_switch(pin, state):
    GPIO.output(pin, state)

def refresh():
    GPIO.output(latch_pin, 1)
    GPIO.output(latch_pin, 0)

# 각 음식에 대한 점자 데이터 정의
braille_menu = {
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


def print_braille_menu(menu):
    for character in braille_menu[menu]:
        for i in range(len(data_pins)):
            for row in character[i]:
                toggle_switch(data_pins[i], row)
        refresh()

def main():
    # 소켓 설정
    HOST = 'localhost'  # 서버 호스트
    PORT = 65432        # 포트(임의)

    # 소켓 생성
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 소켓 연결
        s.bind((HOST, PORT))
        s.listen()

        print("점자 출력 서버가 시작되었습니다.")

        while True:
            # 클라이언트 연결 수락
            conn, addr = s.accept()
            with conn:
                print(f"클라이언트 {addr}가 연결되었습니다.")
                while True:
                    # 클라이언트로부터 데이터 수신
                    data = conn.recv(1024)
                    if not data:
                        break
                    # 수신된 데이터를 문자열로 디코딩
                    selected_menus = data.decode().split(',')
                    print(f"클라이언트로부터 받은 메뉴: {selected_menus}")

                    # 선택된 메뉴들에 해당하는 점자 출력
                    for menu in selected_menus:
                        if menu in braille_menu:
                            print_braille_menu(menu)
                            sleep(0.5)  # 0.5초간 대기
                        else:
                            print(f"잘못된 입력 '{menu}'입니다. 해당 메뉴는 무시됩니다.")


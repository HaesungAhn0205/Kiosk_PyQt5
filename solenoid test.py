import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정
GPIO.setmode(GPIO.BCM)
SOLENOID_PIN = 17

# GPIO 핀 설정
GPIO.setup(SOLENOID_PIN, GPIO.OUT)

try:
    while True:
        # 솔레노이드 ON
        GPIO.output(SOLENOID_PIN, GPIO.HIGH)
        print("Solenoid ON")
        time.sleep(1)

        # 솔레노이드 OFF
        GPIO.output(SOLENOID_PIN, GPIO.LOW)
        print("Solenoid OFF")
        time.sleep(1)

except KeyboardInterrupt:
    # 사용자가 Ctrl+C로 프로그램을 종료할 때
    pass

finally:
    # GPIO 클린업
    GPIO.cleanup()

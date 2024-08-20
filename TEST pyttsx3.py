import pyttsx3

# 음성 출력을 위한 함수 정의
def play_voice_announcement(text):
    # pyttsx3 엔진 초기화
    engine = pyttsx3.init(driverName='espeak')

    # 속도와 볼륨 설정 (필요에 따라 조정 가능)
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)

    # 텍스트를 음성으로 변환 및 출력
    engine.say(text)

    # 음성 변환이 끝날 때까지 대기
    engine.runAndWait()

# 함수 사용 예시
play_voice_announcement("환영합니다.")

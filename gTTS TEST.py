from gtts import gTTS
import os
from playsound import playsound

# 한국어 텍스트 설정
text = "안녕하세요, 라즈베리 파이에서 gTTS를 사용하고 있습니다."

# TTS 생성 (한국어)
tts = gTTS(text=text, lang='ko')

# 음성 파일로 저장
tts.save("output.mp3")

# 음성 파일 재생 (playsound 사용)
playsound("output.mp3")

# 음성 파일 삭제 (선택사항)
os.remove("output.mp3")

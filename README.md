# 키오스크 점자 보조기 설계 및 제작 
### [cite_start]Design and Fabrication of Braille Assistant for Interactive Kiosk [cite: 4]

[cite_start]본 프로젝트는 편의시설 환경에서 급격히 보편화되고 있는 인터랙티브 키오스크(Interactive Kiosk)에서 소외되는 시각장애인의 디지털 접근성을 향상하기 위해 개발된 **'키오스크 점자 보조기'** 시스템입니다[cite: 43, 177]. [cite_start]파이썬(Python) 및 PyQt5 기반의 키오스크 프로그램과 라즈베리파이(Raspberry Pi)의 GPIO 제어를 결합하여, 시각장애인이 기존의 음성 안내뿐만 아니라 실시간 물리 점자 출력을 통해 키오스크를 직관적이고 독립적으로 조작할 수 있도록 지원합니다[cite: 28, 33, 178].

---

## 🛠️ 주요 기능 (Key Features)

* [cite_start]**초음파 센서 기반 자동 안내 (TTS)** [cite: 39]
  * [cite_start]사용자가 키오스크 전방 50cm 이내로 접근하면 초음파 센서가 이를 감지합니다[cite: 88].
  * [cite_start]외부 스피커(Aux 연결)를 통해 기기 구성 및 하드웨어 버튼 조작 방법에 대한 안내 음성을 자동으로 출력합니다[cite: 98, 99].
* [cite_start]**물리 스위치 버튼 인터페이스** [cite: 108]
  * [cite_start]터치스크린 조작이 어려운 시각장애인을 위해 총 7개의 하드웨어 스위치 버튼을 배치하여 명확하고 직관적인 입력을 지원합니다[cite: 65, 74].
* [cite_start]**실시간 18구 하드웨어 점자 표시** [cite: 30, 72]
  * [cite_start]총 18개의 솔레노이드 액츄에이터를 병렬 제어하여 메뉴 이름을 실시간 점자 데이터로 표현합니다[cite: 72, 101].
  * [cite_start]각 글자는 사용자의 가독성을 고려해 2초 동안 출력된 후 다음 글자로 전환되며, 출력이 종료되면 모든 모터가 자동으로 초기화됩니다[cite: 105].

---

## 🔌 하드웨어 사양 및 아키텍처 (Hardware Architecture)

[cite_start]점자 보조기 시스템의 하드웨어 회로는 라즈베리파이를 중심으로 병렬 입력 및 전원 분리형 구동 회로로 구성되어 있습니다[cite: 179, 180].

* [cite_start]**메인 제어 장치:** Raspberry Pi 3B+ [cite: 71]
* [cite_start]**점자 구동 모터:** 솔레노이드 액츄에이터 (DS-0420S) 18개 [cite: 72]
* [cite_start]**센서 및 전동 제어:** * 초음파 센서 (HC-SR04) [cite: 75]
  * [cite_start]릴레이 모듈 (라즈베리파이 신호로 외부 고전류 전원을 온/오프 제어) [cite: 114, 180]
  * [cite_start]단자대 (Terminal Block)를 통한 배선 효율화 [cite: 128]
* [cite_start]**회로 보호 장치:** 솔레노이드의 인덕턴스 특성에 따른 플라이백(Flyback) 고전압 현상을 방지하고, 라즈베리파이 및 시스템 오작동을 차단하기 위해 솔레노이드 양단에 역방향 다이오드 연결 [cite: 102]
* [cite_start]**구동 전원:** 18개 모터의 동시 작동 전류를 안정적으로 공급하기 위해 외장형 DC 어댑터 (입력 AC 220V / 출력 DC 12V 10A) 배치 [cite: 101, 107]
* [cite_start]**기구물 외관 케이스:** 3D 프린팅 기법으로 정밀 설계된 백색 상판과 직접 가공한 백색 아크릴 판(측면, 하판, 내부 거치대)의 조합으로 구동축 간섭 최소화 및 내부 회로 보호 [cite: 137, 138, 186, 187]

### 📌 하드웨어 핀 매핑 (Pin Mapping)

| 구분 | 컴포넌트 기능 | BCM 핀 번호 | 물리적 연결 형태 및 사양 |
| :--- | :--- | :--- | :--- |
| **센서** | 초음파 센서 Trigger | `GPIO 1` | [cite_start]초음파 송신 신호 출력 [cite: 522] |
| | 초음파 센서 Echo | `GPIO 0` | [cite_start]전압 분배 회로(Voltage Divider) 거쳐 입력 [cite: 206, 523] |
| **버튼 (입력)** | 이전 메뉴 탐색 (Prev) | `GPIO 22` | [cite_start]내부 풀업 저항(Pull-Up) 사용, Falling Edge 감지 [cite: 588, 596] |
| | 다음 메뉴 탐색 (Next) | `GPIO 27` | [cite_start]내부 풀업 저항(Pull-Up) 사용, Falling Edge 감지 [cite: 588, 596] |
| | 메뉴 장바구니 추가 (Press) | `GPIO 17` | [cite_start]내부 풀업 저항(Pull-Up) 사용, Falling Edge 감지 [cite: 588, 596] |
| | 점자 출력 실행 (Braille) | `GPIO 4` | [cite_start]내부 풀업 저항(Pull-Up) 사용, Falling Edge 감지 [cite: 588, 596] |
| | 장바구니 합산 (Total) | `GPIO 18` | [cite_start]내부 풀업 저항(Pull-Up) 사용, Falling Edge 감지 [cite: 588, 597] |
| | 장바구니 초기화 (Clear) | `GPIO 15` | [cite_start]내부 풀업 저항(Pull-Up) 사용, Falling Edge 감지 [cite: 588, 598] |
| | 최종 결제/주문 (Payment) | `GPIO 14` | [cite_start]내부 풀업 저항(Pull-Up) 사용, Falling Edge 감지 [cite: 589, 596] |
| **모터 (출력)** | 솔레노이드 핀 (총 18개) | `26, 19, 13, 6, 5, 11, 9, 10, 21, 20, 16, 12, 7, 8, 25, 24, 3, 2` | [cite_start]릴레이 모듈 단자와 1:1 매핑되어 HIGH/LOW 제어 [cite: 592, 602] |

---

## 💻 소프트웨어 구조 (Software Architecture)

### 1. 디렉토리 구조
```text
├── .idea/                      # 개발 환경 설정 데이터
├── Kiosk_draft.ui              # Qt Designer로 구현한 키오스크 메인 화면 디자인
├── Kiosk_final.ui              # 최종 주문 완료 팝업 다이얼로그 디자인
├── main.py                     # GUI 이벤트 바인딩 및 RPi.GPIO 통합 제어 애플리케이션
└── all menu braille.py         # 독립 실행형 점자 제어 및 소켓(Socket) 통신 서버 로직

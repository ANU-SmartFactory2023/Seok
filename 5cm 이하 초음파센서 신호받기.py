import RPi.GPIO as GPIO
import time
import json
import requests

class TestModel:
    def __init__(self):
        self.name = ""
        self.password = ""

# GPIO 핀 번호 설정
TRIG_PIN = 23
ECHO_PIN = 24

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)

# GPIO 핀 설정
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# 이전 데이터 전송 여부를 추적하는 변수
data_sent = False

def get_distance():
    # 초음파 신호 발생
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    # 초음파 신호 수신 시간 측정
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    # 초음파의 이동 시간 계산
    pulse_duration = pulse_end - pulse_start

    # 거리 계산 (소리의 속도 = 343m/s, 거리 = 시간 * 속도 / 2)
    distance = pulse_duration * 34300 / 2

    return distance

try:
    # 무한 반복하면서 거리 측정
    while True:
        distance = get_distance()
        print(f"거리: {distance:.2f} cm")

        # 거리가 5cm 이하이고 이전에 데이터를 전송하지 않았을 때
        if distance <= 5 and not data_sent:
            test_model = TestModel()
            test_model.name = "test"
            test_model.password = "1234"

            params = json.dumps(test_model.__dict__)
            headers = {"Content-type": "application/json", "Accept": "*/*"}

            response = requests.post('http://192.168.111.145:5000/api/values/value3', data=params, headers=headers)
            response.raise_for_status()
            print("응답:", response.text)

            # 데이터를 전송했음을 표시
            data_sent = True

        # 거리가 5cm 이상이고 이전에 데이터를 전송했을 때
        elif distance > 5 and data_sent:
            # 데이터를 다시 전송할 수 있도록 초기화
            data_sent = False

        time.sleep(1)  # 1초 대기

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()  # GPIO 설정 초기화

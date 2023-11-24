import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

RELAY_PIN = 17  # 릴레이 모듈을 제어하는 GPIO 핀
SERVO_PIN = 18  # 서보 모터를 제어하는 GPIO 핀

GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.setup(SERVO_PIN, GPIO.OUT)
 # GPIO 18 핀에 PWM 설정
pwm = GPIO.PWM(SERVO_PIN, 50)  # 주파수 50Hz 설정

try:
    # GPIO 17 핀에 HIGH 신호 출력 (릴레이 모듈에 전원 공급)
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    time.sleep(3)  # 3초 동안 대기

    pwm.start(2.5)  # 초기 위치는 2.5%의 듀티 사이클 (0도)

    # 180도 회전을 위해 듀티 사이클을 7.5%로 변경
    pwm.ChangeDutyCycle(7.5)
    time.sleep(1)  # 동작 지속 시간 (조절 가능)

    # 초기 위치로 복귀하는 듀티 사이클 설정 (0도)
    pwm.ChangeDutyCycle(2.5)
    time.sleep(1)  # 동작 지속 시간 (조절 가능)

    # PWM 정지
    pwm.stop()

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()

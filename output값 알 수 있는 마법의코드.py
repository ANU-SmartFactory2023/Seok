import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

SERVO_PIN = 21  # 서보 모터를 제어하는 GPIO 핀

GPIO.setup(SERVO_PIN, GPIO.IN)

try:
    while True:
        input_value = GPIO.input(SERVO_PIN)
        print(f"GPIO {SERVO_PIN} 핀의 입력 값: {input_value}")
        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()

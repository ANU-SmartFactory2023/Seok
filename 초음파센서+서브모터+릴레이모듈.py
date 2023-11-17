from __future__ import print_function
import time
import RPi.GPIO as GPIO

def measure():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start_time = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        end_time = time.time()

    pulse_duration = end_time - start_time
    distance = (pulse_duration * 34300) / 2  # 거리를 센티미터로 계산

    return distance

def measure_average():
    distance1 = measure()
    time.sleep(0.1)
    distance2 = measure()
    time.sleep(0.1)
    distance3 = measure()
    distance = distance1 + distance2 + distance3
    distance = distance / 3
    return distance

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 23
GPIO_ECHO = 24
servo = 18
relay_pin = 21

print("Ultrasonic Measurement")

GPIO.setup(servo, GPIO.OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(relay_pin, GPIO.OUT)

GPIO.output(GPIO_TRIGGER, False)

p = GPIO.PWM(servo, 50)
p.start(2.5)

try:
    while True:
        distance = measure_average()
        print("Distance: %.1f cm" % distance)  # 거리를 센티미터로 출력

        # 거리에 따라 서보 모터와 릴레이 동작
        if distance <= 10:
            p.ChangeDutyCycle(7.5)  # 서보 모터 동작
            GPIO.output(relay_pin, GPIO.HIGH)  # 릴레이 켜기
            time.sleep(1 + (10 - distance) * 0.1)  # 릴레이 켜진 상태를 유지하는 시간
            p.ChangeDutyCycle(2.5)
            GPIO.output(relay_pin, GPIO.LOW)  # 릴레이 끄기

        time.sleep(1)

except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()

#main.py
import RPi.GPIO as GPIO
import time
import logging
from ultrasonic2 import UltrasonicSensor
# from lightsensor import LightSensor
# from ir_sensor import InfraredSensor
# from relay2 import RelayModule

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)

class Sensor:
    # 초음파 센서, 조도 센서, 적외선 센서, 릴레이 모듈 객체 생성
    __ultrasonic_sensor = UltrasonicSensor(trig_pin=23, echo_pin=24)
    # __light_sensor = LightSensor(sensor_pin=25)
    # __ir_sensor = InfraredSensor(ir_pin=22)  # 실제 핀 번호로 변경
    # __relay_module = RelayModule(relay_pin=18)

    # def get_light_sensor(self):
    #     return self.__light_sensor.measure_light()

    def get_ultra_sensor( self ) :
        return self.__ultrasonic_sensor.measure_distance()  
    
    # def get_ir_sensor(self) :
    #     return self.__ir_sensor.measure_ir()
    
    # def get_relay_sensor(self) : 
    #     return self.__relay_module

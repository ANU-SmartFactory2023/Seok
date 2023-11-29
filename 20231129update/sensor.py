import time
import logging
from ultrasonic2 import UltrasonicSensor
from lightsensor import LightSensor
from ir_sensor import InfraredSensor
from relay2 import RelayModule
from photo import ImageCV
import RPi.GPIO as GPIO

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Sensor:
    def __init__(self):
        # 초음파 센서, 조도 센서, 적외선 센서, 릴레이 모듈 객체 생성
        try:
            self.__ultrasonic_sensor = UltrasonicSensor(trig_pin=23, echo_pin=24)
            self.__light_sensor = LightSensor(sensor_pin=25)
            self.__ir_sensor = InfraredSensor(ir_pin=22)  # 실제 핀 번호로 변경
            self.__relay_module = RelayModule(relay_pin=18)
            self.__photo_sensor = ImageCV()  # 웹캠 객체 생성
        except Exception as e:
            print(f"센서 초기화 중 예상치 못한 오류: {e}")

    def get_relay_sensor(self):
        if self.__relay_module:
            return self.__relay_module
        else:
            print("릴레이 모듈이 초기화되지 않았습니다.")
            return None
    
    def initialize(self):
        # 센서 초기화
        self.__ultrasonic_sensor.initialize()
        self.__light_sensor.initialize()
        self.__ir_sensor.initialize()
        self.__relay_module.initialize()

    def cleanup_gpio(self):
        # GPIO 정리
        GPIO.setmode(GPIO.BCM) #BCM모드로 설정
        self.__ultrasonic_sensor.cleanup_gpio()
        self.__light_sensor.cleanup_gpio()
        self.__ir_sensor.cleanup_gpio()
        self.__relay_module.cleanup_gpio()
        # 웹캠의 경우 cleanup 메서드가 없는 경우도 있으므로 주의 필요

    def get_light_sensor(self):
        return self.__light_sensor.measure_light()

    def get_ultra_sensor( self ) :
        return self.__ultrasonic_sensor.measure_distance()  
    
    def get_ir_sensor(self) :
        return self.__ir_sensor.measure_ir()
    
    def get_relay_sensor(self) :
        return self.__relay_module
    
    def get_photo_sensor(self) :
        return self.__photo_sensor.count_black_pixels()
    

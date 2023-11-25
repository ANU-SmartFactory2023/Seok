from sensor import Sensor
import logging
import time

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sensor 클래스 초기화
sensor = Sensor()


try:
    while True:
        try:
            # 각 센서 값 가져오기
            # light_level = sensor.get_light_sensor()
            distance = sensor.get_ultra_sensor()
            # ir_value = sensor.get_ir_sensor()
            # relay_module = sensor.get_relay_sensor()

            # 로깅
            # logger.info(f"빛의 강도: {light_level}")
            logger.info(f"거리: {distance} cm")
            # logger.info(f"적외선 센서 값: {ir_value}")

            # 거리가 5cm 이하이면 릴레이 모듈 작동
            if distance and distance <= 5:
                # relay_module.turn_on_relay()
                logger.info("릴레이 켜짐")
            else:
                # relay_module.turn_off_relay()
                logger.info("릴레이 꺼짐")

            time.sleep(1)

        except Exception as e:
            logger.exception(f"예상치 못한 오류가 발생했습니다: {e}")

except KeyboardInterrupt:
    logger.info("사용자에 의해 종료")

# finally:
    # # GPIO 정리
    # sensor.measure_relay().cleanup_gpio()

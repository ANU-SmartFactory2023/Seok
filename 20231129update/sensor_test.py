from sensor import Sensor
import logging
import time

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Sensor class
sensor = Sensor()

try:
    while True:
        # Get values from each sensor
        light_intensity = sensor.get_light_sensor()
        distance = sensor.get_ultra_sensor()
        ir_value = sensor.get_ir_sensor()
        relay_module = sensor.get_relay_sensor()
        black_pixel = sensor.get_photo_sensor()

        # Logging
        logger.info(f"Light Intensity: {light_intensity}")
        logger.info(f"Distance: {distance} cm")
        logger.info(f"Infrared Sensor Value: {ir_value}")
        logger.info(f"Webcam Black Pixel Count: {black_pixel}")

        # Turn on the relay module if the distance is less than or equal to 5cm
        if distance and distance <= 5:
            relay_module.turn_on_relay()
            logger.info("Relay turned on")
        else:
            relay_module.turn_off_relay()
            logger.info("Relay turned off")

        time.sleep(1)

except KeyboardInterrupt:
    logger.info("Terminated by the user")

except Exception as e:  
    logger.exception(f"An unexpected error occurred: {e}")

finally:
    # Clean up GPIO
    sensor.cleanup_gpio()

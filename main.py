import logging
import time

import RPi.GPIO as GPIO

from configs import LED_PIN
from configs import WEIGHT_SENSOR_DOUT
from configs import WEIGHT_SENSOR_PD_SCK
from devices import LED
from devices import WeightSensor
from greengrass import BottleShadow
from greengrass import BottleStreamManagerClient
from smart_bottle import SmartBottle

# Configure logging
# logger = logging.getLogger("AWSIoTPythonSDK.core")
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # set to logging.DEBUG for additional logging
streamHandler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Configure Device
GPIO.setmode(GPIO.BOARD)
weight_sensor = WeightSensor(WEIGHT_SENSOR_DOUT, WEIGHT_SENSOR_PD_SCK)
# led = LED(Configs.LED_PIN)
led = LED(LED_PIN)

# Shadow Service
bottle_shadow = BottleShadow()

# Stream Service
bottle_stream = BottleStreamManagerClient()

# Configure Smart Bottle
smart_bottle = SmartBottle(led, weight_sensor)
smart_bottle.configure_shadow_handler(bottle_shadow)
smart_bottle.configure_stream_manager_handler(bottle_stream)
smart_bottle.enable_auto_sync(True)


smart_bottle.start()
# print(smart_bottle._find_next_alarm_time())
# while True:
#     try:
        # smart_bottle.weigh()
        # time.sleep(2)

    # except (KeyboardInterrupt, SystemExit):
    #     GPIO.cleanup()

import asyncio
import logging

from datetime import time, timedelta, date, datetime


class SmartBottle(object):
    _logger = logging.getLogger(__name__)

    # def __init__(self, led, weight_sensor):
    # TODO try dependency injection way to import weight sensor and led
    # def __init__(self, weight_dout, weight_pd_sck, led_pin):
    #     # TODO switch weight_sensor to GPIOzero device to avoid GPIO management
    #     self.weight_sensor = HX711(weight_dout, weight_pd_sck)
    #
    #     self.weight_sensor.set_reading_format("MSB", "MSB")
    #     self.weight_sensor.set_reference_unit(Configs.WEIGHT_SENSOR_REFERENCE_UNIT)
    #     self.weight_sensor.reset()
    #     self.weight_sensor.tare()
    #
    #     # TODO handle GPIO setting,since HX711 has modified GPIO setting too.
    #     # GPIO.setwarnings(False)
    #     GPIO.setmode(GPIO.BOARD)
    #     GPIO.setup(self.led_pin, GPIO.OUT, initial=GPIO.LOW)
    #
    #     self._shadow_handler = None
    #     self._stream_manager_handler = None
    #     self._auto_sync = False

    def __init__(self, led, weight_sensor):
        self._led = led
        self._weight_sensor = weight_sensor

        self._shadow_handler = None
        self._stream_manager_handler = None
        self._auto_sync = False

        self.weight = 0
        self.type = "water"
        self.schedule = {}
        self.bottle_size = 1000  # 1000 ml
        self.quantity_of_daily_water = 2000

        ## TODO should load schedule from the cloud shadow.
        self.set_schedule()
        self.loop = asyncio.get_event_loop()

    def led_on(self):
        self._led.on()

    def led_off(self):
        self._led.off()

    def weigh(self):
        self.weight = self._weight_sensor.weigh()

        self._logger.info("The newest weight is {}".format(self.weight))
        if self._auto_sync:
            self._sync_to_shadow()
            self._sync_to_stream()
        return self.weight

    def _sync_to_shadow(self):
        self._shadow_handler.set_water_in_the_bottle(self.weight)

    def _sync_to_stream(self):
        self._stream_manager_handler.append_state(self.weight, self.type)

    def set_bottle_size(self, size):
        self.bottle_size = size

    def set_quantity_of_daily_water(self, target):
        self.quantity_of_daily_water = target

    def set_schedule(self, beginning=time(hour=9), end=time(hour=21), interval=timedelta(minutes=45)):
        def add_delta_to_time(time, delta):
            return (datetime.combine(date.min, time) + delta).time()

        duration = datetime.combine(date.min, end) - datetime.combine(date.min, beginning)
        times = int(duration / interval)
        quantity_of_each_time = int(self.quantity_of_daily_water / times)

        for i in range(0, times):
            self.schedule[add_delta_to_time(beginning, i * interval).isoformat()] = quantity_of_each_time

    def flash(self, text):
        pass

    def _find_next_alarm_time(self):
        current_datetime = datetime.now()
        time_sheet = sorted(self.schedule)
        # self._logger.info(time_sheet)

        for i, t in enumerate(time_sheet):
            if current_datetime.time().isoformat() <= t:
                next_alert_datetime = datetime.combine(current_datetime.date(), time.fromisoformat(t))
                return next_alert_datetime

        # If we have no more alarm today, return tomorrow first alarm
        tomorrow_date = current_datetime.date() + timedelta(days=1)
        tomorrow_first_alert_datetime = datetime.combine((tomorrow_date, time.fromisoformat(time_sheet[0])))
        return tomorrow_first_alert_datetime

    async def periodic_alert(self):
        while True:
            next_alert_time = self._find_next_alarm_time()
            self._logger.info("The next alarm will be {}".format(next_alert_time))
            next_alert_remaining_time_in_second = (datetime.now() - next_alert_time).seconds
            await asyncio.sleep(next_alert_remaining_time_in_second)
            self._logger.info("Hey drink more water")

    async def periodic_weigh(self):
        while True:
            await asyncio.sleep(2)
            self.weigh()

    def start(self):
        cors = asyncio.wait([self.periodic_alert(), self.periodic_weigh()])
        self.loop.run_until_complete(cors)

    def drink_water(self):
        pass

    def add_alarm(self):
        pass

    def remove_alarm(self):
        pass

    def configure_shadow_handler(self, handler):
        self._logger.info("Configuring shadow service...")
        self._shadow_handler = handler

    # def _shadow_update(self, weight):
    #
    #     self._shadow_handler.
    #     JSON_payload = {
    #         "state": {
    #             "desired": {
    #                 "weight": weight
    #             }
    #         }
    #     }
    #
    #     def shadow_update_callback(payload, response_status, token):
    #         if response_status == "timeout":
    #             self._logger.info("Shadow update request" + token + " time out!")
    #         if response_status == "accepted":
    #             payload_dict = json.loads(payload)
    #             self._logger.info("Update request with token: " + token + " accepted")
    #             self._logger.info("property: " + str(payload_dict["state"]["desired"]["weight"]))
    #         if response_status == "rejected":
    #             self._logger.info("Shadow update request" + token + " rejected!")
    #
    #     self._shadow_handler.shadowUpdate(json.dumps(JSON_payload), shadow_update_callback, 5)

    def enable_auto_sync(self, enable=True):
        if self._shadow_handler == None or self._stream_manager_handler == None:
            raise AttributeError("Miss shadow handler or stream manager handler")
        self._auto_sync = enable

    def configure_stream_manager_handler(self, handler):
        self._logger.info("Configuring Stream Manager service...")
        self._stream_manager_handler = handler

    # def _stream_update(self, weight):
    #     payload = {
    #         "weight": weight
    #     }
    #     try:
    #         # sequence_number = self._stream_manager_handler.append_message(stream_name="Data",
    #         #                                                               data=b'Arbitrary bytes data')
    #         self._stream_manager_handler.append_message("SomeStream", json.dumps(payload).encode("utf-8"))
    #         self._logger.info("append the data", payload)
    #     except StreamManagerException as e:
    #         pass
    #         # Properly handle errors.
    #     except ConnectionError or asyncio.TimeoutError:
    #         pass
    #         # Properly handle errors.

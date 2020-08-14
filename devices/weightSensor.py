import RPi.GPIO as GPIO

from devices.hx711 import HX711


class WeightSensor(object):
    def __init__(self, dout, pd_sck, mode=GPIO.BOARD, reference_unit=427):
        self._hx711 = HX711(dout, pd_sck, mode)
        self._hx711.set_reading_format("MSB", "MSB")
        self._hx711.set_reference_unit(reference_unit)

        self.reset()
        self.tare()

    def reset(self):
        self._hx711.reset()

    def weigh(self):
        return max(0, int(self._hx711.get_weight(5)))

    def tare(self):
        self._hx711.tare()






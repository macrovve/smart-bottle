import RPi.GPIO as GPIO


class LED(object):
    def __init__(self, pin):
        self._pin = pin
        GPIO.setup(self._pin, GPIO.OUT, initial=GPIO.LOW)

    def on(self):
        GPIO.output(self._pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self._pin, GPIO.LOW)


    # TODO
    def clean(self):
        pass

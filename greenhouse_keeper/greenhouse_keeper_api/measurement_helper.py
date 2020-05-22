class Measurement_helper():

    def __init__(self, data):
        self.temperature = self.temperature_validator(data)
        self.humidity = self.humidity_validator(data)
        self.pressure = self.pressure_validator(data)
        self.message = self.message_generator(data)

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, data):
        self._temperature = self.temperature_validator(data)

    @property
    def humidity(self):
        return self._humidity

    @humidity.setter
    def humidity(self, data):
        self._humidity = self.humidity_validator(data)

    @property
    def pressure(self):
        return self._pressure

    @pressure.setter
    def pressure(self, data):
        self._pressure = self.pressure_validator(data)

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, data):
        self._message = message_generator(data)

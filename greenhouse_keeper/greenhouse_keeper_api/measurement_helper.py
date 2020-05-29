import json
from pprint import pprint
from datetime import datetime, time


class MeasurementHelper():
    """ MeasurementHelper() accepts data of type dictionary. Must contain temperature, humidity and pressure. """
    def __init__(self, data):
        self._is_night = self.isNight()
        self._max_temperature = 20 if self.is_night else 30
        self._min_temperature = 15 if self.is_night else 20
        self._max_humidity = 90
        self._min_humidity = 20
        self._max_pressure = 1100
        self._min_pressure = 900
        self._data = self.validateType(data, dict)
        self._temperature = self.temperatureValidator()
        self._humidity = self.humidityValidator()
        self._pressure = self.pressureValidator()
        self._message = self.messageGenerator()


    @property
    def max_temperature(self):
        return self._max_temperature

    @max_temperature.setter
    def max_temperature(self, temp):
        self.validateType(temp)
        self._max_temperature = self.validateMinMax(temp, -20, 60)

    @property
    def min_temperature(self):
        return self._min_temperature

    @min_temperature.setter
    def min_temperature(self, temp):
        self.validateType(temp)
        self._min_temperature = self.validateMinMax(temp, -20, 60)

    @property
    def max_humidity(self):
        return self._max_humidity

    @max_humidity.setter
    def max_humidity(self, humi):
        self.validateType(humi)
        self._max_humidity = self.validateMinMax(humi, 0, 100)

    @property
    def min_humidity(self):
        return self._min_humidity

    @min_humidity.setter
    def min_humidity(self, humi):
        self.validateType(humi)
        self._min_humidity = self.validateMinMax(humi, 0, 100)

    @property
    def max_pressure(self):
        return self._max_pressure

    @max_pressure.setter
    def max_pressure(self, pres):
        self.validateType(pres)
        self._max_pressure = self.validateMinMax(pres, 0, 2000)

    @property
    def min_pressure(self):
        return self._min_pressure

    @min_pressure.setter
    def min_pressure(self, pres):
        self.validateType(pres)
        self._min_pressure = self.validateMinMax(pres, 0, 2000)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._temperature = self.validateType(data, dict)

    @property
    def temperature(self):
        return self.getMeasureResult(
            self._temperature, max_limit=self.max_temperature, min_limit=self.min_temperature)

    @temperature.setter
    def temperature(self, temp):
        self._temperature = self.validateType(temp)

    @property
    def humidity(self):
        return self.getMeasureResult(
            self._humidity, max_limit=self.max_humidity, min_limit=self.min_humidity)

    @humidity.setter
    def humidity(self, humi):
        self._humidity = self.validateType(humi)

    @property
    def pressure(self):
        return self.getMeasureResult(
            self._pressure, max_limit=self.max_pressure, min_limit=self.min_pressure)

    @pressure.setter
    def pressure(self, pres):
        self._pressure = self.validateType(pres)

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message):
        self._message = self.validateType(message, str)

    @property
    def is_night(self):
        return self._is_night

    @is_night.setter
    def is_night(self, is_night):
        self._is_night = self.validateType(is_night, bool)

    def messageGenerator(self):
        """ Returns a string message based on the measurement sum. """
        sum = self.getMeasurementSum()
        message = self.generateMessage(sum)
        return message

    def temperatureValidator(self):
        """ Validates the temperature from 'data dictionary' and validates that the temperature is within bondaries. Returns the temperature. """
        temp = self.getFloatValueFromDataDict('temperature')
        return self.validateMinMax(temp, -20, 60)

    def humidityValidator(self):
        """ Validates the humidity from 'data dictionary' and validates that the humidity is within bondaries. Returns the humidity. """
        humi = self.getFloatValueFromDataDict('humidity')
        return self.validateMinMax(humi, 0, 100)

    def pressureValidator(self):
        """ Validates the pressure from 'data dictionary' and validates that the pressure is within bondaries. Returns the pressure. """
        pres = self.getFloatValueFromDataDict('pressure')
        return self.validateMinMax(pres, 0, 2000)

    def getFloatValueFromDataDict(self, key):
        """ Validates the that the 'data' parsed to the constructor is of type dictionary. Validates the parsed 'key' is of type string. Returns tha validated value to the corrosponding key of the data dictionary.  """
        data = self.validateType(self.data, types=dict)
        key = self.validateType(key, str)
        float_val = data[key]
        return self.validateType(float_val)

    def getMeasureResult(self, value, max_limit=60, min_limit=20):
        """ Validates type of all parsed values. Returns a string as result of the parsed 'value's size. """
        for val in (value, max_limit, min_limit):
            self.validateType(val)
        
        if value > max_limit:
            result = 'High'
        elif value < min_limit:
            result = 'Low'
        else:
            result = 'Ok'
        return result

    def getData(self):
        """ Returns a dictionary with temperature, humidity, pressure, sum and message. """
        return {
            'temperature': self.temperature,
            'humidity': self.humidity,
            'pressure': self.pressure,
            'sum': self.getMeasurementSum(),
            'message': self.message
        }

    def getMeasurementSum(self):
        """ Calculated the measurement sum. Returns the sum. """
        # 5 - 3 and -1 corropsonds to how important the values is weighted.
        high, low, ok = 3, 2, 1
        sum = 0

        temp, humi, pres = self._temperature, self._humidity, self._pressure

        if temp > self.max_temperature:
            sum += high * 5
        elif temp < self.min_temperature:
            sum += low * 5
        else:
            sum += ok * 5
        if humi > self.max_humidity:
            sum += high * 3
        elif humi < self.min_humidity:
            sum += low * 3
        else:
            sum += ok * 3
        if pres > self.max_pressure:
            sum += high * -1
        elif pres < self.min_pressure:
            sum += low * -1
        else:
            sum += ok * -1

        return sum

    def isNight(self):
        """ Returns true if local datetime is night, else returns true. """
        now = datetime.now()
        now_time = now.time()
        morning = time(6, 00)
        evening = time(18, 00)
        
        if now_time > evening or now_time < morning:
            return True
        
        return False

    def generateMessage(self, sum):
        """ Returns a message based on the given 'sum'. """
        if sum < 10:
            message = "Close window, no need to water."
        elif sum < 15:
            message = "Close window, water the plants."
        elif sum < 20:
            message = "Open window, no need to water."
        else:
            message = "Open window, water the plants."
        return message

    def validateMinMax(self, value, min_value, max_value):
        """ Validates the parsed 'value' is within the parsed 'min_value' and 'max_value'. Returns validated value or raises ValueError. """
        for val in (value, min_value, max_value):
            self.validateType(val)
        if not (value >= min_value and value <= max_value):
            raise ValueError(
                f'value should be between {min_value} and {max_value}, {value} given')
        return value

    def validateType(self, value, types=(int, float)):
        """ Validates the parsed 'value' is of parsed 'types'. Returns value or raises TypeError. """
        if not isinstance(value, types):
            raise TypeError(
                f'value should be of type {types}, {type(value)} given')
        return value
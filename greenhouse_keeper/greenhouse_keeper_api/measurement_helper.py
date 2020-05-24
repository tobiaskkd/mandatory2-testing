import json
from pprint import pprint

class Measurement_helper():

    def __init__(self, data):
        self.temperature = self.temperature_validator(data)
        self.humidity = self.humidity_validator(data)
        self.pressure = self.pressure_validator(data)
        self.message = self.message_generator()
    
    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, temp):
        if not isinstance(temp, (float, int)):
            raise TypeError(f'value should be of type {float}, {type(temp)} given')
        self._temperature = temp

    @property
    def humidity(self):
        return self._humidity

    @humidity.setter
    def humidity(self, humi):
        if not isinstance(humi, (float, int)):
            raise TypeError(f'value should be of type {float}, {type(humi)} given')
        self._humidity = humi

    @property
    def pressure(self):
        return self._pressure

    @pressure.setter
    def pressure(self, pres):
        if not isinstance(pres, (float, int)):
            raise TypeError(f'value should be of type {float}, {type(pres)} given')
        self._pressure = pres

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message):
        if not isinstance(message, (str)):
            raise TypeError(f'value should be of type {str}, {type(message)} given')
        self._message = message

    def message_generator(self):
        temp = f'Temperature {self.temperature}\n' if self.temperature else ''
        humi = f'Pressure {self.humidity}\n' if self.humidity else ''
        pres = f'Temperature {self.pressure}\n' if self.pressure else ''
        message = ''.join((temp,humi,pres))
        return message if len(message) > 0 else 'Everything is fine'

    def temperature_validator(self, data):
        temp = self.get_float_value_from_dict(data, 'temperature')
        result = self.get_measure_result(temp, max_limit=50, min_limit=25)
        return result

    def humidity_validator(self, data):
        humi = self.get_float_value_from_dict(data, 'humidity')
        result = self.get_measure_result(humi, max_limit=50, min_limit=25)
        return result

    def pressure_validator(self, data):
        pres = self.get_float_value_from_dict(data, 'pressure')
        result = self.get_measure_result(pres, max_limit=50, min_limit=25)
        return result

    def get_float_value_from_dict(self, data, key):
        if not isinstance(data, dict):
            raise TypeError(f'data should be of type {dict}, {type(data)} given')
        if not isinstance(key, str):
            raise TypeError(f'key should be of type {str}, {type(key)} given')
        float_val = data[key]
        if not isinstance(float_val, (float, int)):
            raise TypeError(f'value should be of type {float}, {type(float_val)} given')
        return float_val
    
    def get_measure_result(self, value, max_limit=60, min_limit=20):
        if not isinstance(value, (float, int)):
            raise TypeError(f'value should be of type {float} or {int}, {type(value)} given')
        if not isinstance(max_limit, (float, int)):
            raise TypeError(f'value should be of type {float} or {int}, {type(max_limit)} given')
        if not isinstance(min_limit, (float, int)):
            raise TypeError(f'value should be of type {float} or {int}, {type(min_limit)} given')
        if value > max_limit:
            result = 'Too high'
        elif value < min_limit:
            result = 'Too low'
        else:
            result = False
        return result

    def get_data(self):
        return self.__dict__
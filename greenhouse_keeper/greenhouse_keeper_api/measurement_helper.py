import json
from pprint import pprint
from datetime import datetime, time


class Measurement_helper():

    def __init__(self, data):
        self._is_night = self.is_night()
        self._max_temperature = 30 if self.is_night else 20
        self._min_temperature = 20 if self.is_night else 15
        self._max_humidity = 90
        self._min_humidity = 20
        self._max_pressure = 1100
        self._min_pressure = 900
        self._data = self.validate_type(data, dict)
        self._temperature = self.temperature_validator()
        self._humidity = self.humidity_validator()
        self._pressure = self.pressure_validator()
        self._message = self.message_generator()


    @property
    def max_temperature(self):
        return self._max_temperature

    @max_temperature.setter
    def max_temperature(self, temp):
        self.validate_type(temp)
        self._max_temperature = self.validate_min_max(temp, -20, 60)

    @property
    def min_temperature(self):
        return self._min_temperature

    @min_temperature.setter
    def max_temperature(self, temp):
        self.validate_type(temp)
        self._min_temperature = self.validate_min_max(temp, -20, 60)

    @property
    def max_humidity(self):
        return self._max_humidity

    @max_humidity.setter
    def max_humidity(self, humi):
        self.validate_type(humi)
        self._max_humidity = self.validate_min_max(humi, 0, 100)

    @property
    def min_humidity(self):
        return self._min_humidity

    @min_humidity.setter
    def min_humidity(self, humi):
        self.validate_type(humi)
        self._min_humidity = self.validate_min_max(humi, 0, 100)

    @property
    def max_pressure(self):
        return self._max_pressure

    @max_pressure.setter
    def max_pressure(self, pres):
        self.validate_type(pres)
        self._max_pressure = self.validate_min_max(pres, 0, 2000)

    @property
    def min_pressure(self):
        return self._min_pressure

    @min_pressure.setter
    def min_pressure(self, pres):
        self.validate_type(pres)
        self._min_pressure = self.validate_min_max(pres, 0, 2000)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._temperature = self.validate_type(data, dict)

    @property
    def temperature(self):
        return self.get_measure_result(
            self._temperature, max_limit=self.max_temperature, min_limit=self.min_temperature)

    @temperature.setter
    def temperature(self, temp):
        self._temperature = self.validate_type(temp)

    @property
    def humidity(self):
        return self.get_measure_result(
            self._humidity, max_limit=self.max_humidity, min_limit=self.min_humidity)

    @humidity.setter
    def humidity(self, humi):
        self._humidity = self.validate_type(humi)

    @property
    def pressure(self):
        return self.get_measure_result(
            self._pressure, max_limit=self.max_pressure, min_limit=self.min_pressure)

    @pressure.setter
    def pressure(self, pres):
        self._pressure = self.validate_type(pres)

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message):
        self._message = self.validate_type(message, str)

    @property
    def is_night(self):
        return self._is_night

    @is_night.setter
    def is_night(self, is_night):
        self._is_night = self.validate_type(is_night, bool)

    def message_generator(self):
        sum = self.get_measurement_sum()
        message = self.generate_message(sum)
        return message

    def temperature_validator(self):
        temp = self.get_float_value_from_data_dict('temperature')
        return self.validate_min_max(temp, -20, 60)

    def humidity_validator(self):
        humi = self.get_float_value_from_data_dict('humidity')
        return self.validate_min_max(humi, 0, 100)

    def pressure_validator(self):
        pres = self.get_float_value_from_data_dict('pressure')
        return self.validate_min_max(pres, 0, 2000)

    def get_float_value_from_data_dict(self, key):
        data = self.validate_type(self.data, types=dict)
        key = self.validate_type(key, str)
        float_val = data[key]
        return self.validate_type(float_val)

    def get_measure_result(self, value, max_limit=60, min_limit=20):
        for val in (value, max_limit, min_limit):
            self.validate_type(val)
        if value > max_limit:
            result = 'High'
        elif value < min_limit:
            result = 'Low'
        else:
            result = 'Ok'
        return result

    def get_data(self):
        return {
            'temperature': self.temperature,
            'humidity': self.humidity,
            'pressure': self.pressure,
            'message': self.message
        }

    def get_measurement_sum(self):

        high, low, ok = 3, 2, 1
        sum = 0

        temp, humi, pres = self._temperature, self._humidity, self._pressure

        if temp >= self.max_temperature:
            sum += high * 5
        elif temp <= self.min_temperature:
            sum += low * 5
        else:
            sum += ok * 5
        if humi >= self.max_humidity:
            sum += high * 3
        elif humi <= self.min_humidity:
            sum += low * 3
        else:
            sum += ok * 3
        if pres >= self.max_pressure:
            sum += high * -1
        elif pres <= self.min_pressure:
            sum += low * -1
        else:
            sum += ok * -1

        return sum

    def is_night(self):

        now = datetime.now()
        now_time = now.time()
        morning = time(6, 00)
        evening = time(18, 00)

        if now_time > evening or now_time < morning:
            return True

        return False

    def generate_message(self, sum):

        if sum < 10:
            message = "Close window, no need to water."
        elif sum < 15:
            message = "Close window, water the plants."
        elif sum < 20:
            message = "Open window, no need to water."
        else:
            message = "Open window, water the plants."

        return message

    def validate_min_max(self, value, min_value, max_value):
        for val in (value, min_value, max_value):
            self.validate_type(val)
        if not value >= min_value and not value <= max_value:
            raise ValueError(
                f'value should be between {min_value} and {max_value}, {value} given')

        return value

    def validate_type(self, value, types=(int, float)):
        if not isinstance(value, types):
            raise TypeError(
                f'value should be of type {[t for t in types]}, {type(value)} given')
        return value

if __name__ == "__main__":
    mh = Measurement_helper({"temperature": 11, "humidity": 91, "pressure": 1101})

    print(mh.get_data())
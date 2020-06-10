from django.test import TestCase
import unittest
from unittest import mock
import base64
from django.test import Client
from . import views
from . import models
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from .measurement_helper import MeasurementHelper
from .models import Measurement
from freezegun import freeze_time
from pprint import pprint


class MeasurementLogicTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.factory = APIRequestFactory()
        self.user = models.User.objects.get(username='admin')
        # Get the view
        self.view = views.MeasurementLogic.as_view()
        # Insert a record in the db for testing purposes
        if not Measurement.objects.filter(created_by=self.user).exists():
            m = Measurement(temperature=25, humidity=80,
                            pressure=1000, created_by=self.user, message='test')
            m.save()

    def testPost(self):
        # Issue a POST request.

        # Make an authenticated request to the view...
        request = self.factory.post(
            '/measurements/',
            data={
                "temperature": 20,
                "humidity": 60,
                "pressure": 1000
            })
        force_authenticate(request, user=self.user)
        response = self.view(request)
        
        # Check that the response is 201 OK and data is correct.
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {'humidity': 'Ok',
                                         'message': 'Close window, no need to water.',
                                         'pressure': 'Ok',
                                         'sum': 7,
                                         'temperature': 'Ok'})

    def testGet(self):
        # Issue a GET request.

        # Make an authenticated request to the view..rgnb vc.
        request = self.factory.get('/measurements/')
        force_authenticate(request, user=self.user)
        response = self.view(request)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


class MeasurementHelperTest(unittest.TestCase):

    def setUp(self):
        """ Creates an instance of MeasurementHelper and sets up test cases. """
        # Instantiate MeasurementHelper class
        self.measurement_helper = MeasurementHelper(
            {"temperature": 31, "humidity": 91, "pressure": 1101})
        # Create instance of measurementHelper.py class
        # 27 test cases for day data that is expected to output all possible outcomes.
        self.test_case_data_day = [
            {"temperature": 31, "humidity": 91, "pressure": 1101},
            {"temperature": 31, "humidity": 91, "pressure": 899},
            {"temperature": 31, "humidity": 91, "pressure": 1000},
            {"temperature": 31, "humidity": 19, "pressure": 1101},
            {"temperature": 31, "humidity": 19, "pressure": 899},
            {"temperature": 31, "humidity": 19, "pressure": 1000},
            {"temperature": 31, "humidity": 55, "pressure": 1101},
            {"temperature": 31, "humidity": 55, "pressure": 899},
            {"temperature": 31, "humidity": 55, "pressure": 1000},
            {"temperature": 25, "humidity": 91, "pressure": 1101},
            {"temperature": 25, "humidity": 91, "pressure": 899},
            {"temperature": 25, "humidity": 91, "pressure": 1000},
            {"temperature": 25, "humidity": 19, "pressure": 1101},
            {"temperature": 25, "humidity": 19, "pressure": 899},
            {"temperature": 25, "humidity": 19, "pressure": 1000},
            {"temperature": 25, "humidity": 55, "pressure": 1101},
            {"temperature": 25, "humidity": 55, "pressure": 899},
            {"temperature": 25, "humidity": 55, "pressure": 1000},
            {"temperature": 19, "humidity": 91, "pressure": 1101},
            {"temperature": 19, "humidity": 91, "pressure": 899},
            {"temperature": 19, "humidity": 91, "pressure": 1000},
            {"temperature": 19, "humidity": 19, "pressure": 1101},
            {"temperature": 19, "humidity": 19, "pressure": 899},
            {"temperature": 19, "humidity": 19, "pressure": 1000},
            {"temperature": 19, "humidity": 55, "pressure": 1101},
            {"temperature": 19, "humidity": 55, "pressure": 899},
            {"temperature": 19, "humidity": 55, "pressure": 1000}
        ]

        # 27 test cases for night data that is expected to output all possible outcomes.
        self.test_case_data_night = [
            {"temperature": 21, "humidity": 91, "pressure": 1101},
            {"temperature": 21, "humidity": 91, "pressure": 899},
            {"temperature": 21, "humidity": 91, "pressure": 1000},
            {"temperature": 21, "humidity": 19, "pressure": 1101},
            {"temperature": 21, "humidity": 19, "pressure": 899},
            {"temperature": 21, "humidity": 19, "pressure": 1000},
            {"temperature": 21, "humidity": 55, "pressure": 1101},
            {"temperature": 21, "humidity": 55, "pressure": 899},
            {"temperature": 21, "humidity": 55, "pressure": 1000},
            {"temperature": 14, "humidity": 91, "pressure": 1101},
            {"temperature": 14, "humidity": 91, "pressure": 899},
            {"temperature": 14, "humidity": 91, "pressure": 1000},
            {"temperature": 14, "humidity": 19, "pressure": 1101},
            {"temperature": 14, "humidity": 19, "pressure": 899},
            {"temperature": 14, "humidity": 19, "pressure": 1000},
            {"temperature": 14, "humidity": 55, "pressure": 1101},
            {"temperature": 14, "humidity": 55, "pressure": 899},
            {"temperature": 14, "humidity": 55, "pressure": 1000},
            {"temperature": 17, "humidity": 91, "pressure": 1101},
            {"temperature": 17, "humidity": 91, "pressure": 899},
            {"temperature": 17, "humidity": 91, "pressure": 1000},
            {"temperature": 17, "humidity": 19, "pressure": 1101},
            {"temperature": 17, "humidity": 19, "pressure": 899},
            {"temperature": 17, "humidity": 19, "pressure": 1000},
            {"temperature": 17, "humidity": 55, "pressure": 1101},
            {"temperature": 17, "humidity": 55, "pressure": 899},
            {"temperature": 17, "humidity": 55, "pressure": 1000}
        ]

        # The 54 diffrent outcomes
        self.test_case_output_day = [{'temperature': 'High',
                                      'humidity': 'High',
                                      'pressure': 'High',
                                      'sum': 21,
                                      'message': 'Open window, water the plants.'
                                      },
                                     {'temperature': 'High',
                                      'humidity': 'High',
                                      'pressure': 'Low',
                                      'sum': 22,
                                      'message': 'Open window, water the plants.'
                                      },
                                     {'temperature': 'High',
                                      'humidity': 'High',
                                      'pressure': 'Ok',
                                      'sum': 23,
                                      'message': 'Open window, water the plants.'
                                      },
                                     {'temperature': 'High',
                                      'humidity': 'Low',
                                      'pressure': 'High',
                                      'sum': 18,
                                      'message': 'Open window, no need to water.'
                                      },
                                     {'temperature': 'High',
                                      'humidity': 'Low',
                                      'pressure': 'Low',
                                      'sum': 19,
                                      'message': 'Open window, no need to water.'
                                      },
                                     {'temperature': 'High',
                                      'humidity': 'Low',
                                      'pressure': 'Ok',
                                      'sum': 20,
                                      'message': 'Open window, water the plants.'
                                      },
                                     {'temperature': 'High',
                                      'humidity': 'Ok',
                                      'pressure': 'High',
                                      'sum': 15,
                                      'message': 'Open window, no need to water.'
                                      },
                                     {'temperature': 'High',
                                      'humidity': 'Ok',
                                      'pressure': 'Low',
                                      'sum': 16,
                                      'message': 'Open window, no need to water.'
                                      },
                                     {'temperature': 'High',
                                      'humidity': 'Ok',
                                      'pressure': 'Ok',
                                      'sum': 17,
                                      'message': 'Open window, no need to water.'
                                      },
                                     {'temperature': 'Ok',
                                      'humidity': 'High',
                                      'pressure': 'High',
                                      'sum': 11,
                                      'message': 'Close window, water the plants.'
                                      },
                                     {'temperature': 'Ok',
                                      'humidity': 'High',
                                      'pressure': 'Low',
                                      'sum': 12,
                                      'message': 'Close window, water the plants.'
                                      },
                                     {'temperature': 'Ok',
                                      'humidity': 'High',
                                      'pressure': 'Ok',
                                      'sum': 13,
                                      'message': 'Close window, water the plants.'
                                      },
                                     {'temperature': 'Ok',
                                      'humidity': 'Low',
                                      'pressure': 'High',
                                      'sum': 8,
                                      'message': 'Close window, no need to water.'
                                      },
                                     {'temperature': 'Ok',
                                      'humidity': 'Low',
                                      'pressure': 'Low',
                                      'sum': 9,
                                      'message': 'Close window, no need to water.'
                                      },
                                     {'temperature': 'Ok',
                                      'humidity': 'Low',
                                      'pressure': 'Ok',
                                      'sum': 10,
                                      'message': 'Close window, water the plants.'
                                      },
                                     {'temperature': 'Ok',
                                      'humidity': 'Ok',
                                      'pressure': 'High',
                                      'sum': 5,
                                      'message': 'Close window, no need to water.'
                                      },
                                     {'temperature': 'Ok',
                                      'humidity': 'Ok',
                                      'pressure': 'Low',
                                      'sum': 6,
                                      'message': 'Close window, no need to water.'
                                      },
                                     {'temperature': 'Ok',
                                      'humidity': 'Ok',
                                      'pressure': 'Ok',
                                      'sum': 7,
                                      'message': 'Close window, no need to water.'
                                      },
                                     {'temperature': 'Low',
                                      'humidity': 'High',
                                      'pressure': 'High',
                                      'sum': 16,
                                      'message': 'Open window, no need to water.'
                                      },
                                     {'temperature': 'Low',
                                      'humidity': 'High',
                                      'pressure': 'Low',
                                      'sum': 17,
                                      'message': 'Open window, no need to water.'
                                      },
                                     {'temperature': 'Low',
                                      'humidity': 'High',
                                      'pressure': 'Ok',
                                      'sum': 18,
                                      'message': 'Open window, no need to water.'
                                      },
                                     {'temperature': 'Low',
                                      'humidity': 'Low',
                                      'pressure': 'High',
                                      'sum': 13,
                                      'message': 'Close window, water the plants.'
                                      },
                                     {'temperature': 'Low',
                                      'humidity': 'Low',
                                      'pressure': 'Low',
                                      'sum': 14,
                                      'message': 'Close window, water the plants.'
                                      },
                                     {'temperature': 'Low',
                                      'humidity': 'Low',
                                      'pressure': 'Ok',
                                      'sum': 15,
                                      'message': 'Open window, no need to water.'
                                      },
                                     {'temperature': 'Low',
                                      'humidity': 'Ok',
                                      'pressure': 'High',
                                      'sum': 10,
                                      'message': 'Close window, water the plants.'
                                      },
                                     {'temperature': 'Low',
                                      'humidity': 'Ok',
                                      'pressure': 'Low',
                                      'sum': 11,
                                      'message': 'Close window, water the plants.'
                                      },
                                     {'temperature': 'Low',
                                      'humidity': 'Ok',
                                      'pressure': 'Ok',
                                      'sum': 12,
                                      'message': 'Close window, water the plants.'},
                                     ]

        self.test_case_output_night = [{'humidity': 'High',
                                        'message': 'Close window, water the plants.',
                                        'pressure': 'High',
                                        'sum': 11,
                                        'temperature': 'Ok'},
                                       {'humidity': 'High',
                                        'message': 'Close window, water the plants.',
                                        'pressure': 'Low',
                                        'sum': 12,
                                        'temperature': 'Ok'},
                                       {'humidity': 'High',
                                        'message': 'Close window, water the plants.',
                                        'pressure': 'Ok',
                                        'sum': 13,
                                        'temperature': 'Ok'},
                                       {'humidity': 'Low',
                                        'message': 'Close window, no need to water.',
                                        'pressure': 'High',
                                        'sum': 8,
                                        'temperature': 'Ok'},
                                       {'humidity': 'Low',
                                        'message': 'Close window, no need to water.',
                                        'pressure': 'Low',
                                        'sum': 9,
                                        'temperature': 'Ok'},
                                       {'humidity': 'Low',
                                        'message': 'Close window, water the plants.',
                                        'pressure': 'Ok',
                                        'sum': 10,
                                        'temperature': 'Ok'},
                                       {'humidity': 'Ok',
                                        'message': 'Close window, no need to water.',
                                        'pressure': 'High',
                                        'sum': 5,
                                        'temperature': 'Ok'},
                                       {'humidity': 'Ok',
                                        'message': 'Close window, no need to water.',
                                        'pressure': 'Low',
                                        'sum': 6,
                                        'temperature': 'Ok'},
                                       {'humidity': 'Ok',
                                        'message': 'Close window, no need to water.',
                                        'pressure': 'Ok',
                                        'sum': 7,
                                        'temperature': 'Ok'},
                                       {'humidity': 'High',
                                        'message': 'Open window, no need to water.',
                                        'pressure': 'High',
                                        'sum': 16,
                                        'temperature': 'Low'},
                                       {'humidity': 'High',
                                        'message': 'Open window, no need to water.',
                                        'pressure': 'Low',
                                        'sum': 17,
                                        'temperature': 'Low'},
                                       {'humidity': 'High',
                                        'message': 'Open window, no need to water.',
                                        'pressure': 'Ok',
                                        'sum': 18,
                                        'temperature': 'Low'},
                                       {'humidity': 'Low',
                                        'message': 'Close window, water the plants.',
                                        'pressure': 'High',
                                        'sum': 13,
                                        'temperature': 'Low'},
                                       {'humidity': 'Low',
                                        'message': 'Close window, water the plants.',
                                        'pressure': 'Low',
                                        'sum': 14,
                                        'temperature': 'Low'},
                                       {'humidity': 'Low',
                                        'message': 'Open window, no need to water.',
                                        'pressure': 'Ok',
                                        'sum': 15,
                                        'temperature': 'Low'},
                                       {'humidity': 'Ok',
                                        'message': 'Close window, water the plants.',
                                        'pressure': 'High',
                                        'sum': 10,
                                        'temperature': 'Low'},
                                       {'humidity': 'Ok',
                                        'message': 'Close window, water the plants.',
                                        'pressure': 'Low',
                                        'sum': 11,
                                        'temperature': 'Low'},
                                       {'humidity': 'Ok',
                                        'message': 'Close window, water the plants.',
                                        'pressure': 'Ok',
                                        'sum': 12,
                                        'temperature': 'Low'},
                                       {'humidity': 'High',
                                        'message': 'Open window, no need to water.',
                                        'pressure': 'High',
                                        'sum': 16,
                                        'temperature': 'Low'},
                                       {'humidity': 'High',
                                        'message': 'Open window, no need to water.',
                                        'pressure': 'Low',
                                        'sum': 17,
                                        'temperature': 'Low'},
                                       {'humidity': 'High',
                                        'message': 'Open window, no need to water.',
                                        'pressure': 'Ok',
                                        'sum': 18,
                                        'temperature': 'Low'},
                                       {'humidity': 'Low',
                                        'message': 'Close window, water the plants.',
                                        'pressure': 'High',
                                        'sum': 13,
                                        'temperature': 'Low'},
                                       {'humidity': 'Low',
                                        'message': 'Close window, water the plants.',
                                        'pressure': 'Low',
                                        'sum': 14,
                                        'temperature': 'Low'},
                                       {'humidity': 'Low',
                                        'message': 'Open window, no need to water.',
                                        'pressure': 'Ok',
                                        'sum': 15,
                                        'temperature': 'Low'},
                                       {'humidity': 'Ok',
                                        'message': 'Close window, water the plants.',
                                        'pressure': 'High',
                                        'sum': 10,
                                        'temperature': 'Low'},
                                       {'humidity': 'Ok',
                                        'message': 'Close window, water the plants.',
                                        'pressure': 'Low',
                                        'sum': 11,
                                        'temperature': 'Low'},
                                       {'humidity': 'Ok',
                                        'message': 'Close window, water the plants.',
                                        'pressure': 'Ok',
                                        'sum': 12,
                                        'temperature': 'Low'},
                                       ]
    @freeze_time("16:00:00")
    def testConstructAndGetters(self):
        """ Test constructor and getters for day and night test caes data """
        # Combining day and night testcase data
        test_case_input = self.test_case_data_day + self.test_case_data_night
        test_case_output = self.test_case_output_day + self.test_case_output_night

        for index, (testcase, testoutput) in enumerate(zip(test_case_input, test_case_output), 1):
            # Every loop the MeasurementHelper() object will be initialized with a new testcase.
            helper = MeasurementHelper(testcase)
            # get_data() is expected to output a string matching self.test_case_output_day.
            self.assertEqual(helper.getData(), testoutput)

            # all object getters are supposed to return a value matching self.test_case_output_day.
            self.assertEqual(helper.temperature,
                             testoutput.get('temperature'))
            self.assertEqual(helper.pressure, testoutput.get('pressure'))
            self.assertEqual(helper.humidity, testoutput.get('humidity'))

    def testValidateType(self):
        """Test if the input given to the function is of type INT or FLOAT then returns "value" else return a TYPE ERROR"""

        bad_input = ["the is a string", "", {1, 2, 3}, "@!€%"]
        good_input = [12, -20, 13.11, 1000]

        good_output = [
            12,
            -20,
            13.11,
            1000,
        ]

        for index, (bad_in, good_in, good_out) in enumerate(zip(bad_input, good_input, good_output), 1):

            with self.assertRaises(TypeError):
                self.measurement_helper.validateType(bad_in)
            self.assertEqual(
                self.measurement_helper.validateType(good_in), good_out)

    def testValidateMinMax(self):
        """Test if the boundaries min & max is set proberly. If a VALUE ERROR is raised if the input is below min_value or above max_value
           In this test, the values from Temperature boundary analysis is used. No need for testing humidity and pressure values since the output will be the same"""

        bad_input = [-21, 61]
        good_input = [-20, -19, 0, 1, 59, 60]

        expected_output = [-20, -19, 0, 1, 59, 60]

        for bad_in in bad_input:
            with self.assertRaises(ValueError):
                self.measurement_helper.validateMinMax(bad_in, -20, 60)
            print(bad_in, 'ValueError\n')
        for index, (good_in, expected_out) in enumerate(zip(good_input, expected_output), 1):
            self.assertEqual(self.measurement_helper.validateMinMax(
                good_in, -20, 60), expected_out)

    def testGetFloatValueFromDataDict(self):
        """Test that a FLOAT or INT value is returned when the correct key is provided"""

        good_input = [
            'temperature',
            'humidity',
            'pressure',
        ]

        for index, good_in in enumerate(good_input, 1):
            self.assertIsInstance(
                self.measurement_helper.getFloatValueFromDataDict(good_in), (float, int))

    def testGetMeasureResult(self):
        """ Test for function returns correct results for diffrent value combinations. Also test for expected value error if wrong value is parsed. """
        bad_inputs = ["string", None, {1, 3, 4}, "@±≠¶™∞£§“§", TypeError]
        good_inputs = [[28, 25, 10], [25, 40, 20], [5, 10, 100],
                       [0, 0, 0], [-10, 300, -900], [10.1, 10.2, 9.9], [10, 5, 1]]
        good_expected = ["High", "Ok", "Low", "Ok", "Ok", "Ok", "High"]

        # Test expected to succeed.
        for index, expected_output in enumerate(good_expected):
            self.assertEqual(self.measurement_helper.getMeasureResult(
                good_inputs[index][0], good_inputs[index][1], good_inputs[index][2]), expected_output)

        # Test expected to raise error.
        for bad_input in bad_inputs:
            with self.assertRaises(TypeError):
                self.measurement_helper.getMeasureResult(bad_input)
    @freeze_time("16:00:00")
    def testGetMeasurementSum(self):
        """ Test every combination and expect to get correct sum caluclated """
        # Combining day and night testcase data
        test_case_input = self.test_case_data_day + self.test_case_data_night
        test_case_output = self.test_case_output_day + self.test_case_output_night
        for index, (testcase, testoutput) in enumerate(zip(test_case_input, test_case_output), 1):
            # Every loop the MeasurementHelper() object will be initialized with a new testcase.
            helper = MeasurementHelper(testcase)
            # get_data() is expected to output a string matching self.test_case_output_day.
            self.assertEqual(helper.getMeasurementSum(), testoutput.get('sum'))

    @freeze_time("16:00:00")
    def testIsNight(self):
        """ Test that False is returned at 16:00 """
        self.assertFalse(self.measurement_helper.isNight())

    @freeze_time("01:00:00")
    def testIsDay(self):
        """ Test that True is returned at 01:00 """
        self.assertTrue(self.measurement_helper.isNight())




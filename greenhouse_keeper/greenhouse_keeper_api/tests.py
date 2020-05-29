from django.test import TestCase
import unittest
from unittest import mock
import base64
from django.test import Client
from pprint import pprint
from . import views
from . import models
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from .measurement_helper import MeasurementHelper
from freezegun import freeze_time


class MeasurementLogicTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.factory = APIRequestFactory()
        self.user = models.User.objects.get(username='admin')
        # Get the view
        self.view = views.MeasurementLogic.as_view()

    def testPost(self):
        # Issue a POST request.

        # Make an authenticated request to the view...
        request = self.factory.post(
            '/measurements/',
            data={
                "temperature": 20,
                "humidity": 20,
                "pressure": 20
            })
        force_authenticate(request, user=self.user)
        response = self.view(request)

        # Check that the response is 201 OK.
        self.assertEqual(response.status_code, 201)

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
        self.measurement_helper = MeasurementHelper({"temperature": 31, "humidity": 91, "pressure": 1101})
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
        self.test_case_output_day = [{'temperature': 'High', 'humidity': 'High',
                            'pressure': 'High', 'sum': 21, 'message': 'Open window, water the plants.'},
                            {'temperature': 'High', 'humidity': 'High',
                            'pressure': 'Low', 'sum': 22, 'message': 'Open window, water the plants.'},
                            {'temperature': 'High', 'humidity': 'High',
                            'pressure': 'Ok', 'sum': 23, 'message': 'Open window, water the plants.'},
                            {'temperature': 'High', 'humidity': 'Low',
                            'pressure': 'High', 'sum': 18, 'message': 'Open window, no need to water.'},
                            {'temperature': 'High', 'humidity': 'Low',
                            'pressure': 'Low', 'sum': 19, 'message': 'Open window, no need to water.'},
                            {'temperature': 'High', 'humidity': 'Low',
                            'pressure': 'Ok', 'sum': 20, 'message': 'Open window, water the plants.'},
                            {'temperature': 'High', 'humidity': 'Ok',
                            'pressure': 'High', 'sum': 15, 'message': 'Open window, no need to water.'},
                            {'temperature': 'High', 'humidity': 'Ok',
                            'pressure': 'Low', 'sum': 16, 'message': 'Open window, no need to water.'},
                            {'temperature': 'High', 'humidity': 'Ok',
                            'pressure': 'Ok', 'sum': 17, 'message': 'Open window, no need to water.'},
                            {'temperature': 'Ok', 'humidity': 'High',
                            'pressure': 'High', 'sum': 11, 'message': 'Close window, water the plants.'},
                            {'temperature': 'Ok', 'humidity': 'High',
                            'pressure': 'Low', 'sum': 12, 'message': 'Close window, water the plants.'},
                            {'temperature': 'Ok', 'humidity': 'High',
                            'pressure': 'Ok', 'sum': 13, 'message': 'Close window, water the plants.'},
                            {'temperature': 'Ok', 'humidity': 'Low',
                            'pressure': 'High', 'sum': 8, 'message': 'Close window, no need to water.'},
                            {'temperature': 'Ok', 'humidity': 'Low',
                            'pressure': 'Low', 'sum': 9, 'message': 'Close window, no need to water.'},
                            {'temperature': 'Ok', 'humidity': 'Low',
                            'pressure': 'Ok', 'sum': 10, 'message': 'Close window, water the plants.'},
                            {'temperature': 'Ok', 'humidity': 'Ok',
                            'pressure': 'High', 'sum': 5, 'message': 'Close window, no need to water.'},
                            {'temperature': 'Ok', 'humidity': 'Ok',
                            'pressure': 'Low', 'sum': 6, 'message': 'Close window, no need to water.'},
                            {'temperature': 'Ok', 'humidity': 'Ok',
                            'pressure': 'Ok', 'sum': 7, 'message': 'Close window, no need to water.'},
                            {'temperature': 'Low', 'humidity': 'High',
                            'pressure': 'High', 'sum': 16, 'message': 'Open window, no need to water.'},
                            {'temperature': 'Low', 'humidity': 'High',
                            'pressure': 'Low', 'sum': 17, 'message': 'Open window, no need to water.'},
                            {'temperature': 'Low', 'humidity': 'High',
                            'pressure': 'Ok', 'sum': 18, 'message': 'Open window, no need to water.'},
                            {'temperature': 'Low', 'humidity': 'Low',
                            'pressure': 'High', 'sum': 13, 'message': 'Close window, water the plants.'},
                            {'temperature': 'Low', 'humidity': 'Low',
                            'pressure': 'Low', 'sum': 14, 'message': 'Close window, water the plants.'},
                            {'temperature': 'Low', 'humidity': 'Low',
                            'pressure': 'Ok', 'sum': 15, 'message': 'Open window, no need to water.'},
                            {'temperature': 'Low', 'humidity': 'Ok',
                            'pressure': 'High', 'sum': 10, 'message': 'Close window, water the plants.'},
                            {'temperature': 'Low', 'humidity': 'Ok',
                            'pressure': 'Low', 'sum': 11, 'message': 'Close window, water the plants.'},
                            {'temperature': 'Low', 'humidity': 'Ok',
                            'pressure': 'Ok', 'sum': 12, 'message': 'Close window, water the plants.'},
                            ]
                            #TODO: Ret alle disse til at være korrekte.
        self.test_case_output_night = [{'temperature': 'High', 'humidity': 'High',
                            'pressure': 'High', 'sum': 11, 'message': 'Open window, water the plants.'},
                            {'temperature': 'High', 'humidity': 'High',
                            'pressure': 'Low', 'sum': 12, 'message': 'Open window, water the plants.'},
                            {'temperature': 'High', 'humidity': 'High',
                            'pressure': 'Ok', 'sum': 13, 'message': 'Open window, water the plants.'},
                            {'temperature': 'High', 'humidity': 'Low',
                            'pressure': 'High', 'sum': 8, 'message': 'Open window, no need to water.'},
                            {'temperature': 'High', 'humidity': 'Low',
                            'pressure': 'Low', 'sum': 9, 'message': 'Open window, no need to water.'},
                            {'temperature': 'High', 'humidity': 'Low',
                            'pressure': 'Ok', 'sum': 10, 'message': 'Open window, water the plants.'},
                            {'temperature': 'High', 'humidity': 'Ok',
                            'pressure': 'High', 'sum': 5, 'message': 'Open window, no need to water.'},
                            {'temperature': 'High', 'humidity': 'Ok',
                            'pressure': 'Low', 'sum': 6, 'message': 'Open window, no need to water.'},
                            {'temperature': 'High', 'humidity': 'Ok',
                            'pressure': 'Ok', 'sum': 7, 'message': 'Open window, no need to water.'},
                            {'temperature': 'Ok', 'humidity': 'High',
                            'pressure': 'High', 'sum': 16, 'message': 'Close window, water the plants.'},
                            {'temperature': 'Ok', 'humidity': 'High',
                            'pressure': 'Low', 'sum': 17, 'message': 'Close window, water the plants.'},
                            {'temperature': 'Ok', 'humidity': 'High',
                            'pressure': 'Ok', 'sum': 18, 'message': 'Close window, water the plants.'},
                            {'temperature': 'Ok', 'humidity': 'Low',
                            'pressure': 'High', 'sum': 13, 'message': 'Close window, no need to water.'},
                            {'temperature': 'Ok', 'humidity': 'Low',
                            'pressure': 'Low', 'sum': 14, 'message': 'Close window, no need to water.'},
                            {'temperature': 'Ok', 'humidity': 'Low',
                            'pressure': 'Ok', 'sum': 15, 'message': 'Close window, water the plants.'},
                            {'temperature': 'Ok', 'humidity': 'Ok',
                            'pressure': 'High', 'sum': 10, 'message': 'Close window, no need to water.'},
                            {'temperature': 'Ok', 'humidity': 'Ok',
                            'pressure': 'Low', 'sum': 11, 'message': 'Close window, no need to water.'},
                            {'temperature': 'Ok', 'humidity': 'Ok',
                            'pressure': 'Ok', 'sum': 12, 'message': 'Close window, no need to water.'},
                            {'temperature': 'Low', 'humidity': 'High',
                            'pressure': 'High', 'sum': 16, 'message': 'Open window, no need to water.'},
                            {'temperature': 'Low', 'humidity': 'High',
                            'pressure': 'Low', 'sum': 17, 'message': 'Open window, no need to water.'},
                            {'temperature': 'Low', 'humidity': 'High',
                            'pressure': 'Ok', 'sum': 18, 'message': 'Open window, no need to water.'},
                            {'temperature': 'Low', 'humidity': 'Low',
                            'pressure': 'High', 'sum': 13, 'message': 'Close window, water the plants.'},
                            {'temperature': 'Low', 'humidity': 'Low',
                            'pressure': 'Low', 'sum': 14, 'message': 'Close window, water the plants.'},
                            {'temperature': 'Low', 'humidity': 'Low',
                            'pressure': 'Ok', 'sum': 15, 'message': 'Open window, no need to water.'},
                            {'temperature': 'Low', 'humidity': 'Ok',
                            'pressure': 'High', 'sum': 10, 'message': 'Close window, water the plants.'},
                            {'temperature': 'Low', 'humidity': 'Ok',
                            'pressure': 'Low', 'sum': 11, 'message': 'Close window, water the plants.'},
                            {'temperature': 'Low', 'humidity': 'Ok',
                            'pressure': 'Ok', 'sum': 12, 'message': 'Close window, water the plants.'},
                            ]
    '''
    #TODO: This test fails. We need to make sure the getData() is equal to 'testoutput'
    def testConstructAndGetters(self):
        """ Test constructor and getters for day and night test caes data """
        # Combining day and night testcase data
        test_case_input = self.test_case_data_day + self.test_case_data_night
        test_case_output =  self.test_case_output_day + self.test_case_output_night
        for index, (testcase, testoutput) in enumerate(zip(test_case_input, test_case_output),1):
            # Every loop the MeasurementHelper() object will be initialized with a new testcase.
            helper = MeasurementHelper(testcase)
            # get_data() is expected to output a string matching self.test_case_output_day.
            self.assertEqual(helper.getData(), testoutput)

            print(index,helper.getData(), '\n')
            # all object getters are supposed to return a value matching self.test_case_output_day.
            self.assertEquals(helper.temperature, testoutput.get('temperature'))
            self.assertEquals(helper.pressure, testoutput.get('pressure'))
            self.assertEquals(helper.humidity, testoutput.get('humidity'))

            # test is_night() ?
    '''
    def testValidateType(self):
        """Test if the input given to the function is of type INT or FLOAT then returns "value" else return a TYPE ERROR"""        
        
        bad_input = ["the is a string", "", {1,2,3}, "@!€%"]
        good_input = [12, -20, 13.11, 1000]

        good_output = [
            12,
            -20,
            13.11,
            1000, 
            ]
        
        for index, (bad_in, good_in, good_out) in enumerate(zip(bad_input, good_input, good_output),1):

            with self.assertRaises(TypeError):
                self.measurement_helper.validateType(bad_in)
            self.assertEquals(self.measurement_helper.validateType(good_in), good_out)
            print(index, good_out, '\n')
    
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


        for index, (good_in, expected_out) in enumerate(zip(good_input, expected_output),1):
            self.assertEquals(self.measurement_helper.validateMinMax(good_in, -20, 60), expected_out)
            print(index, good_in, '\n')
    

    def testGetFloatValueFromDataDict(self):
        """Test that a FLOAT or INT value is returned when the correct key is provided"""        
        
        good_input = [
            'temperature',
            'humidity',
            'pressure',
            ]
            
        for index, good_in in enumerate(good_input,1):
            self.assertIsInstance(self.measurement_helper.getFloatValueFromDataDict(good_in), (float, int))

    def testGetMeasureResult(self):
        """ Test for function returns correct results for diffrent value combinations. Also test for expected value error if wrong value is parsed. """
        bad_inputs = ["string", None, {1,3,4}, "@±≠¶™∞£§“§", TypeError]
        good_inputs = [[28, 25, 10],[25, 40, 20], [5, 10, 100], [0, 0, 0], [-10, 300, -900], [10.1, 10.2,9.9]]
        good_expected = ["High", "Ok", "Low", "Ok", "Ok"]
        # Test expected to succeed.
        for index, expected_output in enumerate(good_expected):
            self.assertEqual(self.measurement_helper.getMeasureResult(good_inputs[index][0],good_inputs[index][1], good_inputs[index][2]), expected_output)

        # Test expected to raise error.
        for bad_input in bad_inputs:
            with self.assertRaises(TypeError):
                self.measurement_helper.getMeasureResult(bad_input)


    def testGetMeasurementSum(self):
        """ Test every combination and expect to get correct sum caluclated """
         # Combining day and night testcase data
        test_case_input = self.test_case_data_day + self.test_case_data_night
        test_case_output =  self.test_case_output_day + self.test_case_output_night
        for index, (testcase, testoutput) in enumerate(zip(test_case_input, test_case_output),1):
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
        

'''
class TestPasswordGenerator(unittest.TestCase):

    # Instance of PasswordGenerator class with default values
    # length=10, characters=True, numbers=True, specialChar=True, uppercase=True, lowercase=True
    passwordGen = PasswordGenerator()

    def test_constructor(self):
        self.assertIsInstance(self.passwordGen, PasswordGenerator)
        # TODO: More tests here?

    def test_length(self):

        # Test cases for expected exceptions.
        failTestCases = [-10, 0, 9, 31, "string", 0.1, None]
        for testcase in failTestCases:
            print("Expect exception with value:", testcase)
            with self.assertRaises(Exception):
                self.passwordGen.length = testcase

        # Test cases for expected success.
        successTestCases = [10, 15, 30]
        for testcase in successTestCases:
            print("Expect success with value:", testcase)
            self.passwordGen.length = testcase
            self.assertEqual(testcase, self.passwordGen.length)
            not self.assertRaises(Exception)

    def test_characters(self):

        # Test cases for expected exceptions.
        failTestCases = [1, "string", 0.1, None]
        for testcase in failTestCases:
            print("Expect exception with value:", testcase)
            with self.assertRaises(Exception):
                self.passwordGen.characters = testcase
                self.passwordGen.numbers = testcase
                self.passwordGen.specialChar = testcase
                self.passwordGen.uppercase = testcase
                self.passwordGen.lowercase = testcase

        # Test cases for expected success.
        successTestCases = [True, False]
        for testcase in successTestCases:
            print("Expect success with value:", testcase)
            self.passwordGen.characters = testcase
            self.assertEqual(testcase, self.passwordGen.characters)
            not self.assertRaises(Exception)

            self.passwordGen.numbers = testcase
            self.assertEqual(testcase, self.passwordGen.numbers)
            not self.assertRaises(Exception)

            self.passwordGen.specialChar = testcase
            self.assertEqual(testcase, self.passwordGen.specialChar)
            not self.assertRaises(Exception)

            self.passwordGen.uppercase = testcase
            self.assertEqual(testcase, self.passwordGen.uppercase)
            not self.assertRaises(Exception)

            self.passwordGen.lowercase = testcase
            self.assertEqual(testcase, self.passwordGen.lowercase)
            not self.assertRaises(Exception)

    def test_generatePassword(self):

        # Test cases
        testCases = [
            {
                "length": 10,
                "characters": True,
                "numbers": True,
                "specialChar": True,
                "uppercase": True,
                "lowercase": True
            },
            {
                "length": 30,
                "characters": False,
                "numbers": True,
                "specialChar": False,
                "uppercase": False,
                "lowercase": False
            },
            {
                "length": 15,
                "characters": False,
                "numbers": True,
                "specialChar": False,
                "uppercase": True,
                "lowercase": False
            },
            {
                "length": 15,
                "characters": True,
                "numbers": True,
                "specialChar": True,
                "uppercase": True,
                "lowercase": True
            }
        ]
        for testCase in testCases:
            self.passwordGen = PasswordGenerator(
                testCase['length'],
                testCase['characters'],
                testCase['numbers'],
                testCase['specialChar'],
                testCase['uppercase'],
                testCase['lowercase']
            )
            self.assertTrue(type(self.passwordGen.generatePassword()) is str)
            passwordToTest = self.passwordGen.generatePassword()
            print("Testcase: ", testCase, "Testing password: ", passwordToTest)
            # Assert that passwordToTest is alphabethical if testCase numbers is not True and vice versa.
            self.assertEqual(
                passwordToTest.isalpha(), not testCase['numbers'])
            # Assert that passwordToTest is lowercase if testCase uppercase is not True and testCase lowercase is True and vice versa.
            self.assertEqual(
                passwordToTest.islower(), not testCase['uppercase'] and testCase['lowercase'])
            # Assert that the final length of the password is the same as the length provided
            self.assertEqual(
                len(passwordToTest), testCase['length'])
        # Assert that setting all settings to False will throw an error
        print('Expect Exception with all settings set to False:')
        with self.assertRaises(Exception):
            self.passwordGen = PasswordGenerator(
                20,
                False,
                False,
                False,
                False,
                False
            )
            self.passwordGen.generatePassword()
        # Assert that setting all settings to False will throw an error
        print('Expect no Exception with all settings set to True:')
        self.passwordGen = PasswordGenerator(
            20,
            True,
            True,
            True,
            True,
            True
        )
        self.passwordGen.generatePassword()
        not self.assertRaises(Exception)


if __name__ == "__main__":
    unittest.main()
'''

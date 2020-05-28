from django.test import TestCase
import unittest
import base64
from django.test import Client
from pprint import pprint
from . import views
from . import models
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from .measurement_helper import Measurement_helper


class MeasurementLogicTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.factory = APIRequestFactory()
        self.user = models.User.objects.get(username='admin')
        # Get the view
        self.view = views.MeasurementLogic.as_view()

    def test_measurements_post(self):
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

    def test_measurements_get(self):
        # Issue a GET request.

        # Make an authenticated request to the view..rgnb vc.
        request = self.factory.get('/measurements/')
        force_authenticate(request, user=self.user)
        response = self.view(request)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


class MeasurementHelperTest(unittest.TestCase):
    # Create instance of measurement_helper.py class

    '''
    message = "Close window, no need to water."
    message = "Close window, water the plants."
    message = "Open window, no need to water."
    message = "Open window, water the plants."
    '''

    def testOutput(self):
        testCaseData = [
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
        testCaseDataNight = [
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

        testCaseOutput = [{'temperature': 'High', 'humidity': 'High',
                           'pressure': 'High', 'Sum': 21, 'message': 'Open window, water the plants.'},
                          {'temperature': 'High', 'humidity': 'High',
                           'pressure': 'Low', 'Sum': 22, 'message': 'Open window, water the plants.'},
                          {'temperature': 'High', 'humidity': 'High',
                           'pressure': 'Ok', 'Sum': 23, 'message': 'Open window, water the plants.'},
                          {'temperature': 'High', 'humidity': 'Low',
                           'pressure': 'High', 'Sum': 18, 'message': 'Open window, no need to water.'},
                          {'temperature': 'High', 'humidity': 'Low',
                           'pressure': 'Low', 'Sum': 19, 'message': 'Open window, no need to water.'},
                          {'temperature': 'High', 'humidity': 'Low',
                           'pressure': 'Ok', 'Sum': 20, 'message': 'Open window, water the plants.'},
                          {'temperature': 'High', 'humidity': 'Ok',
                           'pressure': 'High', 'Sum': 15, 'message': 'Open window, no need to water.'},
                          {'temperature': 'High', 'humidity': 'Ok',
                           'pressure': 'Low', 'Sum': 16, 'message': 'Open window, no need to water.'},
                          {'temperature': 'High', 'humidity': 'Ok',
                           'pressure': 'Ok', 'Sum': 17, 'message': 'Open window, no need to water.'},
                          {'temperature': 'Ok', 'humidity': 'High',
                           'pressure': 'High', 'Sum': 11, 'message': 'Close window, water the plants..'},
                          {'temperature': 'Ok', 'humidity': 'High',
                           'pressure': 'Low', 'Sum': 12, 'message': 'Close window, water the plants.'},
                          {'temperature': 'Ok', 'humidity': 'High',
                           'pressure': 'Ok', 'Sum': 13, 'message': 'Close window, water the plants.'},
                          {'temperature': 'Ok', 'humidity': 'Low',
                           'pressure': 'High', 'Sum': 8, 'message': 'Close window, no need to water.'},
                          {'temperature': 'Ok', 'humidity': 'Low',
                           'pressure': 'Low', 'Sum': 9, 'message': 'Close window, no need to water.'},
                          {'temperature': 'Ok', 'humidity': 'Low',
                           'pressure': 'Ok', 'Sum': 10, 'message': 'Open window, water the plants.'},
                          {'temperature': 'Ok', 'humidity': 'Ok',
                           'pressure': 'High', 'Sum': 5, 'message': 'Close window, no need to water.'},
                          {'temperature': 'Ok', 'humidity': 'Ok',
                           'pressure': 'Low', 'Sum': 6, 'message': 'Close window, no need to water.'},
                          {'temperature': 'Ok', 'humidity': 'Ok',
                           'pressure': 'Ok', 'Sum': 7, 'message': 'Close window, no need to water.'},
                          {'temperature': 'Low', 'humidity': 'High',
                           'pressure': 'High', 'Sum': 16, 'message': 'Open window, no need to water.'},
                          {'temperature': 'Low', 'humidity': 'High',
                           'pressure': 'Low', 'Sum': 17, 'message': 'Open window, no need to water.'},
                          {'temperature': 'Low', 'humidity': 'High',
                           'pressure': 'Ok', 'Sum': 18, 'message': 'Open window, no need to water.'},
                          {'temperature': 'Low', 'humidity': 'Low',
                           'pressure': 'High', 'Sum': 13, 'message': 'Close window, water the plants.'},
                          {'temperature': 'Low', 'humidity': 'Low',
                           'pressure': 'Low', 'Sum': 14, 'message': 'Close window, water the plants.'},
                          {'temperature': 'Low', 'humidity': 'Low',
                           'pressure': 'Ok', 'Sum': 15, 'message': 'Open window, no need to water.'},
                          {'temperature': 'Low', 'humidity': 'Ok',
                           'pressure': 'High', 'Sum': 10, 'message': 'Close window, water the plants.'},
                          {'temperature': 'Low', 'humidity': 'Ok',
                           'pressure': 'Low', 'Sum': 11, 'message': 'Close window, water the plants.'},
                          {'temperature': 'Low', 'humidity': 'Ok',
                           'pressure': 'Ok', 'Sum': 12, 'message': 'Close window, water the plants.'},
                          ]

        # Test constructor
        for index, testcase in enumerate(testCaseData):
            helper = Measurement_helper(testcase)
            #self.assertEqual(helper.get_data(), testCaseOutput[testCaseData])
            print(helper.get_data(), '\n')
            print("expect", testCaseOutput[index])


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

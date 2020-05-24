from django.test import TestCase
import unittest, base64
from django.test import Client
from pprint import pprint
from . import views
from . import models
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory

class SimpleTest(unittest.TestCase):
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



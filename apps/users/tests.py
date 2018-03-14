import json

from .models import User
from django.urls import reverse

from rest_framework.test import APITestCase


class UserRegistrationAPIViewTestCase(APITestCase):
    url = reverse('user_list')

    def test_user_registration(self):
        """
        Test to verify that a post call with user valid data
        """
        user_data = {
            "username": "elcrack",
            "email": "elcrack@gmail.com",
            "password": "Elpayasoeso12345"
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(200, response.status_code)
        self.assertTrue("token" in json.loads(response.content))

    def test_get_user_registration(self):
        """
        Test to verify the list of users
        """
        user_data = {
            "username": "john",
            "email": "john@snow.com",
            "password": "you_know_nothing"
        }
        user_data_response = {
            "username": "john",
            'first_name': '',
            'last_name': '',
            'email': 'john@snow.com',
        }
        token = json.loads(self.client.post(self.url, user_data).content)
        self.client.credentials(HTTP_AUTHORIZATION=token['token'])
        response = json.loads(self.client.get(self.url).content)
        self.assertEqual(user_data_response, response)


    def test_unique_email_validation(self):
        """
        Test to verify that a post call with already exists email
        """
        user_data_1 = {
            "username": "test2user",
            "email": "test@testuser.com",
            "password": "123123"
        }
        response = self.client.post(self.url, user_data_1)
        self.assertEqual(200, response.status_code)

        user_data_2 = {
            "username": "test2user",
            "email": "test3@testuser.com",
            "password": "123123"
        }
        response = self.client.post(self.url, user_data_2)
        self.assertEqual(400, response.status_code)


class UserLoginAPIViewTestCase(APITestCase):
    url = reverse("user_login")

    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create(
            username=self.username,
            email=self.email,
        )
        self.user.set_password(self.password)
        self.user.save()

    def test_authentication_without_password(self):
        response = self.client.post(self.url, {"email": "daenerys"})
        self.assertEqual(400, response.status_code)

    def test_authentication_with_wrong_password(self):
        response = self.client.post(
            self.url,
            {"email": self.username, "password": "I_know"}
        )
        self.assertEqual(400, response.status_code)

    def test_authentication_with_valid_data(self):
        response = self.client.post(
            self.url,
            {"email": self.email, "password": self.password}
        )
        self.assertEqual(200, response.status_code)
        self.assertTrue("token" in json.loads(response.content))

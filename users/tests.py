# Create your tests here.
from django.test import TestCase

from django.urls import reverse


class LoginTests(TestCase):
    def test_login_view_without_auth(self):
        response = self.client.get(reverse("users:login"))
        self.assertEquals(response.status_code, 200)

    def test_logout_view_without_auth(self):
        response = self.client.get(reverse("users:logout"))
        self.assertEquals(response.status_code, 302)

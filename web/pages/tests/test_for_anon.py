from http import HTTPStatus

from django.test import TestCase, Client
from django.urls import reverse

from ..models import Publication, Comment, User


class TaskAnonUser(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

    def test_open_pages(self):
        urls = [
            '/',
            f'/signup/{self.group.slug}/',
            f'/login/{self.user.username}/'
        ]
        for address in urls:
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

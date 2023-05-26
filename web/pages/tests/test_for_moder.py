from http import HTTPStatus

from django.test import TestCase, Client
from django.urls import reverse

from ..models import Publication, Comment, User


class TaskModer(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Name', role='MODERATOR')
        cls.modarator = Client()
        cls.second_user = User.objects.create_user(username='Another_ordinary_user')
        cls.modarator.force_login(cls.user)
        cls.publication = Publication.objects.create(
            title='Тестовая статья',
            full_text='Тектс для тестовой статьи',
            author = cls.user,
        )

    def test_1(self):
        urls = [
            '/',
            f'/publication/{self.publication.id}/',
            '/personal_page/',
            '/favorites/',
            '/my_publications/',
            '/create/',
            f'/change/{self.publication.id}/',
            f'/users/{self.second_user.id}/',
        ]
        for address in urls:
            with self.subTest(address=address):
                response = self.modarator.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_2(self):
        urls = [
            '/',
            f'/publication/{self.publication.id}/',
            '/personal_page/',
            '/favorites/',
            '/my_publications/',
            '/create/',
            f'/change/{self.publication.id}/',
            f'/users/{self.second_user.id}/',
        ]
        for address in urls:
            with self.subTest(address=address):
                response = self.modarator.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_3(self):
        urls = [
            '/',
            f'/publication/{self.publication.id}/',
            '/personal_page/',
            '/favorites/',
            '/my_publications/',
            '/create/',
            f'/change/{self.publication.id}/',
            f'/users/{self.second_user.id}/',
        ]
        for address in urls:
            with self.subTest(address=address):
                response = self.modarator.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)                

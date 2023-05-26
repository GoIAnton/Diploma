from http import HTTPStatus

from django.test import TestCase, Client
from django.urls import reverse

from ..models import Publication, Comment, User


class TaskAuthUser(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Ordinary_user')
        cls.second_user = User.objects.create_user(username='Another_ordinary_user')
        cls.publication = Publication.objects.create(
            title='Тестовая статья',
            full_text='Тектс для тестовой статьи',
            author = cls.user,
        )
    
    def setUp(self):
        self.authorized_user = Client()
        self.authorized_user.force_login(self.user)

    def test_open_pages(self):
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
                response = self.authorized_user.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)
    
    def test_templates(self):
        urls = [
            '/',
            '/signup/',
            '/login/'
        ]
        for address in urls:
            with self.subTest(address=address):
                response = self.authorized_user.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)
    
    def test_redirect_from_user_page_for_owner(self):
        urls = [
            f'/users/{self.user.id}/',
        ]
        for address in urls:
            with self.subTest(address=address):
                response = self.authorized_user.get(address)
                self.assertRedirects(
                    response,
                    reverse('pages:my_publications')
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
                response = self.authorized_user.get(address)
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
                response = self.authorized_user.get(address)
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
                response = self.authorized_user.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_4(self):
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
                response = self.authorized_user.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

from http import HTTPStatus

from django.test import TestCase, Client
from django.urls import reverse

from ..models import Publication, Comment, User


class TaskAnonUser(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.anon_user = Client()
        cls.user = User.objects.create_user(username='Ordinary_user')
        cls.user2 = User.objects.create_user(username='Ordinary_user_2')
        cls.authorized_user = Client()
        cls.authorized_user.force_login(cls.user)
        cls.publication = Publication.objects.create(
            title='Тестовая статья',
            full_text='Тектс для тестовой статьи',
            author = cls.user2,
        )

    def test_open_pages(self):
        urls = [
            '/personal_page/',
            '/favorites/',
            '/my_publications/',
            '/create/',
        ]
        for address in urls:
            with self.subTest(address=address):
                response = self.anon_user.get(address)
                self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_templates(self):
        urls = [
            '/',
            '/signup/',
            '/login/'
        ]
        for address in urls:
            with self.subTest(address=address):
                response = self.anon_user.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_change_by_other_user(self):
        response = self.authorized_user.post(
            reverse(
                'pages:change',
                kwargs={'publication_id': f'{self.publication.id}'}
            ),
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTrue(
            Publication.objects.filter(
                id=self.publication.id,
                author=self.user2,
                full_text='Тектс для тестовой статьи',
            ).exists()
        )

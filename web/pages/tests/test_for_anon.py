from http import HTTPStatus

from django.test import TestCase, Client
from django.urls import reverse
from django.shortcuts import get_object_or_404

from ..models import Publication, Comment, User


class TaskAnonUser(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.anon_user = Client()

    def test_open_pages(self):
        urls = [
            '/',
            '/signup/',
            '/login/'
        ]
        for address in urls:
            with self.subTest(address=address):
                response = self.anon_user.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

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

    def test_signup(self):
        user_count = User.objects.count()
        form_data = {
            'username': 'New_user',
            'password1': '12341dfqgwbnertbnwtyn546',
            'password2': '12341dfqgwbnertbnwtyn546',
        }
        response = self.anon_user.post(
            reverse('pages:signup'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('pages:index'))
        self.assertEqual(User.objects.count(), user_count + 1)
        username = self.anon_user.get('/my_publications/').context['author'].username
        self.assertEqual(username, 'New_user')

    def test_login(self):
        user_count = User.objects.count()
        form_data = {
            'username': 'New_user',
            'password1': '12341dfqgwbnertbnwtyn546',
            'password2': '12341dfqgwbnertbnwtyn546',
        }
        response = self.anon_user.post(
            reverse('pages:signup'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('pages:index'))
        self.assertEqual(User.objects.count(), user_count + 1)
        username = self.anon_user.get('/my_publications/').context['author'].username
        self.assertEqual(username, 'New_user')
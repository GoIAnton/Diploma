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
        cls.modarator.force_login(cls.user)

    def test_urls_use_correct_templates(self):
        url_templates_names = {
            '/': 'posts/index.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.user.username}/': 'posts/profile.html',
            f'/posts/{self.post.id}/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
            f'/posts/{self.post.id}/edit/': 'posts/create_post.html',
        }
        for address, template in url_templates_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

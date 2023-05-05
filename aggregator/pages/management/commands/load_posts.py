import csv

from pages.models import Post, User, Tag
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.get(id=1)
        tag = Tag.objects.get(slug='ml')
        post = Post(
            title='title',
            full_text='text',
            author = user,
        )
        post.save()
        post.tags.add(tag)

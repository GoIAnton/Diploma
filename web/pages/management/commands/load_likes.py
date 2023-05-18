import csv

from pages.models import Like, User, Publication
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('/app/likes.csv', encoding='utf-8') as r_file:
            file_reader = csv.reader(r_file, delimiter = ",")
            for row in file_reader:
                user = User.objects.get(username=str(row[0]))
                pub = Publication.objects.get(title=str(row[2]))
                Like.objects.get_or_create(
                    publication=pub,
                    user=user,
                    value = row[1],
                )

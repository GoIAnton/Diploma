import csv

from pages.models import Publication, User
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('/app/publications.csv', encoding='utf-8') as r_file:
            user = User.objects.get(username='a')
            file_reader = csv.reader(r_file, delimiter = ",")
            for row in file_reader:
                Publication.objects.get_or_create(
                    title=row[0],
                    full_text=row[1],
                    author = user,
                )

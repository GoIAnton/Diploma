import csv

from pages.models import Tag
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('/app/tags.csv', encoding='utf-8') as r_file:
            file_reader = csv.reader(r_file, delimiter = ",")
            for row in file_reader:
                Tag.objects.get_or_create(
                    name=row[0],
                    slug=row[1],
                )

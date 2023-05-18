import csv

from pages.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('/app/users.csv', encoding='utf-8') as r_file:
            file_reader = csv.reader(r_file, delimiter = ",")
            for row in file_reader:
                User.objects.create_user(
                    username=row[0],
                    password=row[1]
                )
from django.core.management import BaseCommand, CommandError
import subprocess as sp


class Command(BaseCommand):
    help = 'Create not admin user with given credentials'

    def handle(self, *args, **options):
        data = sp.check_output(['pip', 'freeze']).decode('utf-8')
        with open('requirements.txt', 'w') as file:
            file.write(data)

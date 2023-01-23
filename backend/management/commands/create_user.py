from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = 'Create not admin user with given credentials'

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='+', type=str)
        parser.add_argument('password', nargs='+', type=str)

    def handle(self, *args, **options):
        UserModel = get_user_model()
        username = options.get('username')[0]
        pwd = options.get('password')[0]
        if UserModel.objects.filter(username=username).count():
            raise CommandError(f"Username '{username}' is already exists")
        UserModel.objects.create(username=username, password=make_password(pwd))
        print(f"User {username} has created")

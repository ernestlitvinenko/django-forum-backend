import json

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Create not admin user with given credentials'

    def add_arguments(self, parser):
        parser.add_argument('json_path', nargs='+', type=str)

    def handle(self, *args, **options):
        UserModel = get_user_model()
        json_path = options.get('json_path')[0]
        with open(json_path, 'r') as file:
            data = json.load(file)

        users = []

        for user in data:
            username = user.get('username', None)
            password = user.get('password', None)

            if any([username is None, password is None]):
                raise CommandError("Need username and password for all users")
            if UserModel.objects.filter(username=username).count():
                raise CommandError(f"User {username} is already exists")

            query = {
                "username": username,
                "password": make_password(password),
            }

            for key, val in user.items():
                if not key in dir(UserModel):
                    raise CommandError(f"User '{username}' has unexpected attribute '{key}'")
                query[key] = val
            users.append(UserModel(**query))

        UserModel.objects.bulk_create(users)


        # if UserModel.objects.filter(username=username).count():
        #     raise CommandError(f"Username '{username}' is already exists")
        # UserModel.objects.create(username=username, password=make_password(pwd))
        # print(f"User {username} has created")

from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import connection


class User(AbstractUser):
    pass


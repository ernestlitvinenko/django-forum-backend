from django.contrib.auth import get_user_model
from django.conf import settings

from django.db import models

Users: settings.AUTH_USER_MODEL = get_user_model()


class Topics(models.Model):
    owner = models.ForeignKey(Users, on_delete=models.CASCADE)
    topic_name = models.CharField(max_length=100)


class Messages(models.Model):
    owner = models.ForeignKey(Users, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)


class RepliesRelation(models.Model):
    message = models.ForeignKey(Messages, on_delete=models.CASCADE)
    reply = models.ForeignKey(Messages, on_delete=models.CASCADE, related_name='reply')

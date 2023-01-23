import datetime

from django.contrib.auth import get_user_model
from django.conf import settings

from django.db import models

Users: settings.AUTH_USER_MODEL = get_user_model()


class Topics(models.Model):
    owner = models.ForeignKey(Users, on_delete=models.CASCADE)
    topic_name = models.CharField(max_length=100)
    date_created = models.DateField(default=datetime.datetime.utcnow)
    date_modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.topic_name


class Messages(models.Model):
    owner = models.ForeignKey(Users, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)

    def __str__(self):
        return ', '.join([self.owner.username, self.topic.topic_name, self.message])


class RepliesRelation(models.Model):
    message = models.ForeignKey(Messages, on_delete=models.CASCADE)
    reply = models.ForeignKey(Messages, on_delete=models.CASCADE, related_name='reply')


class LikesTopicRelation(models.Model):
    owner = models.ForeignKey(Users, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE)


class LikesMessageRelation(models.Model):
    owner = models.ForeignKey(Users, on_delete=models.CASCADE)
    message = models.ForeignKey(Messages, on_delete=models.CASCADE)


AVAILABLE_MODELS = (Topics, Messages, RepliesRelation, LikesTopicRelation, LikesMessageRelation)

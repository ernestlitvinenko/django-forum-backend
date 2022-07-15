from typing import Dict, TypeVar

from django.contrib import admin
from .models import AVAILABLE_MODELS

AdminModel = TypeVar('AdminModel')


class Topics(admin.ModelAdmin):
    list_display = ('owner', 'topic_name')


class Messages(admin.ModelAdmin):
    list_display = ('owner', 'topic', 'message')


AVAILABLE_ADMINS: Dict[str, AdminModel] = {
    'Topics': Topics,
    'Messages': Messages,
}

[admin.site.register(model) if model.__name__ not in AVAILABLE_ADMINS else admin.site.register(model, AVAILABLE_ADMINS[
    model.__name__]) for model in AVAILABLE_MODELS]

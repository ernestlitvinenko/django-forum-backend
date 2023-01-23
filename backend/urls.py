from django.urls import path
from .views import (GetTopicListView,
                    ThreadView,
                    CreateTopicView,
                    CreateMessageView)

urlpatterns = [
    path('get-topics-list', GetTopicListView.as_view()),
    path('get-topic/<idx>', ThreadView.as_view()),
    path('create-topic', CreateTopicView.as_view()),
    path('create-message', CreateMessageView.as_view())
]

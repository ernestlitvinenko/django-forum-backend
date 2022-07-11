from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, serializers, status
from rest_framework.permissions import IsAuthenticated

from backend.serializers import TopicSerializer, ThreadSerializer, CreateMessageSerializer
from backend.models import Topics, Messages


class GetTopicListView(generics.ListAPIView):
    serializer_class = TopicSerializer

    def get_queryset(self):
        return Topics.objects.all()


class ThreadView(generics.RetrieveAPIView):
    serializer_class = ThreadSerializer

    def get_object(self):
        topic_idx = self.request.query_params.get('idx', None)
        if not topic_idx:
            raise serializers.ValidationError({'idx': {'message': "Need param"}}, code=status.HTTP_400_BAD_REQUEST)
        try:
            topic = Topics.objects.get(pk=int(topic_idx))
        except ObjectDoesNotExist:
            raise serializers.ValidationError({'idx': {'message': "Topic doesn't exist"}},
                                              code=status.HTTP_400_BAD_REQUEST)

        return {
            'topic': topic,
            'messages': Messages.objects.filter(topic=topic)
        }


class CreateTopicView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = TopicSerializer

    def get_serializer(self, *args, **kwargs):
        user = self.request.user
        kwargs['user'] = user

        return super().get_serializer(*args, **kwargs)


class CreateMessageView(generics.CreateAPIView):
    serializer_class = CreateMessageSerializer
    permission_classes = (IsAuthenticated, )

    def get_serializer(self, *args, **kwargs):
        user = self.request.user
        kwargs['user'] = user

        return super().get_serializer(*args, **kwargs)


from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import generics, serializers, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from backend.serializers import TopicSerializer, ThreadSerializer, CreateMessageSerializer
from backend.models import Topics, Messages


class GetTopicListView(generics.ListAPIView):
    # Пример пагинации
    pagination_class = PageNumberPagination
    serializer_class = TopicSerializer

    AVAILABLE_FILTER_FIELDS = {'idxes': 'id', 'users': 'owner_id', 'date-from': "date_created__gte",
                               'date-till': 'date-created__lte'}

    def get_queryset(self):
        # Пример фильтрации
        filters = [(key, val) for key, val in self.request.query_params.items() if key in self.AVAILABLE_FILTER_FIELDS]
        if len(filters):
            filter_query = Q()
            for _filter_key, _filter_val in filters:

                # Если много фильтров
                if len(_filter_val.split(',')) > 1 and _filter_key not in ['date-from', 'date-till']:
                    filter_query = filter_query & Q(
                        **{
                            f"{self.AVAILABLE_FILTER_FIELDS[_filter_key]}__in": _filter_val.split(',')
                           }
                    )
                    continue

                filter_query = filter_query & Q(**{self.AVAILABLE_FILTER_FIELDS[_filter_key]: _filter_val})
            return Topics.objects.filter(filter_query)
        return Topics.objects.all()


class ThreadView(generics.RetrieveAPIView):
    serializer_class = ThreadSerializer

    def get_object(self):
        topic_idx = self.kwargs.get('idx', None)
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
    permission_classes = (IsAuthenticated,)
    serializer_class = TopicSerializer

    def get_serializer(self, *args, **kwargs):
        user = self.request.user
        kwargs['user'] = user

        return super().get_serializer(*args, **kwargs)


class CreateMessageView(generics.CreateAPIView):
    serializer_class = CreateMessageSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer(self, *args, **kwargs):
        user = self.request.user
        kwargs['user'] = user

        return super().get_serializer(*args, **kwargs)

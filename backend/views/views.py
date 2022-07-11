from rest_framework import generics
from .serializers import

class GetTopicListView(generics.ListAPIView):
    serializer_class =
from django.contrib.auth import get_user_model
from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated

from .models import User

Users: User = get_user_model()


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    password = serializers.CharField()

    def create(self, validated_data):
        return Users.objects.create_user(username=validated_data.get('username'),
                                         password=validated_data.get('password'))


class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class RetrieveUserView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

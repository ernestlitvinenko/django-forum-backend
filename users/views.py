from django.contrib.auth import get_user_model
from rest_framework import generics, serializers
from .models import User

Users: User = get_user_model()


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def create(self, validated_data):
        return Users.objects.create_user(username=validated_data.get('username'),
                                         password=validated_data.get('password'))


class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

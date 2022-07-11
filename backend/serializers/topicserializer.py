from rest_framework import serializers
from ..models import Topics


class TopicSerializer(serializers.ModelSerializer):
    topicName = serializers.CharField(source='topic_name')
    user = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def get_user(self, obj):
        return obj.owner.username

    class Meta:
        model = Topics
        fields = ('id', 'topicName', 'user')

    def create(self, validated_data):
        topic_name = validated_data.get('topic_name')

        return Topics.objects.create(owner=self.user, topic_name=topic_name)


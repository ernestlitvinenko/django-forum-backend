from rest_framework import serializers
from .topicserializer import TopicSerializer
from ..models import Messages, RepliesRelation, Topics


class MessageSerializer(serializers.Serializer):
    user = serializers.CharField(source='owner')
    messageText = serializers.CharField(source='message')


class ThreadSerializer(serializers.Serializer):
    topic = TopicSerializer()
    messages = serializers.ListSerializer(child=MessageSerializer())


class CreateMessageSerializer(serializers.Serializer):
    # owner, topic, message
    topicId = serializers.IntegerField(source='topic_id')
    messageText = serializers.CharField(source='message')
    user = serializers.CharField(source='owner', read_only=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        topic_id: int = validated_data.get('topic_id')
        message: str = validated_data.get('message')

        return Messages.objects.create(owner=self.user,
                                       topic_id=topic_id,
                                       message=message)

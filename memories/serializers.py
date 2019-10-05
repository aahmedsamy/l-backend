from rest_framework import serializers
from .models import (Message, Memory, MemoryReply, MessageReply)


class MessageReplyPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageReply
        fields = ['message', 'reply', 'user']


class MemoryReplyPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryReply
        fields = ['memory', 'reply', 'user']


class MessageReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = ['id', 'reply']


class MessageSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ["id", 'body', 'replies']

    def get_replies(self, obj):
        replies = MemoryReply.objects.filter(message=obj)
        return MessageReplySerializer(replies, many=True).data


class MemoryReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryReply
        fields = ['id', 'reply']


class MemorySerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Memory
        fields = ['id', 'title', 'body', 'image', 'replies']

    def get_replies(self, obj):
        replies = MemoryReply.objects.filter(memory=obj)
        return MemoryReplySerializer(replies, many=True).data


class MemoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = ['id', 'title', 'image']


class FavouriteMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message']


class FavouriteMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = ['memory']

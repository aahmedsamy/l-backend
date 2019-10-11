from rest_framework import serializers
from .models import (Message, Memory, MemoryReply, MessageReply, FavouriteMessage, FavouriteMemory)


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
    reply = serializers.SerializerMethodField()
    is_favourite = serializers.SerializerMethodField()

    class Meta:
        model = Message
        exclude = ['index', 'created_by']


    def get_reply(self, obj):
        if obj:
            try:
                reply = MessageReply.objects.get(message=obj)
                return MessageReplySerializer(reply).data
            except MessageReply.DoesNotExist:
                return {}

    def get_is_favourite(self, obj):
        if not obj:
            return
        try:
            FavouriteMessage.objects.get(message=obj, user=self.context.get("request").user)
            return True
        except FavouriteMessage.DoesNotExist:
            return False


class MessageListSerializer(serializers.ModelSerializer):
    is_favourite = serializers.SerializerMethodField()

    class Meta:
        model = Message
        exclude = ['index', 'created_by']

    def get_is_favourite(self, obj):
        if not obj:
            return
        try:
            FavouriteMessage.objects.get(message=obj)
            return True
        except FavouriteMessage.DoesNotExist:
            return False


class MemoryReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryReply
        fields = ['id', 'reply']


class MemorySerializer(serializers.ModelSerializer):
    reply = serializers.SerializerMethodField()
    is_favourite = serializers.SerializerMethodField()

    class Meta:
        model = Memory
        exclude = ['created_by', 'visible']

    def get_reply(self, obj):
        if not obj:
            return
        try:
            reply = MemoryReply.objects.get(memory=obj)
            return MemoryReplySerializer(reply).data
        except MemoryReply.DoesNotExist:
            return {}

    def get_is_favourite(self, obj):
        if not obj:
            return
        try:
            FavouriteMemory.objects.get(memory=obj)
            return True
        except FavouriteMemory.DoesNotExist:
            return False


class MemoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        exclude = ['created_by', 'visible', 'body']


class FavouriteMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message']


class FavouriteMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = ['memory']

from rest_framework import serializers
from .models import (Category, Message, Memory, MemoryReply, MessageReply, FavouriteMessage, FavouriteMemory,
                     SpecialMessageSource, SpecialMessage)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class SpecialMessageSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialMessageSource
        fields = ['id', 'source']


class SpecialMessageSerializer(serializers.ModelSerializer):
    source = SpecialMessageSourceSerializer()

    class Meta:
        model = SpecialMessage
        exclude = ['lovers']


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
        model = MessageReply
        fields = ['id', 'reply']


class MessageSerializer(serializers.ModelSerializer):
    reply = serializers.SerializerMethodField()
    favourite_id = serializers.SerializerMethodField()

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

    def get_favourite_id(self, obj):
        if not obj:
            return
        try:
            fav = FavouriteMessage.objects.get(message=obj)
            return fav.id
        except FavouriteMessage.DoesNotExist:
            return False


class MessageListSerializer(serializers.ModelSerializer):
    favourite_id = serializers.SerializerMethodField()

    class Meta:
        model = Message
        exclude = ['index', 'created_by']

    def get_favourite_id(self, obj):
        if not obj:
            return
        try:
            fav = FavouriteMessage.objects.get(message=obj)
            fav = FavouriteMessage.objects.get(message=obj)
            return fav.id
        except FavouriteMessage.DoesNotExist:
            return False


class MemoryReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryReply
        fields = ['id', 'reply']


class MemorySerializer(serializers.ModelSerializer):
    reply = serializers.SerializerMethodField()
    favourite_id = serializers.SerializerMethodField()
    category = CategorySerializer()

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

    def get_favourite_id(self, obj):
        if not obj:
            return
        try:
            fav = FavouriteMemory.objects.get(memory=obj)
            return fav.id
        except FavouriteMemory.DoesNotExist:
            return False


class MemoryListSerializer(serializers.ModelSerializer):
    favourite_id = serializers.SerializerMethodField()
    category = CategorySerializer()

    class Meta:
        model = Memory
        exclude = ['created_by', 'visible', 'body']

    def get_favourite_id(self, obj):
        if not obj:
            return
        try:
            fav = FavouriteMemory.objects.get(memory=obj)
            return fav.id
        except FavouriteMemory.DoesNotExist:
            return False


class FavouriteMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteMessage
        fields = ['message', 'user']


class FavouriteMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteMemory
        fields = ['memory', 'user']

from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework import (viewsets, mixins)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated)

from helpers.numbers import gen_rand_number_between

from memories.serializers import FavouriteMessageSerializer, FavouriteMemorySerializer

from .models import (Message, Memory, MemoryReply, MessageReply, FavouriteMessage, FavouriteMemory)
from .serializers import (MessageSerializer, MemorySerializer, MemoryListSerializer, MessageReplyPostSerializer,
                          MemoryReplyPostSerializer, MessageListSerializer)


class MessageViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    def get_queryset(self):
        my_love_view = self.request.GET.get('my_love_view', "")
        viewer = self.request.user.get_my_lover()
        if my_love_view.lower() == "true":
            viewer = viewer.get_my_lover()

        if self.action in ["today"]:
            try:
                queryset = Message.objects.get(created_by=viewer, index=True)
            except Message.DoesNotExist:
                queryset = {}
        elif self.action in ["list", 'retrieve']:
            queryset = Message.objects.filter(created_by=viewer, published=True)
        elif self.action in ['favourite']:
            queryset = Message.objects.filter(favourite_message__user=self.request.user)
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def get_serializer_class(self):
        if self.action in ['retrieve', 'today']:
            return MessageSerializer
        if self.action in ['list', 'favourite']:
            return MessageListSerializer

    def get_permissions(self):
        """
        Set actions permissions.
        """
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def today(self, request):
        my_love_view = request.GET.get('my_love_view', "")
        try:
            message = self.get_queryset()
            if not message:
                return Response({})
            if not message.seen and my_love_view.lower() != "true":
                message.seen = True
                message.seen_at = timezone.now()
                message.save()
            serializer = self.get_serializer_class()(message)
            print(serializer.data)
            return Response(serializer.data, 200)
        except Message.DoesNotExist:
            return Response({}, 200)

    @action(detail=False, methods=['get'])
    def favourite(self, requeset):
        messages = self.get_queryset()
        serializer = self.get_serializer_class()(messages, many=True)
        return Response(serializer.data, 200)


class MemoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    def get_queryset(self):
        my_love_view = self.request.GET.get('my_love_view', "")
        viewer = self.request.user.get_my_lover()
        if my_love_view.lower() == "true":
            viewer = viewer.get_my_lover()
        if self.action in ["random_memory"]:
            queryset = Memory.objects.filter(created_by=viewer, publish_date__lt=timezone.now())
            if queryset:
                rand_idx = gen_rand_number_between(0, len(queryset) - 1)
                queryset = queryset[rand_idx]

        elif self.action in ["today"]:
            queryset = Memory.objects.filter(created_by=viewer, publish_date=timezone.now(), visible=True)
        elif self.action in ['list', 'retrieve']:
            queryset = Memory.objects.filter(created_by=viewer, publish_date__lte=timezone.now(), visible=True)
        elif self.action in ['favourite']:
            queryset = Memory.objects.filter(favourite_memory__user=self.request.user)
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def get_serializer_class(self):
        if self.action in ['list', 'favourite', 'today']:
            return MemoryListSerializer
        if self.action in ['random_memory', 'retrieve']:
            return MemorySerializer

    def get_permissions(self):
        """
        Set actions permissions.
        """
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def today(self, request):
        memories = self.get_queryset()
        serializer = self.get_serializer_class()(memories, many=True, context=self.get_serializer_context())
        context = serializer.data
        return Response(context)

    def retrieve(self, request, pk):
        my_love_view = request.GET.get('my_love_view', "")
        memory = get_object_or_404(self.get_queryset(), pk=pk)
        if my_love_view.lower() != "true" and not memory.seen:
            memory.seen = True
            memory.seen_at = timezone.now()
            memory.save()
        serializer = self.get_serializer_class()(memory, context=self.get_serializer_context())
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def random_memory(self, request):
        memories = self.get_queryset()
        serializer = self.get_serializer_class()(memories, context=self.get_serializer_context())
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def favourite(self, requeset):
        memories = self.get_queryset()
        serializer = self.get_serializer_class()(memories, many=True)
        return Response(serializer.data, 200)


class MessageReplyViewSets(mixins.CreateModelMixin, viewsets.GenericViewSet):
    def get_queryset(self):
        queryset = MessageReply.objects.get(user=self.request.user)
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def get_serializer_class(self):
        return MessageReplyPostSerializer

    def get_permissions(self):
        """
        Set actions permissions.
        """
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.get_serializer_class()(data=data)
        if self.request.user.get_my_lover().id != data['user']:
            return Response({"error": "It is not allowed to reply this messages"}, 400)
        serializer.save()

        return Response({"detail": "Your reply added the message"})


class MemoryReplyViewSets(mixins.CreateModelMixin, viewsets.GenericViewSet):
    def get_queryset(self):
        queryset = MemoryReply.objects.get(user=self.request.user)
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def get_serializer_class(self):
        return MemoryReplyPostSerializer

    def get_permissions(self):
        """
        Set actions permissions.
        """
        permission_classes = []
        if self.action in ['create', ]:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.get_serializer_class()(data=data)
        serializer.is_valid(raise_exception=True)
        if self.request.user.get_my_lover().id != data['user']:
            return Response({"error": "It is not allowed to reply this memory"}, 400)
        serializer.save()

        return Response("Replied")


class FavouriteMessageViewSets(mixins.CreateModelMixin, viewsets.GenericViewSet):
    def get_queryset(self):
        queryset = FavouriteMessage.objects.get(user=self.request.user)
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def get_serializer_class(self):
        return FavouriteMessageSerializer

    def get_permissions(self):
        """
        Set actions permissions.
        """
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.get_serializer_class()(data=data)
        serializer.is_valid(raise_exception=True)
        if self.request.user.get_my_lover().id != data['user']:
            return Response({"error": "It is not allowed to reply this messages"}, 400)
        serializer.save()

        return Response("Message added To your favourites")


class FavouriteMemoryViewSets(mixins.CreateModelMixin, viewsets.GenericViewSet):
    def get_queryset(self):
        queryset = FavouriteMemory.objects.get(user=self.request.user)
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def get_serializer_class(self):
        return FavouriteMemorySerializer

    def get_permissions(self):
        """
        Set actions permissions.
        """
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.get_serializer_class()(data=data)
        serializer.is_valid(raise_exception=True)
        if self.request.user.get_my_lover().id != data['user']:
            return Response({"error": "It is not allowed to reply this messages"}, 400)

        serializer.save()

        return Response("Memory added To your favourite")

from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework import (viewsets, mixins)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated)

from helpers.numbers import gen_rand_number_between

from accounts.models import (User, Lover)

from .models import (Message, Memory, MemoryReply, MessageReply)
from .serializers import (MessageSerializer, MemorySerializer, MemoryListSerializer, MessageReplyPostSerializer,
                          MemoryReplyPostSerializer)


def get_viewer(request):
    my_love_view = request.GET.get('my_love_view', False)
    print("my_love_view", my_love_view == "true")
    try:
        if request.user.gender == User.MALE:
            viewer = Lover.objects.get(male=request.user)
            viewer = viewer.male if my_love_view.lower() == "true" else viewer.female
        else:
            viewer = Lover.objects.get(female=request.user)
            viewer = viewer.female if my_love_view.lower() == "true" else viewer.male
    except Lover.DoesNotExist:
        viewer = None
    return viewer


class MessageViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    def get_queryset(self):
        viewer = get_viewer(self.request)
        if self.action == "today":
            queryset = Message.objects.get(created_by=viewer, index=True)
        elif self.action == "list":
            queryset = Message.objects.filter(created_by=viewer, seen=True)
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def get_serializer_class(self):
        return MessageSerializer

    def get_permissions(self):
        """
        Set actions permissions.
        """
        permission_classes = []
        if self.action in ['today', 'list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def today(self, request):
        my_love_view = request.GET.get('my_love_view', False)
        try:
            message = self.get_queryset()
            if not message.seen and my_love_view.lower() != "true":
                message.seen = True
                message.seen_at = timezone.now()
                message.save()
            serializer = self.get_serializer_class()(message)
            return Response(serializer.data, 200)
        except Message.DoesNotExist:
            return Response({}, 200)


class MemoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    def get_queryset(self):
        viewer = get_viewer(self.request)
        if self.action == "random_memory":
            queryset = Memory.objects.filter(created_by=viewer, publish_date__lt=timezone.now())
            rand_idx = gen_rand_number_between(0, len(queryset) - 1)
            queryset = queryset[rand_idx]

        elif self.action == "today":
            queryset = Memory.objects.filter(created_by=viewer, publish_date=timezone.now(), visible=True)
        else:
            queryset = Memory.objects.filter(created_by=viewer, seen=True)
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def get_serializer_class(self):
        if self.action in ['list']:
            return MemoryListSerializer
        if self.action in ['today', 'random_memory', 'retrieve']:
            return MemorySerializer

    def get_permissions(self):
        """
        Set actions permissions.
        """
        permission_classes = []
        if self.action in ['today', 'random_memory', 'retrieve', 'list']:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def today(self, request):
        memories = self.get_queryset()
        serializer = self.get_serializer_class()(memories, many=True, context=self.get_serializer_context())
        context = serializer.data
        return Response(context)

    def retrieve(self, request, pk):
        my_love_view = request.GET.get('my_love_view', False)
        memory = get_object_or_404(self.get_queryset(), pk=pk)
        if my_love_view.lower() != "true":
            memory.seen = True
            memory.seen_at = timezone.now()
            memory.save()
        serializer = self.get_serializer_class()(memory, context=self.get_serializer_context())
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def random_memory(self, request):
        memories = self.get_queryset()
        serializer = self.get_serializer_class()(memories, many=True, context=self.get_serializer_context())
        context = serializer.data
        return Response(context)


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
        permission_classes = []
        if self.action in ['create', ]:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.get_serializer_class()(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response("Liked")


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
        serializer.save()

        return Response("Liked")

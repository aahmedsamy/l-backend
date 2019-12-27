from django.db.models import Q
from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework import (viewsets, mixins)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated)

from memories.serializers import FavouriteMessageSerializer, FavouriteMemorySerializer

from .models import (Category, Message, Memory, MemoryReply, MessageReply, FavouriteMessage, FavouriteMemory,
                     SpecialMessage)
from .serializers import (CategorySerializer, MessageSerializer, MemorySerializer, MemoryListSerializer,
                          MessageReplyPostSerializer,
                          MemoryReplyPostSerializer, MessageListSerializer, SpecialMessageSerializer)


class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        user = self.request.user
        if user.gender == user.MALE:
            return Category.objects.filter(lovers__male=user)
        else:
            return Category.objects.filter(lovers__female=user)

    def get_permissions(self):
        """
        Set actions permissions.
        """
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class SpecialMessageViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = SpecialMessageSerializer

    def get_queryset(self):
        user = self.request.user
        if user.gender == user.MALE:
            return SpecialMessage.objects.filter(lovers__male=user)
        else:
            return SpecialMessage.objects.filter(lovers__female=user)

    def get_permissions(self):
        """
        Set actions permissions.
        """
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


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
            queryset = Message.objects.filter(favourite_message__user=viewer.get_my_lover())
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
        serializer = self.get_serializer_class()(messages, many=True, context=self.get_serializer_context())
        return Response(serializer.data, 200)


class MemoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    def get_queryset(self):
        my_love_view = self.request.GET.get('my_love_view', "")
        viewer = self.request.user.get_my_lover()
        if my_love_view.lower() == "true":
            viewer = viewer.get_my_lover()

        day = self.request.GET.get("day", None)
        month = self.request.GET.get("month", None)
        year = self.request.GET.get("year", None)

        category_id = self.request.GET.get('cat', None)
        extra = dict()
        if day or month or year:
            if day:
                extra['publish_date__day'] = day
            if month:
                extra['publish_date__month'] = month
            if year:
                extra['publish_date__year'] = year
        else:
            if self.action in ['list', 'retrieve']:
                extra['publish_date__lte'] = timezone.now()

        if self.action in ["memory_in_this_day"]:
            queryset = Memory.objects.filter(created_by=viewer, publish_date__lt=timezone.now(), **extra)

        elif self.action in ["today"]:
            queryset = Memory.objects.filter(
                Q(created_by=viewer, publish_date=timezone.now(), visible=True) | Q(created_by=viewer,
                                                                                    publish_date__lt=timezone.now(),
                                                                                    visible=True, seen=False))
        elif self.action in ['list', 'retrieve']:
            if category_id:
                queryset = Memory.objects.filter(created_by=viewer, visible=True, category__id=category_id,
                                                 **extra)
            else:
                queryset = Memory.objects.filter(created_by=viewer, visible=True, **extra)

        elif self.action in ['favourite']:
            if category_id:
                queryset = Memory.objects.filter(favourite_memory__user=viewer.get_my_lover(),
                                                 category_id=category_id)
            else:
                queryset = Memory.objects.filter(favourite_memory__user=viewer.get_my_lover())

        return queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def get_serializer_class(self):
        if self.action in ['list', 'favourite', 'today', 'memory_in_this_day']:
            return MemoryListSerializer
        if self.action in ['retrieve']:
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
    def memory_in_this_day(self, request):
        memories = self.get_queryset()
        serializer = self.get_serializer_class()(memories, many=True, context=self.get_serializer_context())
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def favourite(self, request):
        memories = self.get_queryset()
        serializer = self.get_serializer_class()(memories, many=True, context=self.get_serializer_context())
        return Response(serializer.data, 200)


class MessageReplyViewSets(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin,
                           viewsets.GenericViewSet):
    def get_queryset(self):
        queryset = MessageReply.objects.filter(user=self.request.user)
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
        serializer = self.get_serializer_class()(data=data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        created_by = Message.objects.get(id=data['message']).created_by
        if created_by.get_my_lover().id != data['user']:
            return Response({"error": "It is not allowed to reply this messages"}, 400)
        reply = serializer.save()

        return Response({"reply_id": reply.id})


class MemoryReplyViewSets(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin,
                          viewsets.GenericViewSet):
    def get_queryset(self):
        queryset = MemoryReply.objects.filter(user=self.request.user)
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
        serializer = self.get_serializer_class()(data=data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        created_by = Memory.objects.get(id=data['memory']).created_by
        if created_by.get_my_lover().id != data['user']:
            return Response({"error": "It is not allowed to reply this memory"}, 400)
        reply = serializer.save()

        return Response({"reply_id": reply.id})


class FavouriteMessageViewSets(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    def get_queryset(self):
        queryset = FavouriteMessage.objects.filter(user=self.request.user)
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
        serializer = self.get_serializer_class()(data=data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        created_by = Message.objects.get(id=data['message']).created_by
        if created_by.get_my_lover().id != data['user']:
            return Response({"error": "It is not allowed add this message to your favourites"}, 400)
        favourite = serializer.save()

        return Response({"favourite_id": favourite.id})


class FavouriteMemoryViewSets(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    def get_queryset(self):
        queryset = FavouriteMemory.objects.filter(user=self.request.user)
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
        serializer = self.get_serializer_class()(data=data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        created_by = Memory.objects.get(id=data['memory']).created_by
        if created_by.get_my_lover().id != data['user']:
            return Response({"error": "It is not allowed add this memory to your favourites"}, 400)

        favourite = serializer.save()

        return Response({"favourite_id": favourite.id})

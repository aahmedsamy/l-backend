from rest_framework import (viewsets, status)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny)

from rest_framework_jwt.settings import api_settings

from .models import User
from .serializers import (LoginSerializer, )


def generate_token(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)


class UserViewSet(viewsets.GenericViewSet):
    def get_queryset(self):
        queryset = User.objects.filter(is_active=True)
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}

    serializer_class = LoginSerializer

    def get_permissions(self):
        """
        Set actions permissions.
        """
        permission_classes = []
        if self.action in ['login']:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def auth(self, serializer):
        kwargs = dict()
        if '@' in serializer.data['phone_or_email']:
            kwargs['email'] = serializer.data['phone_or_email']
        else:
            kwargs['username'] = serializer.data['phone_or_email']

        try:
            user = User.objects.get(**kwargs)
            if user.check_password(serializer.data['password']):
                return user
        except User.DoesNotExist:
            return None

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        context = dict()
        if serializer.is_valid():
            user = self.auth(serializer)
            if not user:
                context['detail'] = "Unable to login with provided credentials"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            token = generate_token(user)
            context['token'] = token
            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


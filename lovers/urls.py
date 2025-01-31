"""lovers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter

from accounts.views import (UserViewSet,)
from memories.views import (CategoryViewSet, MessageViewSet, MemoryViewSet, MessageReplyViewSets, MemoryReplyViewSets,
                            FavouriteMessageViewSets, FavouriteMemoryViewSets, SpecialMessageViewSet)

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('categories', CategoryViewSet, base_name='categories')
router.register('messages', MessageViewSet, basename='messages')
router.register('memories', MemoryViewSet, basename='memories')
router.register('memory_replies', MemoryReplyViewSets, basename='memory_replies')
router.register('message_replies', MessageReplyViewSets, basename='message_replies')
router.register('favourite_messages', FavouriteMessageViewSets, basename='favourite_messages')
router.register('favourite_memories', FavouriteMemoryViewSets, basename='favourite_memories')
router.register('special_messages', SpecialMessageViewSet, basename='special_messages')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

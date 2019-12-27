from django.contrib import admin

from accounts.models import Lover

from .models import (Category, Memory, Message, SpecialMessageSource, SpecialMessage)
from .forms import (MemoryForm, MessageForm)


# Register your models here.

def get_lover_instance(user):
    if user.gender == user.MALE:
        return Lover.objects.get(male=user)
    return Lover.objects.get(female=user)

@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    exclude = ['created_by']
    form = MemoryForm
    list_display = ['title', 'category', 'publish_date', 'visible', 'seen']
    list_editable = ['category', 'visible', 'publish_date']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        return qs.filter(created_by=request.user)

    def has_add_permission(self, request):
        return True

    def has_view_or_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


@admin.register(SpecialMessage)
class SpecialMessageAdmin(admin.ModelAdmin):
    exclude = ['lovers']
    form = MessageForm

    def save_model(self, request, obj, form, change):
        obj.lovers = get_lover_instance(request.user)
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        return qs.filter(lovers=get_lover_instance(request.user))

    def has_add_permission(self, request):
        return True

    def has_view_or_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    exclude = ['created_by', 'published']
    form = MessageForm

    list_display = ['body', 'index', 'seen']
    list_editable = ['index']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(created_by=request.user)

    def has_add_permission(self, request):
        return True

    def has_view_or_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


@admin.register(Category)
class Category(admin.ModelAdmin):
    exclude = ['lovers']

    def save_model(self, request, obj, form, change):
        obj.name = obj.name.upper()
        obj.lovers = get_lover_instance(request.user)
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        if user.gender == user.MALE:
            return qs.filter(lovers__male=user)
        else:
            return qs.filter(lovers__female=user)

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


@admin.register(SpecialMessageSource)
class SpecialMessageSource(admin.ModelAdmin):
    exclude = ['lovers']

    def save_model(self, request, obj, form, change):
        obj.source = obj.source.upper()
        obj.lovers = get_lover_instance(request.user)
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        if user.gender == user.MALE:
            return qs.filter(lovers__male=user)
        else:
            return qs.filter(lovers__female=user)

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

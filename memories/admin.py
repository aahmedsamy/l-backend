from django.contrib import admin
from .models import (Memory, Message)
from .forms import (MemoryForm, MessageForm)


# Register your models here.
@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    exclude = ['created_by']
    form = MemoryForm

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


@admin.register(Message)
class Message(admin.ModelAdmin):
    exclude = ['created_by']
    form = MessageForm

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

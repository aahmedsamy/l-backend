from django.contrib import admin
from .models import (Memory, Message)
from .forms import (MemoryForm, MessageForm)


# Register your models here.
@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    # exclude = ['created_by']
    form = MemoryForm

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Message)
class Message(admin.ModelAdmin):
    # exclude = ['created_by']
    form = MessageForm

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)

from django.contrib import admin
from .models import (Memory, Message)
from .forms import (MemoryForm, MessageForm)


# Register your models here.
@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    form = MemoryForm


@admin.register(Message)
class Message(admin.ModelAdmin):
    form = MessageForm

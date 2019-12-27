from django.db import models
from django.conf import settings

from accounts.models import Lover


# Create your models here.
class Category(models.Model):
    lovers = models.ForeignKey(Lover, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']


class Message(models.Model):
    body = models.TextField(max_length=1024)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name="message_created_by")
    index = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)
    seen_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.index:
            self.published = True
            qs = Message.objects.filter(index=True, created_by=self.created_by)
            qs.update(index=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.body

    class Meta:
        ordering = ['-id']


class Memory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="memory_category")
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=1024)
    image = models.ImageField(upload_to="images")
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memory_created_by")
    seen = models.BooleanField(default=False)
    seen_at = models.DateTimeField(null=True, blank=True)
    publish_date = models.DateField()
    visible = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Memory"
        verbose_name_plural = "Memories"
        ordering = ['-publish_date']


class FavouriteMessage(models.Model):
    message = models.OneToOneField(Message, related_name="favourite_message", on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_fav_message")


class FavouriteMemory(models.Model):
    memory = models.OneToOneField(Memory, related_name="favourite_memory", on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_fav_memory")


class MessageReply(models.Model):
    message = models.OneToOneField(Message, related_name="message_reply", on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_message_reply")
    reply = models.TextField(max_length=1024)


class MemoryReply(models.Model):
    memory = models.OneToOneField(Memory, related_name="memory_reply", on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_memory_reply")
    reply = models.TextField(max_length=1024)

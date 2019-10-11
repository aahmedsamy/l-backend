from django.db import models
from django.conf import settings


# Create your models here.
class Message(models.Model):
    body = models.TextField(max_length=1024)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="message_created_by")
    index = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)
    seen_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.index:
            qs = Message.objects.filter(index=True, created_by=self.created_by)
            qs.update(index=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.body

    class Meta:
        ordering = ['-id']


class Memory(models.Model):
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
        ordering = ['-id']


class FavouriteMessage(models.Model):
    message = models.ForeignKey(Message, related_name="favourite_message", on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_fav_message")

    class Meta:
        unique_together = ["message", "user"]


class FavouriteMemory(models.Model):
    memory = models.ForeignKey(Memory, related_name="favourite_memory", on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_fav_memory")

    class Meta:
        unique_together = ["memory", "user"]


class MessageReply(models.Model):
    message = models.ForeignKey(Message, related_name="message_reply", on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_message_reply")
    reply = models.TextField(max_length=1024)


class MemoryReply(models.Model):
    memory = models.ForeignKey(Memory, related_name="memory_reply", on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_memory_reply")
    reply = models.TextField(max_length=1024)

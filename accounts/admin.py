from django.contrib import admin

from .models import (User, Lover)


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(Lover)
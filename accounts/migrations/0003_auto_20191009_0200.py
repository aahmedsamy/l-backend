# Generated by Django 2.2.6 on 2019-10-08 23:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_lover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lover',
            name='female',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='female_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='lover',
            name='male',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='male_user', to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 2.2.6 on 2019-12-27 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('memories', '0013_specialmessage_specialmessagesource'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialmessage',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='special_message_lovers', to='accounts.Lover'),
        ),
    ]

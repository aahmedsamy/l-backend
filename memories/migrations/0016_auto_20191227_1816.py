# Generated by Django 2.2.6 on 2019-12-27 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memories', '0015_auto_20191227_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialmessage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]

# Generated by Django 2.2.6 on 2019-11-20 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memories', '0009_auto_20191120_1356'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-id'], 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
    ]

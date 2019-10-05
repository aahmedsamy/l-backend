# Generated by Django 2.2.6 on 2019-10-04 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memories', '0006_auto_20191004_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='memory',
            name='visible',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='memory',
            name='publish_date',
            field=models.DateField(),
        ),
    ]

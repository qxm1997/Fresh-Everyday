# Generated by Django 2.2.1 on 2019-12-29 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='is_now',
            field=models.IntegerField(default=0),
        ),
    ]

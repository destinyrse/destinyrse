# Generated by Django 3.2.9 on 2021-11-23 11:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20211123_0936'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
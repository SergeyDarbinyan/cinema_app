# Generated by Django 4.2.18 on 2025-01-17 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_events_movie_alter_events_room_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TodoItem',
        ),
    ]

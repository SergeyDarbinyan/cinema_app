# Generated by Django 4.2.18 on 2025-01-16 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_rename_room_movies_rename_movie_rooms_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.movies'),
        ),
        migrations.AlterField(
            model_name='events',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.rooms'),
        ),
        migrations.AlterField(
            model_name='seats',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.rooms'),
        ),
    ]
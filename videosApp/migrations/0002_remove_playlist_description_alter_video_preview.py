# Generated by Django 4.2 on 2024-04-22 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videosApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playlist',
            name='description',
        ),
        migrations.AlterField(
            model_name='video',
            name='preview',
            field=models.FileField(blank=True, upload_to='preview'),
        ),
    ]

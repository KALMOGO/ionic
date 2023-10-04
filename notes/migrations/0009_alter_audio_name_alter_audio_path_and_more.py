# Generated by Django 4.1.4 on 2023-05-10 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("notes", "0008_alter_video_options_rename_number_audio_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="audio",
            name="name",
            field=models.CharField(max_length=250, unique=True),
        ),
        migrations.AlterField(
            model_name="audio",
            name="path",
            field=models.CharField(max_length=250, unique=True),
        ),
        migrations.AlterField(
            model_name="emotion",
            name="emoji",
            field=models.CharField(max_length=250, unique=True),
        ),
        migrations.AlterField(
            model_name="emotion",
            name="name",
            field=models.CharField(max_length=250, unique=True),
        ),
        migrations.AlterField(
            model_name="video",
            name="name",
            field=models.CharField(max_length=250, unique=True),
        ),
        migrations.AlterField(
            model_name="video",
            name="path",
            field=models.CharField(max_length=250, unique=True),
        ),
    ]
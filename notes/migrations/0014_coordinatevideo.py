# Generated by Django 4.0.10 on 2023-08-02 22:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0013_alter_audio_number_alter_video_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoordinateVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longitude', models.CharField(max_length=50)),
                ('latitude', models.CharField(max_length=50)),
                ('town', models.CharField(max_length=50)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('localisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location_video', to='notes.annotationvideo')),
            ],
            options={
                'ordering': ['-creation_date'],
            },
        ),
    ]

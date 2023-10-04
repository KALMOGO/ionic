# Generated by Django 4.0.10 on 2023-07-03 23:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_language'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0010_rename_video_annotationvideo_video_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='video',
            options={'ordering': ['-creation_date', 'number', 'path', 'language']},
        ),
        migrations.RemoveField(
            model_name='audio',
            name='name',
        ),
        migrations.RemoveField(
            model_name='video',
            name='name',
        ),
        migrations.AddField(
            model_name='audio',
            name='number',
            field=models.CharField(default=0, max_length=250),
        ),
        migrations.AddField(
            model_name='video',
            name='number',
            field=models.CharField(default=0, max_length=250),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='annotations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='annotationvideo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='annotation_video', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='audio',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='music', to='accounts.language'),
        ),
        migrations.AlterField(
            model_name='audio',
            name='path',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='emotion',
            name='emoji',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='emotion',
            name='name',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='video',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video', to='accounts.language'),
        ),
        migrations.AlterField(
            model_name='video',
            name='path',
            field=models.CharField(max_length=250),
        ),
        migrations.CreateModel(
            name='Coordinate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longitude', models.CharField(max_length=50)),
                ('latitude', models.CharField(max_length=50)),
                ('town', models.CharField(max_length=50)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('localisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location', to='notes.annotation')),
            ],
            options={
                'ordering': ['-creation_date'],
            },
        ),
    ]
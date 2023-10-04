from django.contrib import admin
from .models import *

# Register your models here.

class AutoFilter(admin.ModelAdmin):
    list_display = ('id','path','language', 'numAnnotate','creation_date')
    list_filter = ('language',)

class AnnotationFilter(admin.ModelAdmin):
    list_display = ('id','emotion','audio','user','creation_date')


class EmotionFilter(admin.ModelAdmin):
    list_display =('id','name', 'emoji', 'creation_date')
    list_filter=('name',)

class CoordinateFilter(admin.ModelAdmin):
    list_display =('id','longitude', 'latitude','localisation', 'creation_date')

class CoordinateVideoFilter(admin.ModelAdmin):
    list_display =('id','longitude', 'latitude','localisation', 'creation_date')

class AudioResultAnnotationFilter(admin.ModelAdmin):
    list_display=('id','audio', 'note_name', 'note_emoji' ,'creation_date')


class VideoFilter(admin.ModelAdmin):
    list_display = ('id','number','path','language', 'numAnnotate','creation_date')
    list_filter = ('language',)

class VideoAnnotationFilter(admin.ModelAdmin):
    list_display = ('id','emotion','user','creation_date')

class VideoResultAnnotationFilter(admin.ModelAdmin):
    list_display=('id', 'note_name', 'note_emoji' ,'creation_date')



admin.site.register(Audio, AutoFilter)
admin.site.register(Video, VideoFilter)
admin.site.register(Annotation, AnnotationFilter)
admin.site.register(AnnotationVideo, VideoAnnotationFilter)
admin.site.register(Emotion, EmotionFilter)
admin.site.register(AudioResultAnnotation, AudioResultAnnotationFilter)
admin.site.register(VideoResultAnnotation, VideoResultAnnotationFilter)
admin.site.register(Coordinate)
admin.site.register(CoordinateVideo)
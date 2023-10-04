
from django.urls import path
from .views import *


urlpatterns = [
    path('emotion/list/', view=EmotionAPICview.as_view(), name="emotion"),
    
    #Audio
    path('audio/list/', view=list_create_AudioPIVIEW, name="audio"),
    path('audio/mark/', view=AnnotationUserAPIView.as_view(), name='list_audio'),
    path('audio/mark/<int:pk>/update/', view=AnnotationUserAPIView.as_view(), name='note_update'),
    path('audio/<int:pk>/detail/', view=ret_upate_del_AudioView, name="updateNoteaudio"),
    
    #Video 
    path('Video/list/', view=list_create_VideoPIVIEW, name="video"),
    path('video/mark/', view=AnnotationVideoUserAPIView.as_view(), name='list_video'),
    path('video/mark/<int:pk>/update/', view=AnnotationVideoUserAPIView.as_view(), name='video_update'),
    path('video/<int:pk>/detail/', view=ret_upate_del_VideoView, name="updateNotevideo"),
    
    #Perform Annotation des audios
    path('audio/post/', view=PostAnnotationAPIView.as_view(), name="PostNotevideo"),
    path('audio/<int:pk>/update/', view=UpdateAnnotationAPIView.as_view(), name="update_audio_note"),

    # ----- annotation des videos --------------------------

    path('video/post/', view=PostAnnotationVideoAPIView.as_view(), name="PostNewvideo"),
    path('video/<int:pk>/update/', view=UpdateAnnotationVideoAPIView.as_view(), name="update_video_note"),

    #   Données final
    path('audio/resume/list', view=list_create_final_note_audioAPIView, name="result_audio_final"),
    path('location/post/', view=add_list_location, name="locationView_1"),
    path('location/list/', view=add_list_location, name="locationView_2"),
    path('location/<int:pk>/update/', view=update_location, name="update_location"),
    path('location/<int:audio>/retrieve/', view=retrieve_audio_location, name="retrieve_location"),


    #  Localisation video
    path('locationVideo/post/', view=add_list_locationVideo, name="locationView_1"),
    path('locationVideo/list/', view=add_list_locationVideo, name="locationView_2"),
    path('locationVideo/<int:pk>/update/', view=update_locationVideo, name="update_location"),
    path('locationVideo/<int:video>/retrieve/', view=retrieve_video_location, name="retrieve_location")
]
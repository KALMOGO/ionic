
from rest_framework import generics, permissions
from .models import *
from .serializers import *

#----------------------------- Gestion des Audios ----------------------------

class HomeAPIView(generics.ListCreateAPIView):
    '''
        View: get, post Audio
        liste des audio annoter par l'utilisateur et non par l'utilisateur
    '''
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer
    paginator = None
list_create_AudioPIVIEW = HomeAPIView.as_view()

class RetUpdateDelHome(generics.RetrieveUpdateDestroyAPIView):
    '''
        View pour put, patch, delete des Audio 
    '''
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer
    permission_classes = [permissions.IsAdminUser]
ret_upate_del_AudioView = RetUpdateDelHome.as_view()

class EmotionAPICview(generics.ListCreateAPIView):
    queryset = Emotion.objects.all()
    serializer_class = EmotionSerializer
    permission_classes = [permissions.IsAuthenticated]
    paginator = None

class RetUpdateDelEmotion(generics.RetrieveUpdateDestroyAPIView):
    queryset = Emotion.objects.all()
    serializer_class = EmotionSerializer
    permission_classes = [permissions.IsAdminUser]
    paginator = None

class CreateAudio(generics.CreateAPIView):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer
    permission_classes = [permissions.IsAdminUser]
    

from django.db.models import Count
class AnnotationUserAPIView(generics.ListCreateAPIView):
    serializer_class = AnnotationAudioSerializer
    permission_classes = [permissions.IsAuthenticated]
    #paginator = None  #switch on the pagination
    
    def get_queryset(self):
        # Retourne 5 audio de meme langage que l'utilisateur conncete et dont le 
        # nombre de fois que l'audio a été annoté n'a pas atteint 5   
    
        limit_Annotation_Num = 5
        user = self.request.user
        
        # Audio.objects.filter(language__language=user.language)\
        #         .annotate(num_annotators=Count('annotations__user',
        #                 filter=Q(annotations__user__job=user.job)))\
        #         .filter(numAnnotate__lte=limit_Annotation_Num)
        
        return  Audio.objects.filter(language__language = user.language,
                    numAnnotate__lte=limit_Annotation_Num)

from django.db.models import Count


class UpdateAnnotationAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        audio_annotate = Audio.objects.get(id=self.request.data["audio"])
        response = super().patch(request, *args, **kwargs)
        
        # calcul et enregistrement de l'annotation maximal pour l'audio
        if audio_annotate.numAnnotate == 5:
            # Calcul donne chaque annotations et leur nombre par ordre decroissant du nombre
            annotation_compte = Annotation.objects.filter(audio=audio_annotate).values(
                'emotion').order_by().annotate(emotion_count=Count('emotion')).order_by('-emotion_count')
                # recupere l'audio concerne par l'annotation
            
            if len(annotation_compte)!= 0:
                if len(annotation_compte)  == 1: # si on une seul note c'est l'annotion maximale
                    self.note_final_save(annotation_compte[0]["emotion"], audio_annotate)
                else: # si on plus d'une note pour l'audio: les deux premier son les maximun
                    a1 = annotation_compte[0]
                    a2 = annotation_compte[1]
                    
                    if a1['emotion_count'] == a2['emotion_count']: 
                            # Filter annotations based on the first element of annotation_compte
                        annotation_profil_a1 = Annotation.objects.filter(
                            audio=audio_annotate,emotion=a1["emotion"],user__job="Illiterate"
                        ).values('user__job').annotate(emotion_count=Count('user__job')).order_by('-emotion_count')

                        annotation_profil_a2 = AnnotationVideo.objects.filter(audio=audio_annotate,
                            emotion=a2["emotion"],user__job="Illiterate").values('user__job').annotate(
                            emotion_count=Count('user__job')).order_by('-emotion_count')

                        # Get the count of Illiterate occurrences directly from the query
                        cpt1 = annotation_profil_a1[0]['emotion_count'] if annotation_profil_a1 else 0

                        # Get the count of Illiterate occurrences directly from the query
                        cpt2 = annotation_profil_a2[0]['emotion_count'] if annotation_profil_a2 else 0

                        if cpt1 > cpt2:
                            self.note_final_save(a1, audio_annotate)
                        elif cpt2 > cpt1:
                            self.note_final_save(a2, audio_annotate)
                        else :
                            audio_annotate.numAnnotate =0
                            audio_annotate.save()
                    else:
                        # sinon la note 1 est le maximun
                        self.note_final_save(a1, audio_annotate)
        return response
    

    def note_final_save(self, arg0, audio_annotate):
        emotion_max = Emotion.objects.get(id=arg0["emotion"])
        audioResult = AudioResultAnnotation.objects.filter(audio=audio_annotate)
        if len(audioResult)==0:
            final_audio_note = AudioResultAnnotation(
            audio=audio_annotate, audio_name='-', note_name = emotion_max.name, note_emoji=emotion_max.emoji)
            final_audio_note.save()
        else:
            for audioResult in audioResult:
                audioResult.note_name = emotion_max.name
                audioResult.note_emoji = emotion_max.emoji
                audioResult.save()
                
class PostAnnotationAPIView(generics.ListCreateAPIView):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    permission_classes = [permissions.IsAuthenticated]
    paginator = None
    
    def create(self, request, *args, **kwargs):
        audio_annotate = Audio.objects.get(id=self.request.data["audio"])
        
        if(audio_annotate is not None):
            audio_annotate.numAnnotate+= 1
            audio_annotate.save()
        response = super().create(request, *args, **kwargs)

        if audio_annotate.numAnnotate == 5:
            
            # Calcul donne chaque annotations et leur nombre par ordre decroissant du nombre
            annotation_compte = Annotation.objects.filter(audio=audio_annotate).values(
                'emotion').order_by().annotate(emotion_count=Count('emotion')).order_by('-emotion_count')

            if len(annotation_compte)!= 0:
                if len(annotation_compte) == 1: # si on une seul note c'est l'annotion maximale

                    emotion_max = Emotion.objects.get(id=annotation_compte[0]["emotion"])
                    final_audio_note = AudioResultAnnotation(
                    audio=audio_annotate, audio_name='-', note_name = emotion_max.name, note_emoji=emotion_max.emoji)
                    final_audio_note.save()

                else: # si on plus d'une note pour l'audio: les deux premier son les maximun
                    a1 = annotation_compte[0]
                    a2 = annotation_compte[1]
                    
                    if a1['emotion_count'] == a2['emotion_count']: 
                            # Filter annotations based on the first element of annotation_compte
                        annotation_profil_a1 = Annotation.objects.filter(
                            audio=audio_annotate,emotion=a1["emotion"],user__job="Illiterate"
                        ).values('user__job').annotate(emotion_count=Count('user__job')).order_by('-emotion_count')

                        annotation_profil_a2 = AnnotationVideo.objects.filter(
                            audio=audio_annotate,emotion=a2["emotion"],user__job="Illiterate"
                        ).values('user__job').annotate(emotion_count=Count('user__job')).order_by('-emotion_count')

                        # Get the count of Illiterate occurrences directly from the query
                        cpt1 = annotation_profil_a1[0]['emotion_count'] if annotation_profil_a1 else 0

                        # Get the count of Illiterate occurrences directly from the query
                        cpt2 = annotation_profil_a2[0]['emotion_count'] if annotation_profil_a2 else 0

                        if cpt1 > cpt2:
                            self.note_final_save(a1, audio_annotate)
                        elif cpt2 > cpt1:
                            self.note_final_save(a2, audio_annotate)
                        else :
                            audio_annotate.numAnnotate =0
                            audio_annotate.save()
                    else:
                        # sinon la note 1 est le maximun
                        self.note_final_save(a1, audio_annotate)
        return response

    def note_final_save(self, arg0, audio_annotate):
        emotion_max = Emotion.objects.get(id=arg0["emotion"])
        final_audio_note = AudioResultAnnotation(
        audio=audio_annotate, audio_name='-', note_name = emotion_max.name, note_emoji=emotion_max.emoji)
        final_audio_note.save()
class AudioAnnotationFinalListAPIView(generics.ListCreateAPIView):
    queryset = AudioResultAnnotation.objects.all()
    serializer_class = AudioResultAnnotationSerializer
    permission_classes = [permissions.IsAuthenticated]
    paginator = None


list_create_final_note_audioAPIView = AudioAnnotationFinalListAPIView.as_view()
#----------------------------- Gestion des Videos ----------------------------

class HomeVideoAPIView(generics.ListCreateAPIView):
    '''
        View: get, post Video
        liste des Video annoter par l'utilisateur et non par l'utilisateur
    '''
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    paginator = None
list_create_VideoPIVIEW = HomeVideoAPIView.as_view()

class AnnotationVideoUserAPIView(generics.ListCreateAPIView):
    # queryset = Video.objects.all()
    # serializer_class = AnnotationVideoSerializer
    # permission_classes = [permissions.IsAuthenticated]
    # paginator = None

    serializer_class = AnnotationVideoSerializer
    permission_classes = [permissions.IsAuthenticated]
    #paginator = None  #switch on the pagination
    
    def get_queryset(self):
        # Retourne 5 audio de meme langage que l'utilisateur conncete et dont le 
        # nombre de fois que l'audio a été annoté n'a pas atteint 5   
    
        limit_Annotation_Num = 5
        user = self.request.user
        
        # Audio.objects.filter(language__language=user.language)\
        #         .annotate(num_annotators=Count('annotations__user',
        #                 filter=Q(annotations__user__job=user.job)))\
        #         .filter(numAnnotate__lte=limit_Annotation_Num)
        
        return  Video.objects.filter(language__language = user.language,
                    numAnnotate__lte=limit_Annotation_Num)


class RetUpdateDelVIDEOHome(generics.RetrieveUpdateDestroyAPIView):
    '''
        View pour put, patch, delete des Audio 
    '''
    queryset = Video.objects.all()
    serializer_class   = VideoSerializer
    permission_classes = [permissions.IsAdminUser]
ret_upate_del_VideoView= RetUpdateDelVIDEOHome.as_view()




#-------------------- geolocalisation --------------------
class CoordinateAPIView(generics.ListCreateAPIView):
    queryset = Coordinate.objects.all()
    serializer_class = CoordinateSerializer
    permission_classes = [permissions.IsAuthenticated]
    paginator = None
    
add_list_location = CoordinateAPIView.as_view()


class CoordinateUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Coordinate.objects.all()
    serializer_class = CoordinateSerializer
    permission_classes = [permissions.IsAuthenticated]
    paginator = None
update_location = CoordinateUpdateAPIView.as_view()

from rest_framework.response import Response

class AudioLocationSetAPIView(generics.RetrieveAPIView):
    queryset = Coordinate.objects.all()
    serializer_class = CoordinateSerializer
    permission_classes = [permissions.IsAuthenticated]
    paginator = None
    
    def retrieve(self, request, *args, **kwargs):
        audio_id = self.kwargs.get('audio')  
        try:
            coordinate = Coordinate.objects.get(localisation__id=audio_id)
            serializer = self.get_serializer(coordinate)
            return Response(serializer.data)

        except Coordinate.DoesNotExist:
            return Response({"error": "Coordinate not found."}, status=404)
retrieve_audio_location = AudioLocationSetAPIView.as_view()

#--------------- Geolocalisation des videos ------------------------

class CoordinateVideoAPIView(generics.ListCreateAPIView):
    queryset = CoordinateVideo.objects.all()
    serializer_class = CoordinateVideoSerializer
    permission_classes = [permissions.IsAuthenticated]
    paginator = None
    
add_list_locationVideo = CoordinateVideoAPIView.as_view()



class CoordinateVideoUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CoordinateVideo.objects.all()
    serializer_class = CoordinateVideoSerializer
    permission_classes = [permissions.IsAuthenticated]
    paginator = None
update_locationVideo = CoordinateVideoUpdateAPIView.as_view()


from rest_framework.response import Response
class VideoLocationSetAPIView(generics.RetrieveAPIView):
    queryset = CoordinateVideo.objects.all()
    serializer_class = CoordinateVideoSerializer
    permission_classes = [permissions.IsAuthenticated]
    paginator = None
    
    def retrieve(self, request, *args, **kwargs):
        video_id = self.kwargs.get('video')  
        try:
            coordinate = CoordinateVideo.objects.get(localisation__id=video_id)
            serializer = self.get_serializer(coordinate)
            return Response(serializer.data)

        except CoordinateVideo.DoesNotExist:
            return Response({"error": "Coordinate not found."}, status=404)
retrieve_video_location = VideoLocationSetAPIView.as_view()

# --------------------- Post and update annotation video --------------------------------------

class PostAnnotationVideoAPIView(generics.ListCreateAPIView):
    queryset = AnnotationVideo.objects.all()
    serializer_class = AnnotationVSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        video_annotate = Video.objects.get(id=self.request.data["video"])
        # print(self.request.data["video"])
        if(video_annotate is not None):
            video_annotate.numAnnotate+= 1
            video_annotate.save()
        response = super().create(request, *args, **kwargs)

        if video_annotate.numAnnotate == 5:
            
            # Calcul donne chaque annotations et leur nombre par ordre decroissant du nombre
            annotation_compte = AnnotationVideo.objects.filter(video=video_annotate).values(
                'emotion').order_by().annotate(emotion_count=Count('emotion')).order_by('-emotion_count')
            
            
            # print(annotation_compte)
            if len(annotation_compte)!= 0:
                if len(annotation_compte)== 1: # si on une seul note c'est l'annotion maximale

                    emotion_max = Emotion.objects.get(id=annotation_compte[0]["emotion"])
                    final_video_note = VideoResultAnnotation(
                    video=video_annotate, video_name='_', note_name = emotion_max.name, note_emoji=emotion_max.emoji)
                    final_video_note.save()

                else: # si on plus d'une note pour l'video: les deux premier son les maximun
                    a1 = annotation_compte[0]
                    a2 = annotation_compte[1]
                                      
                    if a1['emotion_count'] == a2['emotion_count']: 
                         # Filter annotations based on the first element of annotation_compte
                        annotation_profil_a1 = AnnotationVideo.objects.filter(
                            video=video_annotate,
                            emotion=a1["emotion"],user__job="Illiterate"
                        ).values('user__job').annotate(emotion_count=Count('user__job')).order_by('-emotion_count')

                        annotation_profil_a2 = AnnotationVideo.objects.filter(
                            video=video_annotate,
                            emotion=a2["emotion"],user__job="Illiterate"
                        ).values('user__job').annotate(emotion_count=Count('user__job')).order_by('-emotion_count')

                        # Get the count of Illiterate occurrences directly from the query
                        cpt1 = annotation_profil_a1[0]['emotion_count'] if annotation_profil_a1 else 0

                        # Get the count of Illiterate occurrences directly from the query
                        cpt2 = annotation_profil_a2[0]['emotion_count'] if annotation_profil_a2 else 0

                        if cpt1 > cpt2:
                            self.note_final_save(a1, video_annotate)
                        elif cpt2 > cpt1:
                            self.note_final_save(a2, video_annotate)
                        else :
                            video_annotate.numAnnotate =0
                            video_annotate.save()

                    else:
                        # sinon la note 1 est le maximun
                        self.note_final_save(a1, video_annotate)
        return response

    def note_final_save(self, arg0, video_annotate):

        print("Hello")
        emotion_max = Emotion.objects.get(id=arg0["emotion"])
        final_video_note = VideoResultAnnotation(
        video=video_annotate, video_name='', note_name = emotion_max.name, note_emoji=emotion_max.emoji)
        final_video_note.save()


class UpdateAnnotationVideoAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AnnotationVideo.objects.all()
    serializer_class = AnnotationVSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def patch(self, request, *args, **kwargs):
        video_annotate = Video.objects.get(id=self.request.data["video"])
        response = super().patch(request, *args, **kwargs)
        
        # calcul et enregistrement de l'annotation maximal pour l'video
        if video_annotate.numAnnotate == 5:
            # Calcul donne chaque annotations et leur nombre par ordre decroissant du nombre
            annotation_compte = AnnotationVideo.objects.filter(video=video_annotate).values(
                'emotion').order_by().annotate(emotion_count=Count('emotion')).order_by('-emotion_count')
                # recupere l'video concerne par l'annotation
            
            if len(annotation_compte)!= 0:
                if len(annotation_compte)== 1: # si on une seul note c'est l'annotion maximale
                    self.note_final_update(annotation_compte[0]["emotion"], video_annotate)
                else: # si on plus d'une note pour l'video: les deux premier son les maximun
                    a1 = annotation_compte[0]
                    a2 = annotation_compte[1]
                    if a1['emotion_count'] == a2['emotion_count']: 
                        # si on deux annotations differentes qui sont maximal 
                          # Filter annotations based on the first element of annotation_compte
                        annotation_profil_a1 = AnnotationVideo.objects.filter(
                            video=video_annotate,
                            emotion=a1["emotion"],user__job="Illiterate"
                        ).values('user__job').annotate(emotion_count=Count('user__job')).order_by('-emotion_count')

                        annotation_profil_a2 = AnnotationVideo.objects.filter(
                            video=video_annotate,
                            emotion=a2["emotion"],user__job="Illiterate"
                        ).values('user__job').annotate(emotion_count=Count('user__job')).order_by('-emotion_count')

                        # Get the count of Illiterate occurrences directly from the query
                        cpt1 = annotation_profil_a1[0]['emotion_count'] if annotation_profil_a1 else 0

                        # Get the count of Illiterate occurrences directly from the query
                        cpt2 = annotation_profil_a2[0]['emotion_count'] if annotation_profil_a2 else 0

                        if cpt1 > cpt2:
                            self.note_final_save(a1, video_annotate)
                        elif cpt2 > cpt1:
                            self.note_final_save(a2, video_annotate)
                        else :
                            video_annotate.numAnnotate =0
                            video_annotate.save()
                    else:
                        # sinon la note 1 est le maximun
                        self.note_final_update(a1, video_annotate)
        return response
    
    def note_final_update(self, arg0, video_annotate):
        emotion_max = Emotion.objects.get(id=arg0["emotion"])
        videoResult = VideoResultAnnotation.objects.filter(video=video_annotate)
        if len(videoResult)==0:
                final_video_note = VideoResultAnnotation(
                video=video_annotate, video_name='', note_name = emotion_max.name, note_emoji=emotion_max.emoji)
                final_video_note.save()
        else:
            for dt in videoResult:
                dt.note_name = emotion_max.name
                dt.note_emoji = emotion_max.emoji
                dt.save()
      


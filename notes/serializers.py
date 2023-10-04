from rest_framework import serializers
from .models import *

class AudioSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = Audio
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = Video
        fields = '__all__'

class EmotionSerializer(serializers.ModelSerializer):

    class Meta:
        model= Emotion
        fields = '__all__'

class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = '__all__'

class AnnotationVSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnotationVideo
        fields = '__all__'

class AudioResultAnnotationSerializer(serializers.ModelSerializer):
    audio_name_ = serializers.SerializerMethodField() 
    audio_language = serializers.SerializerMethodField() 
    numAnnotation = serializers.SerializerMethodField() 
    
    class Meta:
        model = AudioResultAnnotation
        fields = ('note_name', 'note_emoji', 'audio_name_','audio_language', 'numAnnotation','creation_date')
    
    def get_audio_name_(self, obj):
        return f'{obj.audio.path}'
    
    def get_audio_language(self, obj):
        return f'{obj.audio.language}'
    
    def get_numAnnotation(self, obj):
        return f'{obj.audio.numAnnotate}'
    
class EmotionInlineSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    emoji=serializers.CharField(read_only=True)
    
class AnnotationInlineSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    emotion=EmotionInlineSerializer()

class AnnotationAudioSerializer(serializers.ModelSerializer):
    annotation = serializers.SerializerMethodField(read_only=True)
    language = serializers.SerializerMethodField() 
    
    class Meta:
        model = Audio
        fields = ('id','number', 'path','language', 'numAnnotate','annotation', 'annotations')
    
    def get_language(self, obj):
        return f'{obj.language.language}'
    
    def get_annotation(self, obj):
        request = self.context.get("request")
        user = request.user if request and hasattr(request, "user") else None
        data = Annotation.objects.filter(audio=obj,user=user)
        data = AnnotationInlineSerializer(data, many=True).data

        return data[0] if len(data)!=0 else None


class AnnotationVideoSerializer(serializers.ModelSerializer):
    annotation = serializers.SerializerMethodField(read_only=True)
    language = serializers.SerializerMethodField() 
    
    class Meta:
        model = Video
        fields = ('id', 'number','path','language', 'numAnnotate','annotation', 'annotations')
    
    def get_language(self, obj):
        return f'{obj.language.language}'
    
    def get_annotation(self, obj):
        request = self.context.get("request")
        user = request.user if request and hasattr(request, "user") else None
        data = AnnotationVideo.objects.filter(video=obj,user=user)
        data = AnnotationInlineSerializer(data, many=True).data

        return data


# ---------------------- geolocation ----------------

class CoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Coordinate
        fields = '__all__'

class CoordinateVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = CoordinateVideo
        fields = '__all__'

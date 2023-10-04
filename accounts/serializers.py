from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError

from .models import User
from .models import Language

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)
    job = serializers.CharField(max_length=250)
    gender = serializers.BooleanField( default=True)
    # language = LanguageSerializer()
    
    class Meta:
        model = User
        fields = [
            "email", "username", "password", "first_name", "job",
            "gender", "last_name", "language"
        ]

    def validate(self, attrs):

        if email_exists := User.objects.filter(email=attrs["email"]).exists():
            raise ValidationError("Email has already been used")

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = super().create(validated_data)

        user.set_password(password)

        user.save()

        Token.objects.create(user=user)

        return user

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =[ 'id']
        
class CurrentUserPostsSerializer(serializers.ModelSerializer):
    annotations = serializers.HyperlinkedRelatedField(
        many=True, view_name="annotation_detail", queryset=User.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "annotations"]

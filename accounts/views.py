from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .tokens import create_jwt_pair_for_user
from .models import Language


class LanguageAPIView(generics.ListCreateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    paginator = None
list_create_language = LanguageAPIView.as_view()


class RetUpdateDelLanguage(generics.RetrieveUpdateDestroyAPIView):

    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [permissions.IsAdminUser]
ret_upate_del_LanguageView = RetUpdateDelLanguage.as_view()

#### ---------------Authentification -------------------###
class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = []

    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response = {"message": "User Created Successfully", "data": serializer.data}

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = []

    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is None:
            return Response(data={"message": "Invalid email or password"})
        
        tokens = create_jwt_pair_for_user(user)
        response = {"message": "Login Successfull", "tokens": tokens}

        print(request.data)
        
        return Response(data=response, status=status.HTTP_200_OK)

    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}

        return Response(data=content, status=status.HTTP_200_OK)

class UserListAPIView(generics.ListAPIView):
    
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]
    paginator = None
    
    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.filter(id=user.id)
        return queryset



from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views

urlpatterns = [
    path("language/", view=views.list_create_language, name="create_language"),
    path("language/<int:pk>/detail/", views.ret_upate_del_LanguageView, name="update_language"),
    
    path("user/list/", views.UserListAPIView.as_view(), name='user_list'),
    
    #   authentication 
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("jwt/create/", TokenObtainPairView.as_view(), name="jwt_create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
    
    path('auth/google/', views.google_auth, name='google_auth'),
]

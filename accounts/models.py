from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")

        return self.create_user(email=email, password=password, **extra_fields)


# user table
class Language(models.Model):
    """
            class des langue locaux
    """
    
    language=models.CharField(max_length=250)
    creation_date = models.DateTimeField( auto_now_add=True)
    
    class Meta:
        ordering = ['language','-creation_date']
    
    def __str__(self) -> str:
        return f'{self.language}'
    
    
class User(AbstractUser):
    email = models.CharField(max_length=80, unique=True)
    username = models.CharField(max_length=45)
    
    job=models.CharField(max_length=250)
    gender=models.BooleanField( default=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    language=models.ForeignKey(Language, related_name="users", on_delete=models.DO_NOTHING, null=True)

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        ordering = ['username','email']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

from django.db import models
from projects.models import Skill, Project

class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError("Email address is required")
        if not password:
            raise ValueError("Password is required")
           
        user = self.model(
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.save()
        return user
       
    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user
    
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.id, filename)
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=50)
    about = models.TextField(blank=True)
    avatar = models.ImageField(blank=True, null=True,
                               upload_to=user_directory_path)
    skills = models.ManyToManyField(Skill)
    projects = models.ManyToManyField(Project)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    
    


    

    
    
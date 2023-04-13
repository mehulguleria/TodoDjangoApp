from random import randint

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)

class UserManager(BaseUserManager):

    def create_user(self,email,password=None,**kwargs):
        if not email:
            raise ValueError("Email Required")
        
        user = self.model(email=self.normalize_email(email),verify=randint(100000,999999),**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password):
        print('start superuser')
        user = self.create_user(email,password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using = self._db)
    
class User(AbstractBaseUser,PermissionsMixin):

    email = models.EmailField(max_length=100,unique=True,null=False)
    name = models.CharField(max_length=100)
    verify = models.IntegerField()
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
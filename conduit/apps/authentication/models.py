import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManger(BaseUserManager):
    """
    custom manger for our new User Model, we override both create_user and
    create_super_user method

    """

    def create_user(self,username,email,password=None):
        """
        create and return a user with an email and username
        """
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username,email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self,username,email,password):
        """
         create and return user with spueruser permisson
        """
        if password is None:
            raise TypeError('Super user must have a password')

        user =self.create_user(username,email,password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

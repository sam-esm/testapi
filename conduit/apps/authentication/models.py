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

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model which use email to logging in
    """
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManger()

    def __str__(self):
        """
        Returns a string representation of this `User`.
        we return email of user
        """
        return self.email

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        },settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')


    def get_full_name(self):
        """
        since we dont store name and family name so we return username instead
        """
        return self.username

    def get_short_name(self):

        """
        since we dont store name and so we return username instead

        """
        return self.username

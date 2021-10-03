from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.
class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=100, blank=True, null=True)
    nickname = models.CharField(max_length=30, blank=True, null=True)
    thumbnail = models.CharField(max_length=256, blank=True, null=True)

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.nickname

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table = 'users'

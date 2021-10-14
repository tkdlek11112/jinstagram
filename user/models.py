from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.
class User(AbstractBaseUser):
    name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(verbose_name='email', max_length=100, blank=True, null=True, unique=True)
    user_id = models.CharField(max_length=30, blank=True, null=True)
    thumbnail = models.CharField(max_length=256, default='default_profile.jpg', blank=True, null=True)

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['user_id']

    def __str__(self):
        return self.user_id

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table = 'users'


class Follow(models.Model):
    follower = models.EmailField(verbose_name='email', max_length=100)
    following = models.EmailField(verbose_name='email', max_length=100)
    is_live = models.BooleanField(default=False)

    class Meta:
        db_table = 'follow'
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'], name='follower-following')
        ]
        indexes = [
            models.Index(fields=['follower']),
            models.Index(fields=['following']),
        ]

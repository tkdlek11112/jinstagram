from django.db import models


# Create your models here.
class Feed(models.Model):
    content = models.TextField()
    image = models.TextField()
    profile_image = models.TextField()
    email = models.EmailField(verbose_name='email', max_length=100, blank=True, null=True)
    user_id = models.CharField(max_length=30, blank=True, null=True)
    like_count = models.IntegerField()


class Reply(models.Model):
    feed_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.CharField(max_length=30, blank=True, null=True)
    content = models.TextField()
    email = models.EmailField(verbose_name='email', max_length=100, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['feed_id'])
        ]


class FeedLike(models.Model):
    feed_id = models.IntegerField()
    email = models.CharField(max_length=30, blank=True, null=True)
    is_like = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['feed_id']),
            models.Index(fields=['email']),
        ]

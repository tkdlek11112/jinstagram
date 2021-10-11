from django.urls import path
from .views import UploadFeed, CreateReply


urlpatterns = [
    path('upload', UploadFeed.as_view(), name='upload_feed'),
    path('reply/create', CreateReply.as_view(), name='reply_create'),
]


from django.urls import path
from .views import UploadFeed, CreateReply, LikeFeed, BookmarkFeed


urlpatterns = [
    path('upload', UploadFeed.as_view(), name='upload_feed'),
    path('reply/create', CreateReply.as_view(), name='reply_create'),
    path('like', LikeFeed.as_view(), name='like'),
    path('bookmark', BookmarkFeed.as_view(), name='bookmark'),
]


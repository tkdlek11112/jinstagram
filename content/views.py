from django.shortcuts import render
from rest_framework.views import APIView
from content.models import Feed, Reply, FeedLike, Bookmark
from rest_framework.response import Response
from user.models import User
from rest_framework.response import Response
import os
from jinstagram.settings import MEDIA_ROOT
from uuid import uuid4
from datetime import datetime


class UploadFeed(APIView):
    def post(self, request):
        file = request.FILES['file']
        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        content = request.data.get('content')
        image = uuid_name
        profile_image = request.data.get('profile_image')
        user_id = request.data.get('user_id')
        email = request.data.get('email')
        Feed.objects.create(content=content, image=image, profile_image=profile_image, user_id=user_id, email=email, like_count=0)
        return Response(status=200)


class LikeFeed(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id')
        email = request.data.get('email')
        is_like = request.data.get('is_like', 'True')

        if is_like.lower() == 'false':
            is_like = False
        else:
            is_like = True
        feed_like = FeedLike.objects.filter(feed_id=feed_id, email=email).first()

        if feed_like is None:
            FeedLike.objects.create(feed_id=feed_id,
                                    email=email,
                                    is_like=is_like,
                                    )
        else:
            feed_like.is_like = is_like
            feed_like.save()

        return Response(status=200, data=dict(message='피드 좋아요 완료.'))


class CreateReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id')
        user_id = request.data.get('user_id')
        content = request.data.get('content')
        email = request.data.get('email')
        Reply.objects.create(feed_id=feed_id,
                             user_id=user_id,
                             content=content,
                             email=email
                             )

        return Response(status=200, data=dict(message='댓글 작성 완료.'))


class DeleteReply(APIView):
    def post(self, request):
        reply_id = request.data.get('reply_id')
        email = request.data.get('email')

        reply = Reply.objects.filter(id=reply_id).first()

        if reply is None:
            return Response(status=500, data=dict(message='삭제 실패'))

        if reply.email == email:
            reply.delete()
            return Response(status=200, data=dict(message='성공'))
        else:
            return Response(status=500, data=dict(message='삭제 실패'))


class BookmarkFeed(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id')
        email = request.data.get('email')
        is_bookmarked = request.data.get('is_bookmarked', 'True')

        if is_bookmarked.lower() == 'false':
            is_bookmarked = False
        else:
            is_bookmarked = True
        bookmark = Bookmark.objects.filter(feed_id=feed_id, email=email).first()

        if bookmark is None:
            Bookmark.objects.create(feed_id=feed_id,
                                    email=email,
                                    is_bookmarked=is_bookmarked,
                                    )
        else:
            bookmark.is_bookmarked = is_bookmarked
            bookmark.save()

        return Response(status=200, data=dict(message='북마크 설정 완료.'))

from django.shortcuts import render
from rest_framework.views import APIView
from content.models import Feed, Reply
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
        is_like = request.data.get('is_like', True)

        Reply.objects.create(feed_id=feed_id,
                             email=email,
                             is_like=is_like,
                             )

        return Response(status=200, data=dict(message='성공'))


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

        return Response(status=200, data=dict(message='성공'))


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

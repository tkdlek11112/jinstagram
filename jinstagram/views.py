from django.shortcuts import render
from rest_framework.views import APIView
from content.models import Feed
from rest_framework.response import Response
import os
from .settings import MEDIA_ROOT
from uuid import uuid4
from datetime import datetime


class Main(APIView):
    def get(self, request):
        feed_list = Feed.objects.all().order_by('-id')
        return render(request, 'jinstagram/main.html', context=dict(feed_list=feed_list))


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

        Feed.objects.create(content=content, image=image, profile_image=profile_image, user_id=user_id, like_count=0)

        return Response(status=200)


class Login(APIView):
    def get(self, request):
        return render(request, 'user/login.html')

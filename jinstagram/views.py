from django.shortcuts import render
from rest_framework.views import APIView
from content.models import Feed, Reply, FeedLike
from user.models import User


class Main(APIView):
    def get(self, request):
        email = request.session.get('email', None)
        if email is None:
            return render(request, 'user/login.html')

        user = User.objects.filter(email=email).first()
        if user is None:
            return render(request, 'user/login.html')

        feed_object_list = Feed.objects.all().order_by('-id')
        feed_list = []
        for feed in feed_object_list:
            like_count = FeedLike.objects.filter(feed_id=feed.id, is_like=True).count()
            is_like = FeedLike.objects.filter(feed_id=feed.id, is_like=True, email=email).exists()
            reply_list = Reply.objects.filter(feed_id=feed.id)
            profile_image = User.objects.filter(email=email).first().thumbnail or 'default_profile.jpg'
            feed_list.append(dict(
                id=feed.id,
                profile_image=profile_image,
                user_id=feed.user_id,
                image=feed.image,
                content=feed.content,
                like_count=like_count,
                is_like=is_like,
                reply_list=reply_list

            ))

        return render(request,
                      'jinstagram/main.html',
                      context=dict(feed_list=feed_list,
                                   user=user))


class Profile(APIView):
    def get(self, request):
        email = request.session.get('email', None)
        if email is None:
            return render(request, 'user/login.html')

        user = User.objects.filter(email=email).first()
        if user is None:
            return render(request, 'user/login.html')

        feed_object_list = Feed.objects.filter(email=email).order_by('-id')
        print(feed_object_list)
        print(email)
        feed_list = []
        row_feed_list = []
        for feed in feed_object_list:
            like_count = FeedLike.objects.filter(feed_id=feed.id, is_like=True).count()
            is_like = FeedLike.objects.filter(feed_id=feed.id, is_like=True, email=email).exists()
            reply_list = Reply.objects.filter(feed_id=feed.id)
            row_feed_list.append(dict(
                id=feed.id,
                profile_image=feed.profile_image,
                user_id=feed.user_id,
                image=feed.image,
                content=feed.content,
                like_count=like_count,
                is_like=is_like,
                reply_list=reply_list
            ))

            if len(row_feed_list) == 3:
                feed_list.append(dict(row_feed_list=row_feed_list))
                row_feed_list = []

        if len(row_feed_list) > 0:
            feed_list.append(dict(row_feed_list=row_feed_list))

        return render(request,
                      'jinstagram/profile.html',
                      context=dict(feed_list=feed_list,
                                   user=user))

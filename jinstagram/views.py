from django.shortcuts import render
from rest_framework.views import APIView
from content.models import Feed, Reply, FeedLike, Bookmark
from user.models import User, Follow


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
            is_bookmarked = Bookmark.objects.filter(email=email, is_bookmarked=True, feed_id=feed.id).exists()
            reply_list = Reply.objects.filter(feed_id=feed.id)
            profile_image = User.objects.filter(email=feed.email).first().thumbnail or 'default_profile.jpg'
            feed_list.append(dict(
                id=feed.id,
                profile_image=profile_image,
                user_id=feed.user_id,
                image=feed.image,
                content=feed.content,
                like_count=like_count,
                is_like=is_like,
                reply_list=reply_list,
                is_bookmarked=is_bookmarked
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
        feed_list = []
        row_feed_list = []
        feed_count = feed_object_list.count()
        for feed in feed_object_list:
            like_count = FeedLike.objects.filter(feed_id=feed.id, is_like=True).count()
            is_like = FeedLike.objects.filter(feed_id=feed.id, is_like=True, email=email).exists()
            reply_count = Reply.objects.filter(feed_id=feed.id).count()
            row_feed_list.append(dict(
                id=feed.id,
                profile_image=feed.profile_image,
                user_id=feed.user_id,
                image=feed.image,
                content=feed.content,
                like_count=like_count,
                is_like=is_like,
                reply_count=reply_count
            ))

            if len(row_feed_list) == 3:
                feed_list.append(dict(row_feed_list=row_feed_list))
                row_feed_list = []

        if len(row_feed_list) > 0:
            feed_list.append(dict(row_feed_list=row_feed_list))

        following_count = Follow.objects.filter(follower=email, is_live=True).count()
        follower_count = Follow.objects.filter(following=email, is_live=True).count()

        bookmark_list = Bookmark.objects.filter(email=email, is_bookmarked=True).order_by('-id')
        bookmark_feed_list = []
        row_bookmark_feed_list = []
        for bookmark in bookmark_list:
            feed = Feed.objects.filter(id=bookmark.feed_id).first()
            if feed is None:
                continue
            like_count = FeedLike.objects.filter(feed_id=feed.id, is_like=True).count()
            is_like = FeedLike.objects.filter(feed_id=feed.id, is_like=True, email=email).exists()
            reply_count = Reply.objects.filter(feed_id=feed.id).count()
            row_bookmark_feed_list.append(dict(
                id=feed.id,
                profile_image=feed.profile_image,
                user_id=feed.user_id,
                image=feed.image,
                content=feed.content,
                like_count=like_count,
                is_like=is_like,
                reply_count=reply_count
            ))

            if len(row_bookmark_feed_list) == 3:
                bookmark_feed_list.append(dict(row_bookmark_feed_list=row_bookmark_feed_list))
                row_bookmark_feed_list = []

        if len(row_bookmark_feed_list) > 0:
            bookmark_feed_list.append(dict(row_bookmark_feed_list=row_bookmark_feed_list))

        return render(request,
                      'jinstagram/profile.html',
                      context=dict(feed_list=feed_list,
                                   bookmark_feed_list=bookmark_feed_list,
                                   feed_count=feed_count,
                                   following_count=following_count,
                                   follower_count=follower_count,
                                   user=user))

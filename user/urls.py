from django.urls import path
from .views import Login, Join, LogOut, UpdateProfile


urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('logout', LogOut.as_view(), name='logout'),
    path('join', Join.as_view(), name='join'),
    path('profile/update', UpdateProfile.as_view(), name='profile_update'),
]


from django.urls import path
from .views import *

app_name = 'video'





urlpatterns = [
    path('', index, name='index'),
    path('upload/<str:slug>', video_upload, name='video_upload'),
    path('movie/<str:slug>', video, name='show'),
    path('movie/create/', create_movie, name='create-movie'),



    path('play-list/<str:slug>', playLists, name='play-list'),
    path('play-list/create/', playListCreate, name='create-play-list'),
    path('play-lists/', lists, name='lists')
]

from django.urls import path
from .views import *





urlpatterns = [
    path('', index, name='index'),
    path('dashboard', dashboard, name='dashboard'),
    path('upload/<str:slug>', video_upload, name='video_upload'),
    path('movie/<str:slug>', video, name='show'),
    path('movie/create/', create_movie, name='create-movie'),
    path('movies/', movies, name='movies'),



    path('play-list/<str:slug>', playLists, name='play-list'),
    path('play-list/create/', playListCreate, name='create-play-list'),
    path('play-lists/', lists, name='lists'),
    path('movie/update/<str:slug>', MovieUpdateView.as_view(), name='movie-update'),
    path('video/delete/<int:id>', deleteVideo, name='delete-video')
]

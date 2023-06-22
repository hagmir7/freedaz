from django.urls import path
from .views import *


urlpatterns = [
   
    
]



urlpatterns = [
    path('categories', categories, name='categories'),
    path('series/', SerieListView.as_view(), name='serie-list'),
    path('playlists/', PlayListView.as_view(), name='playlist-list'),
    path('movies/', MovieListView.as_view(), name='movie-list'),
    path('videos/', VideoListView.as_view(), name='video-list'),
    path('comments/', CommentListView.as_view(), name='comment-list'),
]

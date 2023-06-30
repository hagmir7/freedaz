from django.urls import path
from .views import *
from .sites.wecima import *
from .sites.top import *
from .sites.best import *
from .sites.new import *



urlpatterns = [
    path('', index, name='index'),
    path('menu', menu, name='menu'),
    path('dashboard', dashboard, name='dashboard'),
    path('upload/<str:slug>', video_upload, name='video_upload'),
    path('movie/<str:slug>', video, name='show'),
    path('movie/create/', create_movie, name='create-movie'),
    path('movies/new/', new_movies, name='movies_new'),
    path('movies/best', best_movies, name='movies_best'),
    path('movie/delete/<int:id>', delete_movie, name='delete_movie'),



    path('play-list/<str:slug>', playLists, name='play-list'),
    path('play-list/create/', playListCreate, name='create-play-list'),
    path('play-lists/', lists, name='lists'),
    path('movie/update/<str:slug>', MovieUpdateView.as_view(), name='movie-update'),
    path('video/delete/<int:id>', deleteVideo, name='delete-video'),



    path('category/create/', create_category, name='create-category'),
    path('category/list/', categoryList, name='list-category'),
    path('category/update/<int:id>/', update_category, name='update-category'),
    path('category/delete/<int:id>/', delete_category, name='delete-category'),
    path('category/<str:slug>/', category, name='view-category'),


    path('serie/create/', create_serie, name='serie_create'),
    path('serie/update/<int:id>/', update_serie, name='serie_update'),
    path('serie/delete/<int:id>/', delete_serie, name='serie_delete'),
    path('serie/list/', serie_list, name='serie_list'),
    path('serie/<slug:slug>/', serie, name='serie_detail'),

    path('episode/create', create_episode, name="create_episode"),

    path('wecima', wecima),
    path('top', top),
    path('best', best),
    path('new', new)

]

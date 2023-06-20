from django.urls import path
from .views import *

app_name = 'video'





urlpatterns = [
    path('', index, name='index'),
    path('upload/', video_upload, name='video_upload'),
    path('<int:id>', video, name='video'),
]

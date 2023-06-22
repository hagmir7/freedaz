from rest_framework import permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from django.core.paginator import Paginator
from video.models import *
from .serializers import *

from rest_framework import generics
from rest_framework.pagination import PageNumberPagination



@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def categories(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category, many=True)
    return Response(serializer.data)



# Define your pagination class
class CustomPagination(PageNumberPagination):
    page_size = 10  # Number of objects to be returned per page
    page_size_query_param = 'page_size'
    max_page_size = 100


# Create your list view
class SerieListView(generics.ListAPIView):
    queryset = Serie.objects.all()
    serializer_class = SerieSerializer
    pagination_class = CustomPagination

class PlayListView(generics.ListAPIView):
    queryset = PlayList.objects.all()
    serializer_class = PlayListSerializer
    pagination_class = CustomPagination

class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = CustomPagination

class VideoListView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    pagination_class = CustomPagination

class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CustomPagination
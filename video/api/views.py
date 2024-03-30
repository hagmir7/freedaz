from rest_framework import permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from django.core.paginator import Paginator
from video.models import *
from .serializers import *

from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
import requests
from bs4 import BeautifulSoup



def remove_first_end_spaces(string):
    return "".join(string.rstrip().lstrip())

def str_cleaner(string :str):
    return string.replace("\r", '')

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def movie_detail(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    
    try:
        scrap = getItem(movie.scraping_url) if movie.scraping_url else []
    except Exception as e:
        scrap = []
    
    return Response(scrap)

def getItem(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    movie_content = soup.find('div', {'class': 'Download--Wecima--Single'})
    movies = movie_content.find_all('a', {'class': 'hoverable'})
    
    quality = []
    for movie in movies:
        quality.append({
            'quality': remove_first_end_spaces(movie.find('resolution').text),
            'url': movie['href']
        })
    
    servers = soup.find('ul', {'class': 'WatchServersList'}).find_all("btn")
    servers_array = []
    for btn in servers:
        servers_array.append({
            'name': btn.find('strong').text,
            'url': str_cleaner(btn["data-url"])
        })
    
    return {
        "qualities" : quality,
        "servers": servers_array
    }

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
    queryset = Movie.objects.all().order_by('-uploaded_at')
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
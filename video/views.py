from django.shortcuts import render, redirect, get_object_or_404
from django_user_agents.utils import get_user_agent
from .forms import *
from .models import *
from django.http import JsonResponse
import requests
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator

def index(request):
    list = Movie.objects.all().order_by('-uploaded_at')
    paginator = Paginator(list, 25) 
    page_number = request.GET.get("page")
    videos = paginator.get_page(page_number)

    context = {
        'videos' : videos,
    }
    return render(request, 'video/index.html', context)


def movies(request):
    list = Movie.objects.filter(episode__isnull=True)
    paginator = Paginator(list, 25) 
    page_number = request.GET.get("page")
    movies = paginator.get_page(page_number)
    context = {
        'movies' : movies,
    }
    return render(request, 'movies.html', context)



def series(request):
    list = PlayList.objects.filter(category__name='Movis')
    paginator = Paginator(list, 25) 
    page_number = request.GET.get("page")
    series = paginator.get_page(page_number)
    context = {
        'series' : series,
    }
    return render(request, 'series.html', context)


def anime(request):
    list = Video.objects.filter(category__name='Anime')
    paginator = Paginator(list, 25) 
    page_number = request.GET.get("page")
    animes = paginator.get_page(page_number)
    context = {
        'animes' : animes,
    }
    return render(request, 'anime.html', context)

def anime_series(request):
    list = PlayList.objects.filter(category__name='Anime')
    paginator = Paginator(list, 25) 
    page_number = request.GET.get("page")
    series = paginator.get_page(page_number)
    context = {
        'series' : series,
    }
    return render(request, 'anime-serise.html', context)




def course(request):
    list = Video.objects.filter(category__name='Course')
    paginator = Paginator(list, 25) 
    page_number = request.GET.get("page")
    series = paginator.get_page(page_number)
    context = {
        'series' : series,
    }
    return render(request, 'anime-serise.html', context)


def course_list(request):
    list = PlayList.objects.filter(category__name='Course')
    paginator = Paginator(list, 25) 
    page_number = request.GET.get("page")
    series = paginator.get_page(page_number)
    context = {
        'series' : series,
    }
    return render(request, 'anime-serise.html', context)



def create_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            movie.save()
            return redirect(f'/upload/{movie.slug}')
    else:
        form = MovieForm()
    return render(request, 'video/create.html', {'form': form})



def video_upload(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.movie = movie
            video.save()
            return JsonResponse({'messsage': "You video uploaded successfully."})
    else:
        form = VideoForm()
    return render(request, 'video/upload.html', {'form': form, 'movie' : movie})







def getLocaction(ip):
    url = f"https://api.ipgeolocation.io/ipgeo?apiKey=2df9c865ff864fb4bcbf81ebbe0386eb&ip={ip}"
    response = requests.get(url)
    return response.json()


def video(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    movies = Movie.objects.all().order_by('-uploaded_at')[0:15]
    episodes = Movie.objects.filter(list=movie.list)

    videos = Video.objects.filter(movie=movie.id)

    agent = get_user_agent(request)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    try:
        if not Location.objects.filter(ip=ip).exists():
            location = Location.objects.create(
                ip=ip,
                user = movie.user,
                os=agent.os[0],
                browser=agent.browser[0],
                country=getLocaction(ip).get('country_name'),
                country_flag=getLocaction(ip).get("country_flag"),
                country_code=getLocaction(ip).get("country_code3"),
                city=getLocaction(ip).get("city"),
            )
        else:
            location = Location.objects.get(ip=ip)

        movie.views.add(location)
        movie.save()
    except:
        pass

    context = {
        'movie' : movie,
        'movies' : movies,
        'title': movie.title,
        'videos': videos,
        'episodes' : episodes
    }
    
    return render(request, 'video/show.html', context)



def playLists(request, slug):
    list = get_object_or_404(PlayList, slug=slug)
    
    ListMovies = Movie.objects.filter(list=list)
    paginator = Paginator(ListMovies, 25) 
    page_number = request.GET.get("page")
    movies = paginator.get_page(page_number)
    context = {
        'list' : list,
        'movies': movies
    }
    return render(request, 'list/show.html', context)

def playListCreate(request):
    if request.method == 'POST':
        form = PlayListForm(request.POST, request.FILES)
        if form.is_valid():
            list = form.save(commit=False)
            list.user = request.user
            list.save()
            return JsonResponse({'message' : "Play list created successfully"})
    else: 
        form = PlayListForm()
    context = {
        'form' : form
    }
    return render(request, 'list/create.html', context)



def lists(request):
    list = PlayList.objects.all()
    paginator = Paginator(list, 25) 
    page_number = request.GET.get("page")
    lists = paginator.get_page(page_number)
    context = {
        'lists' : lists
    }
    return render(request, 'list/list.html', context)





def dashboard(request):

    context = {

    }
    return render(request, 'dashboard.html', context)



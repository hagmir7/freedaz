from django.shortcuts import render, redirect, get_object_or_404
from django_user_agents.utils import get_user_agent
from .forms import *
from .models import *
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.db.models import Q
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db.models import Count




def superuser_required(user):
    if not user.is_superuser:
        raise PermissionDenied
    return True


def duplicated_movies(request):
    # Assuming you have a model named 'YourModel' with a 'title' field
    duplicated_data = PlayList.objects.values('title').annotate(title_count=Count('title')).filter(title_count__gt=1)
    for item in duplicated_data:
            title = item['title']
            duplicates = PlayList.objects.filter(title=title)[1:]  # Exclude the first occurrence
            
            for duplicate in duplicates:
                duplicate.delete()
    context = {
        'movies' : duplicated_data
    }
    return render(request, 'duplicated-movies.html', context)




def index(request):
    list = Movie.objects.all().order_by('-uploaded_at')
    paginator = Paginator(list, 60) 
    page_number = request.GET.get("page")
    videos = paginator.get_page(page_number)

    best_series = PlayList.objects.annotate(views_count=Count('views')).order_by('-views_count')[0:6]
    best_movies = Movie.objects.filter(episode__isnull=True).annotate(views_count=Count('views')).order_by('-views_count')[0:6]

    context = {
        'videos' : videos,
        'best_series' : best_series,
        'best_movies' : best_movies
    }
    return render(request, 'video/index.html', context)



def new_movies(request):
    keywords = request.GET.get('q')
    q = Q()
    if keywords:
        q &= (Q(title__icontains=keywords) | Q(description__icontains=keywords) | Q(tags__icontains=keywords))
        list = Movie.objects.filter(q, episode__isnull=True)
        playList = PlayList.objects.filter(q)
    else:
        list = Movie.objects.filter(episode__isnull=True)
        playList = []
        
    paginator = Paginator(list, 24) 
    page_number = request.GET.get("page")
    movies = paginator.get_page(page_number)
    context = {
        'movies' : movies,
        'lists' : playList
    }
    return render(request, 'movies.html', context)



def best_movies(request):
    list = Movie.objects.filter(episode__isnull=True).annotate(views_count=Count('views')).order_by('-views_count')
    paginator = Paginator(list, 24) 
    page_number = request.GET.get("page")
    movies = paginator.get_page(page_number)
    context = {
        'movies' : movies,
    }
    return render(request, 'movies.html', context)










class MovieUpdateView(View):
    template_name = 'video/create.html'

    def get(self, request, slug):
        movie = Movie.objects.get(slug=slug)
        videos = Video.objects.filter(movie=movie.id)
        form = MovieForm(instance=movie)
        context = {
            'form': form,
            'movie': movie,
            'videos' : videos
        }
        return render(request, self.template_name, context)

    def post(self, request, slug):
        movie = Movie.objects.get(slug=slug)
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            # Redirect to the movie detail page or wherever you want
            return redirect(f'/movie/{movie.slug}')
        return render(request, self.template_name, {'form': form, 'movie': movie})



@user_passes_test(superuser_required)
def deleteVideo(request, id):
    video = get_object_or_404(Video, id=id)
    video.delete()
    messages.success(request, "تم حذف الفيديو بنجاح.")
    return redirect(request.META.get('HTTP_REFERER'))





@user_passes_test(superuser_required)
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


@user_passes_test(superuser_required)
def delete_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    movie.delete()
    messages.success(request, "تم حذف الفلم بنجاج.")
    return redirect('/')



@user_passes_test(superuser_required)
def create_episode(request):
    if request.method == 'POST':
        form = EpisodeForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            movie.save()
            return redirect(f'/upload/{movie.slug}')
    else:
        form = EpisodeForm()
    return render(request, 'video/create.html', {'form': form})


@user_passes_test(superuser_required)
def video_upload(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    videos = Video.objects.filter(movie=movie.id)
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.movie = movie
            video.save()
            messages.success(request, "تم إنشاء المسلسل بنجاح")
            return redirect('create_episode')
    else:
        form = VideoForm()
    context = {
        'form': form,
        'movie' : movie,
        'videos': videos
    }
    return render(request, 'video/upload.html', context)





from bs4 import BeautifulSoup
import re

def getLocaction(ip):
    url = f"https://api.ipgeolocation.io/ipgeo?apiKey=2df9c865ff864fb4bcbf81ebbe0386eb&ip={ip}"
    response = requests.get(url)
    return response.json()



def getItem(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    movie_content = soup.find('div', {'class': 'Download--Wecima--Single'})
    movies = movie_content.find_all('a', {'class': 'hoverable'})

   

    quality = []
    for movie in movies:
        quality.append({
            'quality' : movie.find('resolution').text,
            'url' : movie['href']
        })
    return quality

    


def video(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    episodes = Movie.objects.filter(list=movie.list)

    videos = Video.objects.filter(movie=movie.id)

    list = Movie.objects.annotate(views_count=Count('views')).order_by('-views_count')
    paginator = Paginator(list, 24) 
    page_number = request.GET.get("page")
    movies = paginator.get_page(page_number)

    categories = Category.objects.all()

    agent = get_user_agent(request)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    if not Location.objects.filter(ip=ip).exists():
        location = Location.objects.create(
            ip=ip,
            user = movie.user,
            os=agent.os[0],
            browser=agent.browser[0],
        )
    else:
        location = Location.objects.get(ip=ip)
    if not location in movie.views.all():
        movie.views.add(location)
        movie.save()

    # Scraping Downlaod urls
    if(movie.scraping_url):
        quality = getItem(movie.scraping_url)
    else:
        quality = False
    
    # Get image 
    if movie.image:
        image = movie.image
    elif movie.list:
        if movie.list.image:
            image = movie.list.image
        else:
            image = False
    else:
        image = False

    context = {
        'movie' : movie,
        'movies' : movies,
        'title': movie.title,
        'videos': videos,
        'episodes' : episodes,
        'categories' : categories,
        'quality' : quality,
        'image' : image
    }
   
    return render (request, 'video/show.html', context)



def playLists(request, slug):
    list = get_object_or_404(PlayList, slug=slug)
    
    agent = get_user_agent(request)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    if not Location.objects.filter(ip=ip).exists():
        location = Location.objects.create(
            ip=ip,
            os=agent.os[0],
            browser=agent.browser[0],
        )
    else:
        location = Location.objects.get(ip=ip)
    if not location in list.views.all():
        list.views.add(location)
        list.save()
    
    ListMovies = Movie.objects.filter(list=list)
    paginator = Paginator(ListMovies, 30) 
    page_number = request.GET.get("page")
    movies = paginator.get_page(page_number)
    context = {
        'list' : list,
        'movies': movies
    }
    return render(request, 'list/show.html', context)


@user_passes_test(superuser_required)
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
    list = PlayList.objects.all().order_by('-created_at')
    paginator = Paginator(list, 30) 
    page_number = request.GET.get("page")
    lists = paginator.get_page(page_number)
    context = {
        'lists' : lists
    }
    return render(request, 'list/list.html', context)




@user_passes_test(superuser_required)
def dashboard(request):

    context = {

    }
    return render(request, 'dashboard.html', context)



@user_passes_test(superuser_required)
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "تم إنشاء الصنف بنجاح.")
            return redirect('/category/list/')
    else:
        return redirect('/category/list/')


def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    list = Movie.objects.filter(category__id=category.id)
    paginator = Paginator(list, 24) 
    page_number = request.GET.get("page")
    movies = paginator.get_page(page_number)
    return render(request, 'category/show.html', {'category': category, 'movies': movies})


@user_passes_test(superuser_required)
def categoryList(request):
    categories = Category.objects.all()
    return render(request, 'category/list.html', {'categories': categories})

@user_passes_test(superuser_required)
def update_category(request, id):
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تعديل الصنف بنجاح.")
            return redirect('/category/list/')

    else:
        form = CategoryForm(instance=category)
    return render(request, 'category/update.html', {'form': form})


@user_passes_test(superuser_required)
def delete_category(request, id):
    category = get_object_or_404(Category ,pk=id)
    category.delete()
    return redirect('/category/list')




def menu(request):
    categories = Category.objects.all()
    context = {
        'categories' : categories,
        'title': 'فري داز - القائمة'
    }
    return render(request, 'menu.html', context)


def serie(request, slug):
    serie = get_object_or_404(Serie, slug=slug)
    seasons = serie.playlist_set.all()
    return render(request, 'serie.html', {'serie': serie, 'seasons': seasons})

@user_passes_test(superuser_required)
def create_serie(request):
    if request.method == 'POST':
        form = SerieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم إنشاء المسلسل بنجاح.')
            return redirect('serie_list')
    else:
        form = SerieForm()
    return render(request, 'serie/create.html', {'form': form})


@user_passes_test(superuser_required)
def update_serie(request, id):
    serie = get_object_or_404(Serie, id=id)
    if request.method == 'POST':
        form = SerieForm(request.POST, request.FILES, instance=serie)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تعديل المسلسل بنجاح.')
            return redirect('serie_list')
    else:
        form = SerieForm(instance=serie)
    return render(request, 'serie/update.html', {'form': form, 'serie': serie})

@user_passes_test(superuser_required)
def delete_serie(request, id):
    serie = get_object_or_404(Serie, id=id)
    serie.delete()
    messages.success(request, 'تم حذف الموسم بنجاح')   
    return redirect('/serie/list')


def serie_list(request):
    lsit_series = Serie.objects.all()
    form = SerieForm()
    paginator = Paginator(lsit_series, 10)  # Display 10 series per page

    page_number = request.GET.get('page')
    series = paginator.get_page(page_number)

    return render(request, 'serie/list.html', {'series': series, 'form': form})






from django.shortcuts import render, redirect, get_object_or_404
from django_user_agents.utils import get_user_agent
from .forms import *
from .models import *
from django.http import JsonResponse
import requests
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

def superuser_required(user):
    if not user.is_superuser:
        raise PermissionDenied
    return True







def download_and_save_file(url, quality, slug):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for any errors during the request

        file_temp = NamedTemporaryFile()
        file_temp.write(response.content)
        file_temp.flush()


        video = Video.objects.create(movie=Movie.objects.get(slug=slug))

        with open(file_temp.name, 'rb') as file:
            video.video_file.save('file_name.mp4', File(file))
            video.quality = quality
            video.save()

            

        return video
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while downloading the file: {e}")
        return None

def file(request):
    url = request.GET.get('url')
    result = download_and_save_file(url)
    if result:
        return JsonResponse({"Success": "File Uploaded successfully."})
    else:
        return JsonResponse({"Error": "Fail to Upload File."})


def index(request):
    list = Movie.objects.all().order_by('-uploaded_at')
    paginator = Paginator(list, 60) 
    page_number = request.GET.get("page")
    videos = paginator.get_page(page_number)

    context = {
        'videos' : videos,
    }
    return render(request, 'video/index.html', context)



def movies(request):
    keywords = request.GET.get('q')
    q = Q()
    if keywords:
        q &= (Q(title__icontains=keywords) | Q(description__icontains=keywords) | Q(tags__icontains=keywords))
        list = Movie.objects.filter(q)
    else:
        list = Movie.objects.filter(episode__isnull=True)


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







def getLocaction(ip):
    url = f"https://api.ipgeolocation.io/ipgeo?apiKey=2df9c865ff864fb4bcbf81ebbe0386eb&ip={ip}"
    response = requests.get(url)
    return response.json()


def video(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    movies = Movie.objects.all().order_by('-uploaded_at')[0:18]
    episodes = Movie.objects.filter(list=movie.list)

    videos = Video.objects.filter(movie=movie.id)
    categories = Category.objects.all()

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
        'episodes' : episodes,
        'categories' : categories
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
    list = PlayList.objects.all()
    paginator = Paginator(list, 25) 
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






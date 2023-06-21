from django.shortcuts import render, get_object_or_404

from .forms import VideoForm
from .models import *
from django.http import JsonResponse

def index(request):
    videos = Video.objects.all()

    context = {
        'videos' : videos,
    }
    return render(request, 'video/index.html', context)

def video_upload(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()
            return JsonResponse({'messsage': "You video uploaded successfully."})
    else:
        form = VideoForm()
    return render(request, 'video/create.html', {'form': form})


def video(request, slug):
    video = get_object_or_404(Video, slug=slug)
    videos = Video.objects.all().order_by('-uploaded_at')[0:15]

    context = {
        'video' : video,
        'videos' : videos,
        'title': video.title
    }
    return render(request, 'video/show.html', context)


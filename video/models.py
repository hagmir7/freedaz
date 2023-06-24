from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid
import os




def filename(instance, filename):
    ext = filename.split('.')[-1]  # Get the file extension
    new_filename = f'{uuid.uuid4().hex}.{ext}'
    base_path = f"{str(instance._meta.model_name).lower()}s/{ext.upper()}" # Change this to your desired directory
    current_date = timezone.now().strftime('%Y-%m-%d')
    file = os.path.join(base_path, current_date, new_filename)
    
    return file


class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip = models.CharField(max_length=100)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country_flag = models.CharField(max_length=300, null=True, blank=True)
    country_code = models.CharField(max_length=10, null=True, blank=True)
    browser = models.CharField(max_length=100, null=True, blank=True)
    os = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.ip
    
class Category(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to=filename)
    views = models.ManyToManyField(Location, related_name='category_views')
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid4().hex
        return super(Category, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Subscription(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to=filename)
    description = models.TextField()
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid4().hex
        return super(Subscription, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    


class Serie(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(default='')
    image = models.ImageField(upload_to=filename, null=True, blank=True)
    views = models.ManyToManyField(Location, related_name='serie_views')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, related_name='serie_category', blank=True)
    save = models.ManyToManyField(User, related_name='serie_save', blank=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)


    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid4().hex
        return super(Serie, self).save(*args, **kwargs)

    

class PlayList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(default='')
    image = models.ImageField(upload_to=filename, null=True, blank=True)
    views = models.ManyToManyField(Location, related_name='paly_list_views')
    category = models.ManyToManyField(Category, related_name='play_list_category', blank=True)
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, null=True, blank=True)
    season = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    save = models.ManyToManyField(User, related_name='play_list_save', blank=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid4().hex
        return super(PlayList, self).save(*args, **kwargs)
    
class Movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=filename, null=True, blank=True)
    list = models.ForeignKey(PlayList, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(default='')
    tags = models.CharField(max_length=200, null=True, blank=True)
    views = models.ManyToManyField(Location, related_name='movie_views')
    category = models.ManyToManyField(Category, related_name='movie_category', blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    save = models.ManyToManyField(User, related_name='movie_save', blank=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True, blank=True)
    episode = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)


    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid4().hex
        return super(Movie, self).save(*args, **kwargs)  
    

class Video(models.Model):
    quality = models.CharField(max_length=100)
    video_file = models.FileField(upload_to=filename)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True, blank=True)


    def __str__(self):
        return self.movie.title
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid4().hex
        return super(Video, self).save(*args, **kwargs)
    



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name='comment_like', blank=True)
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

    

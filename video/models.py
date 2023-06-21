from django.db import models
from django.contrib.auth.models import User
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



class IpAddress(models.Model):
    ip = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.ip
    

class PlayList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to=filename, null=True, blank=True)
    views = models.ManyToManyField(IpAddress, related_name='paly_list_views')
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid4().hex
        return super(PlayList, self).save(*args, **kwargs)
    


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=filename, null=True, blank=True)
    video_file = models.FileField(upload_to=filename)
    description = models.TextField()
    tags = models.CharField(max_length=200, null=True, blank=True)
    views = models.ManyToManyField(IpAddress, related_name='video_views')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.title
    

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
    

    

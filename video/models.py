from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models.signals import pre_save, pre_delete,post_save
from django.dispatch import receiver
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
    name = models.CharField(max_length=150, verbose_name="إسم الصنف")
    image = models.ImageField(upload_to=filename, verbose_name="صورة ")
    views = models.ManyToManyField(Location, related_name='category_views')
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid4().hex
        return super(Category, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Subscription(models.Model):
    name = models.CharField(max_length=150, verbose_name="إسم الشركة ")
    image = models.ImageField(upload_to=filename, verbose_name="صورة ")
    description = models.TextField(verbose_name="وصف ")
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid4().hex
        return super(Subscription, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    


class Serie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name="عنوان")
    description = models.TextField(default='', verbose_name="وصف")
    image = models.ImageField(upload_to=filename, null=True, blank=True, verbose_name="صورة")
    views = models.ManyToManyField(Location, related_name='serie_views')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, related_name='serie_category', blank=True, verbose_name="صنف")
    save = models.ManyToManyField(User, related_name='serie_save', blank=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True, blank=True, verbose_name="الشركة المنتجة ")
    slug = models.SlugField(null=True, blank=True)


    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid4().hex
        return super(Serie, self).save(*args, **kwargs)

    

class PlayList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="عنوان")
    description = models.TextField(default='', verbose_name="وصف")
    image = models.ImageField(upload_to=filename, null=True, blank=True, verbose_name="صورة")
    views = models.ManyToManyField(Location, related_name='paly_list_views')
    category = models.ManyToManyField(Category, related_name='play_list_category', blank=True, verbose_name="صنف")
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, null=True, blank=True, verbose_name="تحديد المسلسل")
    season = models.IntegerField(null=True, blank=True, verbose_name="موسم")
    created_at = models.DateTimeField(auto_now_add=True)
    save = models.ManyToManyField(User, related_name='play_list_save', blank=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True, blank=True, verbose_name="الشركة المنتجة ")
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid4().hex
        return super(PlayList, self).save(*args, **kwargs)
    
class Movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="عنوان")
    image = models.ImageField(upload_to=filename, null=True, blank=True, verbose_name="صورة")
    list = models.ForeignKey(PlayList, on_delete=models.CASCADE, null=True, blank=True, verbose_name="إختيار الموسم")
    description = models.TextField(default='', verbose_name="الوصف")
    tags = models.CharField(max_length=200, null=True, blank=True, verbose_name="علامات")
    views = models.ManyToManyField(Location, related_name='movie_views')
    category = models.ManyToManyField(Category, related_name='movie_category', blank=True, verbose_name="صنف")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    save = models.ManyToManyField(User, related_name='movie_save', blank=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True, blank=True, verbose_name='الشركة المنتجة')
    episode = models.IntegerField(null=True, blank=True, verbose_name="لاحلقة")
    is_last = models.BooleanField(null=True, default=False, verbose_name="الحلقة الأخيرة")
    slug = models.SlugField(null=True, blank=True)


    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid4().hex
        return super(Movie, self).save(*args, **kwargs)  
    

class Video(models.Model):
    quality = models.CharField(max_length=100, verbose_name="الجودة")
    video_file = models.FileField(upload_to=filename, verbose_name="تحميل الفيديو ", null=True, blank=True)
    url = models.CharField(max_length=1000, null=True, blank=True, verbose_name="رابط الفيديو")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True, blank=True)


    def __str__(self):
        return self.movie.title
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid4().hex
        return super(Video, self).save(*args, **kwargs)
    
@receiver(pre_delete, sender=Video)
def delete_video_file(sender, instance, **kwargs):
    # Delete the image file when the model instance is deleted
    instance.video_file.delete(save=False)



@receiver(pre_save, sender=Video)
def delete_old_image(sender, instance, **kwargs):
    if instance.pk:
        # Retrieve the existing instance from the database
        existing_instance = sender.objects.get(pk=instance.pk)

        # Check if the image field has changed
        if existing_instance.video_file and existing_instance.video_file != instance.video_file:
            # Delete the old video_file file
            existing_instance.video_file.delete(save=False)
    



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name='comment_like', blank=True)
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

    

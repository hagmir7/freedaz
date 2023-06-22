from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


user_type = (
    (_('Male'),_('Male')),
    (_('Female'), _('Female')),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    avatar = models.ImageField(upload_to='avatar/', default='user_default.webp', blank=True)
    phone = models.IntegerField(blank=True, default=False)
    gander = models.CharField(max_length=40, blank=True)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    country = models.CharField(max_length=40, blank=True)
    bio = models.TextField(max_length=300, blank=True)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    verificated = models.BooleanField(default=False)
    slug = models.SlugField(blank=True, null=True)


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.created.strftime('%d-%m-%Y')}"

    
    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.user.username))
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return f'/{self.slug}'




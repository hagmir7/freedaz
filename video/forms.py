from django import forms
from .models import *

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','image']


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['name','image', 'description']



class SerieForm(forms.ModelForm):
    class Meta:
        model = Serie
        fields = ['title','image', 'description', 'category', 'subscription']



class PlayListForm(forms.ModelForm):
    class Meta:
        model = PlayList
        fields = ['title','image','season','serie', 'description', 'category', 'subscription']



class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title','image', 'description', 'tags', 'subscription', 'category']


class EpisodeForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'list', 'tags', 'episode', 'is_last']



class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['quality','video_file', 'url']



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
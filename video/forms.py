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
        fields = ['title','image', 'description', 'category', 'subscription']



class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title','image','list','episode', 'description', 'tags', 'subscription', 'category']



class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['quality','video_file',]



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
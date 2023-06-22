from users.models import *
from rest_framework import serializers
from video.models import *
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'image', 'name', 'id', 'slug'



class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['name','image', 'description', 'slug']



class SerieSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    subscription = SubscriptionSerializer()
    # views = UserSerializer()

    class Meta:
        model = Serie
        fields = ['title','image', 'description', 'category', 'subscription', 'views', 'created_at', 'slug']



class PlayListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    category = CategorySerializer()
    subscription = SubscriptionSerializer()
    # views = UserSerializer()

    class Meta:
        model = PlayList
        fields = ['title', 'user', 'image', 'views', 'description', 'category', 'subscription', 'created_at', 'slug']



class MovieSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    # views = UserSerializer()
    list = PlayListSerializer()
    category = CategorySerializer()
    subscription = SubscriptionSerializer()

    class Meta:
        model = Movie
        fields = ['title', 'user' ,'image', 'views', 'list', 'description', 'tags', 'subscription', 'category', 'uploaded_at', 'slug']



class VideoSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()
    class Meta:
        model = Video
        fields = ['quality','video_file','movie', 'slug', 'uploaded_at']



class CommentSerializer(serializers.ModelSerializer):
    like = UserSerializer()
    user = UserSerializer()
    class Meta:
        model = Comment
        fields = ['body', 'user', 'like', 'create_at']
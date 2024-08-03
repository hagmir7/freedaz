from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from django.contrib import sitemaps
from django.contrib.sitemaps.views import sitemap
from video.sitemaps import PlayListSitemap, MovieSitemap

list_site_map = {
    'play-list': PlayListSitemap,
    'movie' : MovieSitemap
}

movies = {
    'movie' : MovieSitemap
}



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('video.urls') ),
    path('', include('users.urls') ),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('video.api.urls')),
    path('list.xml', sitemap, {'sitemaps': list_site_map}, name='django.contrib.sitemaps.views.sitemap'),
    path('movie.xml', sitemap, {'sitemaps': movies}, name='django.contrib.sitemaps.views.sitemap'),

]




urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



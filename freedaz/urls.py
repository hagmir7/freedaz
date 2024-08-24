from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib import sitemaps
# from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
# from video.sitemaps import PlayListSitemap, MovieSitemap
from django.contrib.sitemaps import views as sitemaps_views
from video.models import PlayList, Movie


class PaginatedSitemap(GenericSitemap):
    limit = 100


sitemap = {
    'movie' : PaginatedSitemap(
            {"queryset": Movie.objects.all().order_by('id')},
            priority=1.0,
            changefreq = "daily"
    ),

    'play-list': PaginatedSitemap(
        {"queryset": PlayList.objects.all().order_by('id')},
        priority=1.0,
        changefreq = "daily"
    )
}



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('video.urls') ),
    path('', include('users.urls') ),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('video.api.urls')),

    # Sitemap
    path('sitemap.xml', sitemaps_views.index, {'sitemaps': sitemap}, name='django.contrib.sitemaps.views.sitemap'),
    path('sitemap-<section>.xml', sitemaps_views.sitemap, {'sitemaps': sitemap}, name='django.contrib.sitemaps.views.sitemap'),

]




urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



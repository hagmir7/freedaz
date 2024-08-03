from django.contrib.sitemaps import Sitemap
from .models import PlayList, Movie

class PlayListSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return PlayList.objects.all()

    def lastmod(self, obj):
        return obj.created_at


class MovieSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Movie.objects.all()

    def lastmod(self, obj):
        return obj.uploaded_at
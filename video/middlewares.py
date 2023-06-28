class IgnoreScrapingMiddleware(object):
    def process_request(self, request):
        if request.META.get('User-Agent', '').startswith('Mozilla'):
            return None

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 1
    changefreq = 'daily'

    def items(self):
        return ['downloader']  # your URL names

    def location(self, item):
        return reverse(item)

    def get_urls(self, page=1, site=None, protocol=None):
        protocol = 'https'
        domain = 'sdownloader.duckdns.org'
        urls = []
        for item in self.items():
            urls.append({
                'item': item,
                'location': f'{protocol}://{domain}{self.location(item)}',
                'lastmod': None,
                'changefreq': self.changefreq,
                'priority': self.priority,
            })
        return urls
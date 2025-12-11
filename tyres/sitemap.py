# tyres/sitemap.py
from django.contrib.sitemaps import Sitemap
from .models import Vehicle

class VehicleSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8
    
    def items(self):
        return Vehicle.objects.all()
    
    def lastmod(self, obj):
        return obj.tyres.last_updated
    
    def location(self, obj):
        return f'/vehicle/{obj.slug}/'
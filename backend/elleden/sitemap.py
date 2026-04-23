from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from rooms.models import Room
from pages.models import ConferenceBooking, CateringOrder


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return ['home', 'rooms', 'bookings', 'conference', 'catering', 'about', 'contact']

    def location(self, item):
        return reverse(item)


class RoomSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Room.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('room_detail', args=[obj.id])

    def lastmod(self, obj):
        return obj.updated_at

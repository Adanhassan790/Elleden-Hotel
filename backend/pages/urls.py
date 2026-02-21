from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('about/', views.about, name='about'),
    path('rooms/', views.rooms, name='rooms'),
    path('restaurant/', views.restaurant, name='restaurant'),
    path('conference/', views.conference, name='conference'),
    path('catering/', views.catering, name='catering'),
    path('contact/', views.contact, name='contact'),
]

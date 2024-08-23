from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('about', views.about, name='about'),
    path('service', views.service, name='service'),
    path('commune', views.commune, name='commune'),
    path('blog', views.blog, name='blog'),
    path('team', views.team, name='team'),
    path('testimonies', views.testimonies, name='testimony'),
    
    
]
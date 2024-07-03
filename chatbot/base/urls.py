from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('updateRating/', views.updateRating, name = 'updateRating'),
    path('getResponse/', views.getResponse, name = "getResponse"),
    path('debug/', views.getHeader, name = 'debug')
    ]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('getResponse/', views.getResponse, name = "getResponse")
]
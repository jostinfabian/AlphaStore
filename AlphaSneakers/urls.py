from django.urls import path

from AlphaSneakers import views

urlpatterns = [
    path('home', views.home_view, name='home'),

]

from django.urls import path

from . import views

app_name = 'movie'

urlpatterns = [
    path('worldcup/', views.worldcup, name='worldcup'),
]
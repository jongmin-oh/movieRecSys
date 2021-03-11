from django.urls import path

from . import views

app_name = 'movie'

urlpatterns = [
    path('worldcup/', views.worldcup, name='worldcup'),
    path('ratings/',views.ratings, name='ratings'),
    path('main/',views.main , name='main'),
]
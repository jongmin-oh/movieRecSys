import random

from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render

from .models import MovieData , TopMovie

# Create your views here.

def worldcup(request):
    top_movie = list(TopMovie.objects.order_by('movieId'))
    random.shuffle(top_movie)
    top_movie = top_movie[:32]
    context = {'top_movie' : top_movie}
    return render(request,'recommend/wordcup.html',context)

def index(request):
    movie_data = MovieData.objects.order_by('movieId')
    context = {'movie_data' : movie_data}
    return render(request,'recommend/index.html',context)
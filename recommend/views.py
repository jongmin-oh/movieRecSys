import random
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render
from django.db.models import Q

from .models import MovieData , TopMovie
from .contentsRec import content_recommend

# Create your views here.

def worldcup(request):
    top_movie = list(TopMovie.objects.all)
    random.shuffle(top_movie)
    top_movie = top_movie[:32]
    context = {'top_movie' : top_movie}
    return render(request,'recommend/wordcup.html',context)

def index(request):
    #userID
    best_movie_id = 5
    contents = content_recommend(best_movie_id)

    #best_movie = MovieData.objects.filter(movieId=best_movie_id)

    movies_df = pd.DataFrame(list(MovieData.objects.all().values())).set_index('movieId')

    best_movie = movies_df.loc[best_movie_id]

    sim_genre_movie = movies_df.loc[contents['genre'].values].sort_values('vote_count',ascending=False)
    director_movie = movies_df.loc[contents['director_movie'].values].sort_values('vote_count',ascending=False)
    actor1_movie = movies_df.loc[contents['actor1_movie'].values].sort_values('vote_count',ascending=False)
    actor2_movie = movies_df.loc[contents['actor2_movie'].values].sort_values('vote_count',ascending=False)

    sim_genre_list = [i[1] for i in sim_genre_movie.iterrows()]
    director_list = [i[1] for i in director_movie.iterrows()]
    actor1_list = [i[1] for i in actor1_movie.iterrows()]
    actor2_list = [i[1] for i in actor2_movie.iterrows()]
    
    context = {
    'best_movie' : best_movie ,
    'sim_genre_list' : sim_genre_list ,
    'director_list' : director_list,
    'actor1' : contents['actor1'],
    'actor2' : contents['actor2'],
    'actor1_list' : actor1_list,
    'actor2_list' : actor2_list,
     }

    return render(request,'recommend/index.html',context)
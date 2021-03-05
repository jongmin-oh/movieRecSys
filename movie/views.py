import random
import sqlite3
import pandas as pd
from django.shortcuts import render, get_object_or_404, redirect
from .models import MovieData , TopMovie, RecUser, WorldCup
from django.contrib.auth.models import User
from django.db.models import Q
from .recommend import content_recommend, item_based_recommend


def index(request):
    #userID
    user_name = request.user
    best_movie_id = 2
    contents = content_recommend(best_movie_id)

    movies_df = pd.DataFrame(list(MovieData.objects.all().values())).set_index('movieId')
    worldcup_df = pd.DataFrame(list(WorldCup.objects.all().values())).sort_values('championCount',ascending=False)

    best_movie = movies_df.loc[best_movie_id]

    sim_genre_movie = movies_df.loc[contents['genre'].values].sort_values('vote_count',ascending=False)
    director_movie = movies_df.loc[contents['director_movie'].values].sort_values('vote_count',ascending=False)
    actor1_movie = movies_df.loc[contents['actor1_movie'].values].sort_values('vote_count',ascending=False)
    actor2_movie = movies_df.loc[contents['actor2_movie'].values].sort_values('vote_count',ascending=False)
    worldcup_df = movies_df.loc[worldcup_df['movieId'].values][:20]

    sim_genre_list = [i[1] for i in sim_genre_movie.iterrows()]
    director_list = [i[1] for i in director_movie.iterrows()]
    actor1_list = [i[1] for i in actor1_movie.iterrows()]
    actor2_list = [i[1] for i in actor2_movie.iterrows()]
    worldcup_list = [i[1] for i in worldcup_df.iterrows()]
    
    context = {
    'user_name' : user_name,
    'best_movie' : best_movie ,
    'sim_genre_list' : sim_genre_list ,
    'director_list' : director_list,
    'actor1' : contents['actor1'],
    'actor2' : contents['actor2'],
    'actor1_list' : actor1_list,
    'actor2_list' : actor2_list,
    'worldcup_list' : worldcup_list,
     }

    return render(request,'movie/index.html',context)

def worldcup(request):
    username = str(request.user)
    if request.method == 'POST':
        bestmovie_id = int(request.POST.get('bestMovie'))
        winCount = WorldCup(movieId = bestmovie_id)
        winCount.championCount += 1
        winCount.save()
        try:
            find_user = RecUser.objects.get(userName=username)
            find_user.bestMovie = bestmovie_id
            find_user.save()
        except:
            find_user = User.objects.get(username=username)
            current_user = get_object_or_404(User, pk=find_user.id)
            bestmovie = RecUser(userId = current_user , userName = username , bestMovie = bestmovie_id)
            bestmovie.save()

        return redirect('index')

    top_movie = list(TopMovie.objects.all())
    random.shuffle(top_movie)
    top_movie = top_movie[:32]
    context = {'top_movie' : top_movie}

    return render(request,'movie/worldcup.html',context)



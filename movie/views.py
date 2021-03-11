import random
import sqlite3
import pandas as pd
from django.shortcuts import render, get_object_or_404, redirect ,HttpResponse
from .models import MovieData , TopMovie, RecUser, WorldCup , UserRating
from django.contrib.auth.models import User
from django.db.models import Q
from .recommend import content_recommend, item_based_recommend , user_based_recommend , best_item_base_recommend
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def main(request):
    movies_df = pd.DataFrame(list(MovieData.objects.all().values())).set_index('movieId')
    worldcup_df = pd.DataFrame(list(WorldCup.objects.all().values())).sort_values('championCount',ascending=False)
    worldcup_df = movies_df.loc[worldcup_df['movieId'].values][:20]
    worldcup_list = [i[1] for i in worldcup_df.iterrows()]
    context = {
        'worldcup_list' : worldcup_list,
    }
    return render(request, 'movie/init.html',context)

def index(request):
    user_name = request.user
    if str(user_name) != 'AnonymousUser':
        try:
            current_user = RecUser.objects.get(userName=user_name)
            best_movie_id = current_user.bestMovie

            contents = content_recommend(best_movie_id)
            best_item_base = best_item_base_recommend(best_movie_id)

            item_base = item_based_recommend(request.user.id)
            item_base_movieId = item_base.index

            user_base = user_based_recommend(request.user.id)
            user_base_movieId = user_base.index

            movies_df = pd.DataFrame(list(MovieData.objects.all().values())).set_index('movieId')
            worldcup_df = pd.DataFrame(list(WorldCup.objects.all().values())).sort_values('championCount',ascending=False)

            best_movie = movies_df.loc[best_movie_id]

            sim_genre_movie = movies_df.loc[contents['genre'].values].sort_values('vote_count',ascending=False)
            director_movie = movies_df.loc[contents['director_movie'].values].sort_values('vote_count',ascending=False)
            actor1_movie = movies_df.loc[contents['actor1_movie'].values].sort_values('vote_count',ascending=False)
            actor2_movie = movies_df.loc[contents['actor2_movie'].values].sort_values('vote_count',ascending=False)
            worldcup_df = movies_df.loc[worldcup_df['movieId'].values][:20]
            best_item_df = movies_df.loc[best_item_base].sort_values('vote_count',ascending=False)
            item_base_df = movies_df.loc[item_base_movieId]
            user_base_df = movies_df.loc[user_base_movieId]

            #예상 별점 추가하기
            item_base_df = pd.concat([item_base_df,item_base], axis=1)
            item_base_df = item_base_df.rename(columns={ request.user.id : 'pred_score'})
            item_base_df = item_base_df[item_base_df['year'] > 1995][:30]
            item_base_df['pred_score'] = item_base_df['pred_score'].map(lambda x : round(x , 2 ))

            user_base_df = pd.concat([user_base_df,user_base] , axis=1)
            user_base_df = user_base_df.rename(columns={ request.user.id : 'pred_score'})
            user_base_df = user_base_df[user_base_df['year'] > 1995][:30]
            user_base_df['pred_score'] = user_base_df['pred_score'].map(lambda x : round(x , 2 ))

            sim_genre_list = [i[1] for i in sim_genre_movie.iterrows()]
            director_list = [i[1] for i in director_movie.iterrows()]
            actor1_list = [i[1] for i in actor1_movie.iterrows()]
            actor2_list = [i[1] for i in actor2_movie.iterrows()]
            worldcup_list = [i[1] for i in worldcup_df.iterrows()]
            best_item_list = [i[1] for i in best_item_df.iterrows()]
            item_base_list = [i[1] for i in item_base_df.iterrows()]
            user_base_list = [i[1] for i in user_base_df.iterrows()]

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
            'best_item_list' : best_item_list,
            'item_base_list' : item_base_list,
            'user_base_list' : user_base_list,
            }
            return render(request,'movie/index.html',context)
        except RecUser.DoesNotExist:
            return redirect('movie:worldcup')
        # except KeyError:
        #     return redirect('movie:ratings')

    return redirect('movie:main')

@login_required(login_url='common:login')
def worldcup(request):
    username = request.user
    if request.method == 'POST':
        bestmovie_id = int(request.POST.get('bestMovie'))
        try:
            find_user = RecUser.objects.get(userName=username)
            find_user.bestMovie = bestmovie_id
            find_user.save()
        except:
            find_user = User.objects.get(username=username)
            current_user = get_object_or_404(User, pk=find_user.id)
            bestmovie = RecUser(userId = current_user , userName = username , bestMovie = bestmovie_id)
            bestmovie.save()
        if(True):
            try:
                winCount = WorldCup.objects.get(movieId = bestmovie_id)
                winCount.championCount += 1
                winCount.save()
            except:
                winCount = WorldCup(movieId = bestmovie_id, championCount = 1)
                winCount.save()

        return redirect('index')

    top_movie = list(TopMovie.objects.all())
    random.shuffle(top_movie)
    top_movie = top_movie[:32]
    context = {'top_movie' : top_movie}

    return render(request,'movie/worldcup.html',context)

@login_required(login_url='common:login')
def ratings(request):
    rating_movie = list(TopMovie.objects.all())
    random.shuffle(rating_movie)
    rating_movie1 = rating_movie[:32]
    rating_movie2 = rating_movie[32:64]
    
    if request.method == 'POST':

        username = request.user
        find_user = User.objects.get(username=username)
        current_user = get_object_or_404(User, pk=find_user.id)
        movies = get_object_or_404(MovieData, pk=1)

        movieId = list(request.POST.getlist('movie_id'))
        ratings = list(request.POST.getlist('movie_rating'))

        userRating_df = pd.DataFrame({ "movieId" : movieId , "ratings" : ratings})
        userRating_df['ratings'] = userRating_df['ratings'].astype('float')
        userRating_df = userRating_df[userRating_df['ratings'] != 0]

        for i in range(len(userRating_df)):
            movieId = userRating_df.iloc[i]['movieId']
            ratings = userRating_df.iloc[i]['ratings']
            try:
                temp = UserRating.objects.get(movieId=movieId , userId=current_user)
                temp.movieId = movieId
                temp.rating = (ratings / 2) # 10 점 만점 -> 5 점 만점
                temp.save()
            except:
                temp = UserRating(movieId=movieId,userId=current_user,rating=(ratings/2))       
                temp.save()

        return redirect('index')


    context = {
        'rating_movie1' : rating_movie1,
        'rating_movie2' : rating_movie2,
    }
    return render(request,'movie/ratings.html',context)
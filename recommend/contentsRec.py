import os
import pandas as pd
import numpy as np
import sqlite3
from django.conf import settings
from sklearn.metrics.pairwise import cosine_similarity

from math import sqrt
from collections import Counter
from ast import literal_eval
from .models import MovieData

def content_recommend(movieId):

    movies_df = pd.DataFrame(list(MovieData.objects.all().values())).set_index('movieId')

    movies_df['actor_list'] = movies_df['actor'].map(lambda x : literal_eval(x))
    
    baseUrl = settings.MEDIA_ROOT_URL + settings.MEDIA_URL
    genre_representation = pd.read_csv(baseUrl+'genre_representation.csv',index_col='movieId')
    genre_cos_df = cos_sim_matrix(genre_representation,genre_representation)
    genre_cos_df.columns = genre_representation.index

    title = movies_df.loc[movieId]['title_ko']
    
    genre = genre_cos_df.loc[movieId].T.sort_values(by=(movieId,) , ascending=False)[1:7]
    genre_id = genre.index.astype('int64')
    
    director = movies_df.loc[movieId]['director']
    director_movies = movies_df[movies_df['director'] == director].sort_values(by='vote_count',ascending=False)
    director_id = director_movies.loc[director_movies.index != movieId][:6].index
    
    actors = movies_df.loc[movieId]['actor_list']
    main_character1 = actors[0]
    main_character2 = actors[1]
    
    cast_idx1 = []
    cast_idx2 = []
    for i in movies_df['actor'].index :
        if main_character1 in movies_df.loc[i]['actor']:
            cast_idx1.append(i)
            
        if main_character2 in movies_df.loc[i]['actor']:
            cast_idx2.append(i)
            
    character1_movies = movies_df.loc[cast_idx1].sort_values(by='vote_count',ascending=False)
    main1_id = character1_movies.loc[character1_movies.index != movieId][:6].index
    
    character2_movies = movies_df.loc[cast_idx2].sort_values(by='vote_count',ascending=False)
    main2_id = character2_movies.loc[character2_movies.index != movieId][:6].index
    
    result_dict = {
        "title" : title,
        "genre" : genre_id ,
        "director" : director,
        "director_movie" : director_id ,
        "actor1" : main_character1,
        "actor2" : main_character2,
        "actor1_movie" : main1_id ,
        "actor2_movie" : main2_id}
    
    return result_dict

def cos_sim_matrix(a , b):
    cos_sim = cosine_similarity(a , b)
    result_df = pd.DataFrame(data=cos_sim, index=[a.index])
    
    return result_df

# def itemBase(userId):
#     return pass
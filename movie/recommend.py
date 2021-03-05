import os
import pandas as pd
import numpy as np
import sqlite3
from django.conf import settings

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

from math import sqrt
from collections import Counter
from ast import literal_eval
from .models import MovieData

def content_recommend(movieId):

    movies_df = pd.DataFrame(list(MovieData.objects.all().values())).set_index('movieId')

    baseUrl = settings.MEDIA_ROOT_URL + settings.MEDIA_URL
    cut_movies = pd.read_csv(baseUrl+'movies_1700.csv', index_col='movieId', encoding='utf-8')

    vectorizer = TfidfVectorizer()

    genres_vector = vectorizer.fit_transform(cut_movies['genres'])
    genres_sim = cosine_similarity(genres_vector, genres_vector)

    genres_sim_df = pd.DataFrame(data=genres_sim, index=cut_movies.index, columns = cut_movies.index)

    #본인 제외 유사도가 높은 상위 20개를 추리기
    genres_index = genres_sim_df[movieId].sort_values(ascending=False)[:20].index
    genres_index = genres_index[genres_index != movieId]
    #20개 영화를 다시 평균 평점 기준으로 반환 -> movieId 리스트 추출
    genre_id = cut_movies.loc[genres_index].sort_values('vote_average', ascending=False)[:6].index

    title = movies_df.loc[movieId]['title_ko']

    director = movies_df.loc[movieId]['director']
    director_movies = movies_df[movies_df['director'] == director].sort_values(by='vote_count',ascending=False)
    director_id = director_movies.loc[director_movies.index != movieId][:6].index

    movies_df['actor_list'] = movies_df['actor'].map(lambda x : literal_eval(x))

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
        "actor2_movie" : main2_id
    }

    return result_dict

def item_based_recommend(movieId):

    movies_df = pd.DataFrame(list(MovieData.objects.all().values())).set_index('movieId')
    baseUrl = settings.MEDIA_ROOT_URL + settings.MEDIA_URL
    ratings_df = pd.read_csv(baseUrl+'ratings.csv').drop('timestamp', axis=1)

    ratings_movies = pd.merge(ratings_df, movies_df, on='movieId')

    collabo_data = ratings_movies.pivot_table('rating', index = 'userId', columns = 'movieId').fillna(0)
    item_collabo_data = collabo_data.transpose()

    item_sim = cosine_similarity(item_collabo_data, item_collabo_data)

    item_sim_df = pd.DataFrame(data = item_sim, index = item_collabo_data.index, columns = item_collabo_data.index)

    item_sim_index = item_sim_df[movieId].sort_values(ascending=False)[1:7].index
    result = {
        "item_movie" : item_sim_index
    }

    return result

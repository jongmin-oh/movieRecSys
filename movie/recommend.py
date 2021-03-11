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
from .models import MovieData, UserRating


def content_recommend(movieId):

    movies_df = pd.DataFrame(
        list(MovieData.objects.all().values())).set_index('movieId')

    baseUrl = settings.MEDIA_ROOT_URL + settings.MEDIA_URL
    cut_movies = pd.read_csv(baseUrl+'movies_1700.csv',
                             index_col='movieId', encoding='utf-8')

    vectorizer = TfidfVectorizer()

    genres_vector = vectorizer.fit_transform(cut_movies['genres'])
    genres_sim = cosine_similarity(genres_vector, genres_vector)

    genres_sim_df = pd.DataFrame(
        data=genres_sim, index=cut_movies.index, columns=cut_movies.index)

    #본인 제외 유사도가 높은 상위 20개를 추리기
    genres_index = genres_sim_df[movieId].sort_values(ascending=False)[
        :20].index
    genres_index = genres_index[genres_index != movieId]
    #20개 영화를 다시 평균 평점 기준으로 반환 -> movieId 리스트 추출
    genre_id = cut_movies.loc[genres_index].sort_values(
        'vote_average', ascending=False).index

    title = movies_df.loc[movieId]['title_ko']

    director = movies_df.loc[movieId]['director']
    director_movies = movies_df[movies_df['director'] == director].sort_values(
        by='vote_count', ascending=False)
    director_id = director_movies.loc[director_movies.index !=
                                      movieId].index[:20]

    movies_df['actor_list'] = movies_df['actor'].map(lambda x: literal_eval(x))

    actors = movies_df.loc[movieId]['actor_list']
    main_character1 = actors[0]
    main_character2 = actors[1]

    cast_idx1 = []
    cast_idx2 = []
    for i in movies_df['actor'].index:
        if main_character1 in movies_df.loc[i]['actor']:
            cast_idx1.append(i)

        if main_character2 in movies_df.loc[i]['actor']:
            cast_idx2.append(i)

    character1_movies = movies_df.loc[cast_idx1].sort_values(
        by='vote_count', ascending=False)
    main1_id = character1_movies.loc[character1_movies.index !=
                                     movieId].index[:20]

    character2_movies = movies_df.loc[cast_idx2].sort_values(
        by='vote_count', ascending=False)
    main2_id = character2_movies.loc[character2_movies.index !=
                                     movieId].index[:20]

    result_dict = {
        "title": title,
        "genre": genre_id,
        "director": director,
        "director_movie": director_id,
        "actor1": main_character1,
        "actor2": main_character2,
        "actor1_movie": main1_id,
        "actor2_movie": main2_id
    }

    return result_dict

def best_item_base_recommend(movie_id):
    movies_df = pd.DataFrame(list(MovieData.objects.all().values())).set_index('movieId')
    ratings_df = pd.DataFrame(list(UserRating.objects.all().values()))

    ratings_movies = pd.merge(ratings_df, movies_df, on='movieId')

    collabo_data = ratings_movies.pivot_table('rating', index = 'userId_id', columns = 'movieId').fillna(0)
    item_collabo_data = collabo_data.transpose()

    item_sim = cosine_similarity(item_collabo_data, item_collabo_data)

    item_sim_df = pd.DataFrame(data = item_sim, index = item_collabo_data.index, columns = item_collabo_data.index)

    best_item_result = item_sim_df[movie_id].sort_values(ascending=False).index[:30]

    return best_item_result

def item_based_recommend(user_id):
    ratings_df = pd.DataFrame(list(UserRating.objects.all().values()))

    user_ids = sorted(list(set(ratings_df['userId_id'].values)))
    movie_ids = sorted(list(set(ratings_df['movieId'].values)))

    sparse_matrix = pd.DataFrame(index=movie_ids, columns=user_ids)
    sparse_matrix = ratings_df.pivot(
        index='movieId', columns='userId_id', values='rating')

    item_sparse_matrix = sparse_matrix.fillna(0)
    item_cossim_df = cossim_matrix(item_sparse_matrix, item_sparse_matrix)

    userId_grouped = ratings_df.groupby('userId_id')
    item_prediction_result_df = pd.DataFrame(index=list(
        userId_grouped.indices.keys()), columns=item_sparse_matrix.index)

    for userId, group in userId_grouped:
        user_sim = item_cossim_df.loc[group['movieId']]
        user_rating = group['rating']
        sim_sum = user_sim.sum(axis=0).map(lambda x: 1 if x == 0 else x)

        pred_ratings = np.matmul(
            user_sim.T.to_numpy(), user_rating) / (sim_sum)
        item_prediction_result_df.loc[userId] = pred_ratings

    item_result = item_prediction_result_df.loc[user_id].sort_values(
        ascending=False)

    return item_result


def user_based_recommend(user_id):
    ratings_df = pd.DataFrame(list(UserRating.objects.all().values()))

    user_ids = sorted(list(set(ratings_df['userId_id'].values)))
    movie_ids = sorted(list(set(ratings_df['movieId'].values)))

    sparse_matrix = pd.DataFrame(index=movie_ids, columns=user_ids)
    sparse_matrix = ratings_df.pivot(
        index='movieId', columns='userId_id', values='rating')

    user_sparse_matrix = sparse_matrix.fillna(0).transpose()
    user_cossim_df = cossim_matrix(user_sparse_matrix, user_sparse_matrix)

    movieId_grouped = ratings_df.groupby('movieId')
    user_prediction_result_df = pd.DataFrame(index=list(
        movieId_grouped.indices.keys()),columns=user_sparse_matrix.index)
    
    for movieId, group in movieId_grouped:
        user_sim = user_cossim_df.loc[group['userId_id']]
        user_rating = group['rating']
        sim_sum = user_sim.sum(axis=0).map(lambda x : 1 if x==0 else x)

        pred_ratings = np.matmul(user_sim.T.to_numpy(), user_rating) / sim_sum
        user_prediction_result_df.loc[movieId] = pred_ratings
    
    user_prediction_result_df = user_prediction_result_df.transpose()

    user_result = user_prediction_result_df.loc[user_id].sort_values(ascending=False)

    return user_result


def cossim_matrix(a, b):
    cossim_values = cosine_similarity(a.values, b.values)
    cossim_df = pd.DataFrame(
        data=cossim_values, columns=a.index.values, index=a.index)

    return cossim_df

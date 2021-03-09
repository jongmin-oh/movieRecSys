import os
import pandas as pd
from pandas import Series, DataFrame
import sqlite3

#print(os.getcwd())

movieData = pd.read_csv('./media/result_movie.csv')
topMovie = pd.read_csv('./media/top158_movie.csv')
ratings = pd.read_csv('./media/ratings.csv',index_col=0)

con = sqlite3.connect("db.sqlite3")
movieData.to_sql('movie_moviedata',con,if_exists='replace',index=False) # arg chunksize=1000
topMovie.to_sql('movie_topmovie',con,if_exists='replace',index=False)
ratings.to_sql('movie_userrating',con,if_exists='replace', index=False)

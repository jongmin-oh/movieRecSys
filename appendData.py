import os
import sqlite3
import pandas as pd
from pandas import Series, DataFrame

#print(os.getcwd())

movieData = pd.read_csv('./recommend/media/result_movie.csv')
topMovie = pd.read_csv('./recommend/media/top158_movie.csv')
con = sqlite3.connect("db.sqlite3")
movieData.to_sql('recommend_moviedata',con,if_exists='replace') # arg chunksize=1000
topMovie.to_sql('recommend_topmovie',con,if_exists='replace')


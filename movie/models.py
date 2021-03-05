from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class MovieData(models.Model):
    movieId = models.IntegerField(primary_key=True)
    title_en = models.CharField(max_length=200)
    title_ko = models.CharField(max_length=200)
    genres = models.CharField(max_length=300)
    year = models.IntegerField()
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    director = models.CharField(max_length=100)
    actor = models.CharField(max_length=300)
    poster = models.CharField(max_length=500)
    link = models.CharField(max_length=500)

#시리즈물이 겹치는 부분이 너무많아 따로 분리
class TopMovie(models.Model):
    movieId = models.IntegerField(primary_key=True)
    title_en = models.CharField(max_length=200)
    title_ko = models.CharField(max_length=200)
    genres = models.CharField(max_length=300)
    year = models.IntegerField()
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    director = models.CharField(max_length=100)
    actor = models.CharField(max_length=300)
    poster = models.CharField(max_length=500)
    link = models.CharField(max_length=500)

class RecUser(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    userName = models.CharField(max_length=200)
    bestMovie = models.IntegerField()

    def __str__(self):
        return self.userName

class UserRating(models.Model):
    userId = models.ForeignKey(RecUser, on_delete=models.CASCADE)
    movieId = models.ForeignKey(MovieData, on_delete=models.CASCADE)
    rathig = models.FloatField()

class WorldCup(models.Model):
    movieId = models.IntegerField()
    championCount = models.IntegerField(default=0)

# Generated by Django 2.2.6 on 2021-02-23 04:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MovieData',
            fields=[
                ('movieId', models.IntegerField(primary_key=True, serialize=False)),
                ('title_en', models.CharField(max_length=200)),
                ('title_ko', models.CharField(max_length=200)),
                ('genres', models.CharField(max_length=300)),
                ('year', models.IntegerField()),
                ('vote_average', models.FloatField()),
                ('vote_count', models.IntegerField()),
                ('director', models.CharField(max_length=100)),
                ('actor', models.CharField(max_length=300)),
                ('poster', models.CharField(max_length=500)),
                ('link', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='TopMovie',
            fields=[
                ('movieId', models.IntegerField(primary_key=True, serialize=False)),
                ('title_en', models.CharField(max_length=200)),
                ('title_ko', models.CharField(max_length=200)),
                ('genres', models.CharField(max_length=300)),
                ('year', models.IntegerField()),
                ('vote_average', models.FloatField()),
                ('vote_count', models.IntegerField()),
                ('director', models.CharField(max_length=100)),
                ('actor', models.CharField(max_length=300)),
                ('poster', models.CharField(max_length=500)),
                ('link', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userId', models.IntegerField(primary_key=True, serialize=False)),
                ('userName', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('bestMovie', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='WorldCup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('championCount', models.IntegerField()),
                ('winCount', models.IntegerField()),
                ('loseCount', models.IntegerField()),
                ('winningRate', models.FloatField()),
                ('movieId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommend.MovieData')),
            ],
        ),
        migrations.CreateModel(
            name='UserRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rathig', models.FloatField()),
                ('movieId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommend.MovieData')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommend.User')),
            ],
        ),
    ]

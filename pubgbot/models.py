from django.db import models

class Log(models.Model):
    id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=30, default="")
    timestamp = models.DateTimeField(auto_now_add=True)

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100, default="")
    timestamp = models.DateTimeField(auto_now=True)
    season = models.CharField(max_length=50, default="")

class SoloStats(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100, default="")
    timestamp = models.DateTimeField(auto_now=True)
    rounds_played = models.CharField(max_length=30, default="")
    rating = models.CharField(max_length=30, default="")
    best_rating = models.CharField(max_length=30, default="")
    best_rank = models.CharField(max_length=30, default="")
    win_ratio = models.CharField(max_length=30, default="")
    wins = models.CharField(max_length=30, default="")
    top_10_ratio = models.CharField(max_length=30, default="")
    kill_death_ratio = models.CharField(max_length=30, default="")
    kills_pg = models.CharField(max_length=30, default="")
    damage_pg = models.CharField(max_length=30, default="")
    round_most_kills = models.CharField(max_length=30, default="")
    longest_kill = models.CharField(max_length=30, default="")
    percentile = models.CharField(max_length=30, default="")

class DuoStats(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100, default="")
    timestamp = models.DateTimeField(auto_now=True)
    rounds_played = models.CharField(max_length=30, default="")
    rating = models.CharField(max_length=30, default="")
    best_rating = models.CharField(max_length=30, default="")
    best_rank = models.CharField(max_length=30, default="")
    win_ratio = models.CharField(max_length=30, default="")
    wins = models.CharField(max_length=30, default="")
    top_10_ratio = models.CharField(max_length=30, default="")
    kill_death_ratio = models.CharField(max_length=30, default="")
    kills_pg = models.CharField(max_length=30, default="")
    damage_pg = models.CharField(max_length=30, default="")
    round_most_kills = models.CharField(max_length=30, default="")
    longest_kill = models.CharField(max_length=30, default="")
    percentile = models.CharField(max_length=30, default="")

class SquadStats(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100, default="")
    timestamp = models.DateTimeField(auto_now=True)
    rounds_played = models.CharField(max_length=30, default="")
    rating = models.CharField(max_length=30, default="")
    best_rating = models.CharField(max_length=30, default="")
    best_rank = models.CharField(max_length=30, default="")
    win_ratio = models.CharField(max_length=30, default="")
    wins = models.CharField(max_length=30, default="")
    top_10_ratio = models.CharField(max_length=30, default="")
    kill_death_ratio = models.CharField(max_length=30, default="")
    kills_pg = models.CharField(max_length=30, default="")
    damage_pg = models.CharField(max_length=30, default="")
    round_most_kills = models.CharField(max_length=30, default="")
    longest_kill = models.CharField(max_length=30, default="")
    percentile = models.CharField(max_length=30, default="")


class ErrorUser(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100, default="")
    timestamp = models.DateTimeField(auto_now=True)
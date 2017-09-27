from __future__ import absolute_import
from celery import shared_task
from pypubg import core
from pubgbot.models import Log, Users, SoloStats, DuoStats, SquadStats, ErrorUser


@shared_task
def get_user(username):
    api = core.PUBGAPI("b9c5327d-1598-4063-aa06-beb16798c369")
    user_info = api.player(username)

    if 'error' in user_info:
        create_log("no_user_error")
        save_error(username)
    else:
        create_log(username)
        save_stats(username, user_info)

def save_error(username):
    ErrorUser.objects.update_or_create(
        user_name=username
    )


def save_stats(username, user_info):
    create_user_info(username, user_info['defaultSeason'])
    exposure_list = [
        "RoundsPlayed",
        "Rating",
        "BestRating",
        "BestRank",
        "WinRatio",
        "Wins",
        "Top10Ratio",
        "KillDeathRatio",
        "KillsPg",
        "DamagePg",
        "RoundMostKills",
        "LongestKill",
    ]
    season = user_info['defaultSeason']
    stats = user_info['Stats']

    sol_stats = dict()
    duo_stats = dict()
    sq_stats = dict()

    for stat in stats:
        if stat['Season'] == season and stat['Region'] == 'as':
            if stat['Match'] == 'solo':
                sol_stats = stat['Stats']
            elif stat['Match'] == 'duo':
                duo_stats = stat['Stats']
            elif stat['Match'] == 'squad':
                sq_stats = stat['Stats']

    expose_sol_stat = dict()
    expose_duo_stat = dict()
    expose_sq_stat = dict()

    for item in sol_stats:
        label = item['field']
        val = item['displayValue']

        if label in exposure_list:
            expose_sol_stat[label] = val

    for item in duo_stats:
        label = item['field']
        val = item['displayValue']

        if label in exposure_list:
            expose_duo_stat[label] = val

    for item in sq_stats:
        label = item['field']
        val = item['displayValue']

        if label in exposure_list:
            expose_sq_stat[label] = val

    if len(expose_sol_stat) == 0:
        create_empty_stat(username, "solo")
    else:
        create_stat_table(
            username,
            "solo",
            expose_sol_stat['RoundsPlayed'],
            expose_sol_stat['Rating'],
            expose_sol_stat['BestRating'],
            expose_sol_stat['BestRank'],
            expose_sol_stat['WinRatio'],
            expose_sol_stat['Wins'],
            expose_sol_stat['Top10Ratio'],
            expose_sol_stat['KillDeathRatio'],
            expose_sol_stat['KillsPg'],
            expose_sol_stat['DamagePg'],
            expose_sol_stat['RoundMostKills'],
            expose_sol_stat['LongestKill'],
        )

    if len(expose_duo_stat) == 0:
        create_empty_stat(username, "duo")
    else:
        create_stat_table(
            username,
            "duo",
            expose_duo_stat['RoundsPlayed'],
            expose_duo_stat['Rating'],
            expose_duo_stat['BestRating'],
            expose_duo_stat['BestRank'],
            expose_duo_stat['WinRatio'],
            expose_duo_stat['Wins'],
            expose_duo_stat['Top10Ratio'],
            expose_duo_stat['KillDeathRatio'],
            expose_duo_stat['KillsPg'],
            expose_duo_stat['DamagePg'],
            expose_duo_stat['RoundMostKills'],
            expose_duo_stat['LongestKill'],
        )

    if len(expose_sq_stat) == 0:
        create_empty_stat(username, "squad")
    else:
        create_stat_table(
            username,
            "squad",
            expose_sq_stat['RoundsPlayed'],
            expose_sq_stat['Rating'],
            expose_sq_stat['BestRating'],
            expose_sq_stat['BestRank'],
            expose_sq_stat['WinRatio'],
            expose_sq_stat['Wins'],
            expose_sq_stat['Top10Ratio'],
            expose_sq_stat['KillDeathRatio'],
            expose_sq_stat['KillsPg'],
            expose_sq_stat['DamagePg'],
            expose_sq_stat['RoundMostKills'],
            expose_sq_stat['LongestKill'],
        )


def create_user_info(username, season):
    Users.objects.update_or_create(
        user_name=username,
        season=season
    )


def create_empty_stat(username, match_type):
    if match_type == "solo":
        SoloStats.objects.update_or_create(
            user_name=username,
            rounds_played=0
        )
    elif match_type == "duo":
        DuoStats.objects.update_or_create(
            user_name=username,
            rounds_played=0
        )
    elif match_type == "squad":
        SquadStats.objects.update_or_create(
            user_name=username,
            rounds_played=0
        )


def create_stat_table(username, match_type, rounds_played, rating, best_rating, best_rank, win_ratio, wins,
                      top_10_ratio, kill_death_ratio, kills_pg, damage_pg, round_most_kills, longest_kill):
    if match_type == "solo":
        SoloStats.objects.update_or_create(
            user_name=username,
            rounds_played=rounds_played,
            rating=rating,
            best_rating=best_rating,
            best_rank=best_rank,
            win_ratio=win_ratio,
            wins=wins,
            top_10_ratio=top_10_ratio,
            kill_death_ratio=kill_death_ratio,
            kills_pg=kills_pg,
            damage_pg=damage_pg,
            round_most_kills=round_most_kills,
            longest_kill=longest_kill
        )
    elif match_type == "duo":
        DuoStats.objects.update_or_create(
            user_name=username,
            rounds_played=rounds_played,
            rating=rating,
            best_rating=best_rating,
            best_rank=best_rank,
            win_ratio=win_ratio,
            wins=wins,
            top_10_ratio=top_10_ratio,
            kill_death_ratio=kill_death_ratio,
            kills_pg=kills_pg,
            damage_pg=damage_pg,
            round_most_kills=round_most_kills,
            longest_kill=longest_kill
        )
    elif match_type == "squad":
        SquadStats.objects.update_or_create(
            user_name=username,
            rounds_played=rounds_played,
            rating=rating,
            best_rating=best_rating,
            best_rank=best_rank,
            win_ratio=win_ratio,
            wins=wins,
            top_10_ratio=top_10_ratio,
            kill_death_ratio=kill_death_ratio,
            kills_pg=kills_pg,
            damage_pg=damage_pg,
            round_most_kills=round_most_kills,
            longest_kill=longest_kill
        )

def create_log(nickname):
    Log.objects.create(
        nickname = nickname
    )
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from pypubg import core
from pubgbot.models import Log
import json


def keyboard(request):

    return JsonResponse({
        'type' : 'text',
        'content': '닉네임을 입력해주세요.'
    })

@csrf_exempt
def answer(request):
    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    username = received_json_data['content']

    sending_msg = ""
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
    user_info = get_user(username)
    if user_info == "no_user":
        return JsonResponse({
            'message': {
                'text': username + " 유저의 전적을 검색할 수 없습니다."
            },
            'keyboard': {
                'type': 'text',
                'content': '닉네임을 입력해주세요.'
            }
        })

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
        solo_msg = "솔로 \n\n플레이 정보가 없습니다.\n\n"
    else:
        solo_msg = make_msg(
            "솔로",
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
        duo_msg = "듀오 \n\n플레이 정보가 없습니다.\n\n"
    else:
        duo_msg = make_msg(
            "듀오",
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
        sq_msg = "스쿼드 \n\n플레이 정보가 없습니다."
    else:
        sq_msg = make_msg(
            "스쿼드",
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

    sending_msg = username + "님의 " + season + " 시즌 전적 \n\n"
    sending_msg += solo_msg + duo_msg + sq_msg

    return JsonResponse({
        'message': {
            'text': sending_msg
        }
    })

def get_user(username):
    api = core.PUBGAPI("b9c5327d-1598-4063-aa06-beb16798c369")
    user_info = api.player(username)

    if 'error' in user_info:
        create_log("no_user_error")
        return "no_user"
    else:
        create_log(username)
        return user_info

def make_msg(type, match_cnt, rating, top_rating, rank, win_ratio, wins, top10 , kd, kill_pg, deal_pg, kill_streak, long_kill):
    msg = type + ' ' + match_cnt + '게임 \n\n'
    msg += '레이팅: ' + rating + ' (최고 '+ top_rating +') \n'
    msg += '순위   : ' + rank + '위\n'
    msg += '승률   : ' + win_ratio + ' (치킨 ' + wins + '마리) \n'
    msg += '탑텐   : '+ top10 +'\n'
    msg += '킬뎃   : ' + kd + '\n'
    msg += '평균킬: ' + kill_pg + '\n'
    msg += '평균딜: ' + deal_pg + '\n'
    msg += '여포   : ' + kill_streak + '\n'
    msg += '최장거리킬: ' + long_kill + '\n\n'

    return msg

def create_log(nickname):
    Log.objects.create(
        nickname = nickname
    )
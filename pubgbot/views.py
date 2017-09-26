from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from pubgbot.models import Users, SoloStats, DuoStats, SquadStats
import json
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import localtime
import pubgbot.tasks as tasks


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

    if username == "다른계정":
        return JsonResponse({
            'message': {
                'text': "닉네임을 입력해주세요."
            },
            'keyboard': {
                'type': 'text',
                'content': "닉네임을 입력해주세요."
            }
        })

    #유저명 검색
    user_info = search_user_info(username)
    # DB에 없는 유저정보
    if not user_info:
        tasks.get_user(username)
        return JsonResponse({
            'message': {
                'text': "전적 정보 업데이트 중입니다. 잠시 후 다시 시도해주세요. \n존재하지 않는 계정의 경우 업데이트되지 않습니다."
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': [username, "다른계정"]
            }
        })
    #유저명 있을 경우
    else:
        now  = datetime.now()
        time_gap = timedelta(minutes=1)
        db_time = localtime(user_info.timestamp)
        if db_time < (now-time_gap):
            # 시간 not_ok일 경우 api콜
            tasks.get_user(username)
            return JsonResponse({
                'message': {
                    'text': "최신 전적 정보를 가져오는 중입니다. 잠시 후 다시 시도해주세요."
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': [username, "다른계정"]
                }
            })
        else:
            solo_stats = SoloStats.objects.filter(user_name=username).last()
            duo_stats = DuoStats.objects.filter(user_name=username).last()
            squad_stats = SquadStats.objects.filter(user_name=username).last()

            solo_msg = make_msg("솔로", solo_stats)
            duo_msg = make_msg("듀오", duo_stats)
            squad_msg = make_msg("스쿼드", squad_stats)

            sending_msg = username + "님의 " + user_info.season + " 시즌 전적 \n\n"
            if username.lower() == 'godmori':
                sending_msg = "⭐턱별회원 린치클럽 ️에이스 BJ ⭐갓갓갓모리⭐님의 " + user_info.season + " 시즌 전적 \n\n"
            elif username.lower() == 'jrae3391':
                sending_msg = "⭐핵고수 밀베왕 학교일진 강남조폭 여포갑 ⭐케챱도둑⭐님의 " + user_info.season + " 시즌 전적 \n\n"
            sending_msg += solo_msg + duo_msg + squad_msg

            return JsonResponse({
                'message': {
                    'text': sending_msg
                }
            })


def search_user_info(username):
    try:
        user_info = Users.objects.filter(user_name=username).last()
    except ObjectDoesNotExist:
        user_info = None

    return user_info


def make_msg(type, stats):
    if stats.rounds_played == 0:
        return type + " \n\n플레이 정보가 없습니다.\n\n"
    else:
        msg = type + ' ' + stats.rounds_played + '게임 \n\n'
        msg += '레이팅: ' + stats.rating + ' (최고 '+ stats.best_rating +') \n'
        msg += '순위   : ' + stats.best_rank + '위\n'
        msg += '승률   : ' + stats.win_ratio + ' (치킨 ' + stats.wins + '마리) \n'
        msg += '탑텐   : '+ stats.top_10_ratio +'\n'
        msg += '킬뎃   : ' + stats.kill_death_ratio + '\n'
        msg += '평균킬: ' + stats.kills_pg + '\n'
        msg += '평균딜: ' + stats.damage_pg + '\n'
        msg += '여포   : ' + stats.round_most_kills + '\n'
        msg += '최장거리킬: ' + stats.longest_kill + '\n\n\n'

    return msg


# curl -XPOST 'http://127.0.0.1:8000/pubg/message' -d '{"user_key": "encryptedUserKey", "type": "text", "content": "GCrider"}'
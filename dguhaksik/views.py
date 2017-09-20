from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from dguhaksik.models import Menu, Log
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json, datetime
import smtplib
import random
from email.mime.text import MIMEText

button_list = ['상록원', '그루터기', '기숙사식당', '교직원식당', '뭐먹지?', '식당시간']


def keyboard(request):

    return JsonResponse({
        'type' : 'buttons',
        'buttons' : button_list
    })

@csrf_exempt
def answer(request):
    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    cafeteria_name = received_json_data['content']

    if cafeteria_name != '식당시간' and cafeteria_name != "뭐먹지?":

        today = datetime.date.today()
        today_date = today.strftime("%m월 %d일")
        hour_now = datetime.datetime.now().hour

        if hour_now >= 15:
            return JsonResponse({
                'message':{
                    'text': today_date + '의 ' + cafeteria_name + '의 저녁메뉴 입니다. \n \n' + get_dinner_menu(cafeteria_name)
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': button_list
                }
            })

        else :
            return JsonResponse({
                'message': {
                    'text': today_date + '의 ' + cafeteria_name + '의 점심 메뉴입니다. \n \n' + get_lunch_menu(cafeteria_name)
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': button_list
                }
            })
    elif cafeteria_name == "뭐먹지?":
        hour_now = datetime.datetime.now().hour

        if hour_now >= 15:
            return JsonResponse({
                'message': {
                    'text': '저녁 식사로 다음 메뉴 어떠세요? \n \n' + get_random_menu("dinner")
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': button_list
                }
            })
        else:
            return JsonResponse({
                'message': {
                    'text': '점심 식사로 다음 메뉴 어떠세요? \n \n' + get_random_menu("launch")
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': button_list
                }
            })

    else:
        return JsonResponse({
            'message': {
                'text': 'http://dgucoop.dongguk.edu/mobile/shop.html?code=1'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': button_list
            }
        })


def lda(request):
    context = {}

    return TemplateResponse(request, 'lda.html', context=context)

def lda_view(request):
    set = request.GET['set']

    context = {}
    context['set'] = set

    return TemplateResponse(request, 'lda_view.html', context=context)


def get_lunch_menu(cafeteria_name):
    create_log(cafeteria_name)
    if cafeteria_name == '상록원':
        sang_bek_lunch = Menu.objects.get(cafe_name='백반코너', time='중식').menu
        sang_ill_lunch = Menu.objects.get(cafe_name='일품코너', time='중식').menu
        sang_yang_lunch = Menu.objects.get(cafe_name='양식코너', time='중식').menu
        sang_dduk_lunch = Menu.objects.get(cafe_name='뚝배기코너', time='중식').menu

        return "============\n중식\n============\n" \
               +  "백반코너 \n" + sang_bek_lunch \
               + "------------\n" + "일품코너 \n" + sang_ill_lunch \
               + "------------\n" + "양식코너 \n" + sang_yang_lunch \
               + "------------\n" + "뚝배기코너 \n" + sang_dduk_lunch

    elif cafeteria_name == '그루터기':
        gru_a_lunch = Menu.objects.get(cafe_name='A코너', time='중식').menu
        gru_b_lunch = Menu.objects.get(cafe_name='B코너', time='중식').menu

        return "============\n중식\n============\n"\
               + "A코너 \n" + gru_a_lunch \
               + "------------\n" + "B코너 \n" + gru_b_lunch

    elif cafeteria_name == '기숙사식당':
        dorm_a_lunch = Menu.objects.get(cafe_name='기숙사A코너', time='중식').menu
        dorm_b_lunch = Menu.objects.get(cafe_name='기숙사B코너', time='중식').menu

        return "============\n중식\n============\n" \
               + "A코너 \n" + dorm_a_lunch \
               + "------------\n" + "B코너 \n" + dorm_b_lunch

    elif cafeteria_name == '교직원식당':
        kyo_jib_lunch = Menu.objects.get(cafe_name='집밥', time='중식').menu
        kyo_han_lunch = Menu.objects.get(cafe_name='한그릇', time='중식').menu

        return "============\n중식\n============\n" \
               + "집밥 \n" + kyo_jib_lunch \
               + "------------\n" + "한그릇 \n" + kyo_han_lunch

    else:
        return "존재하지 않는 식당이거나 오류 발생중입니다."


def get_dinner_menu(cafeteria_name):
    create_log(cafeteria_name)
    if cafeteria_name == '상록원':
        sang_ill_dinner = Menu.objects.get(cafe_name='일품코너', time='석식').menu
        sang_yang_dinner = Menu.objects.get(cafe_name='양식코너', time='석식').menu
        sang_dduk_dinner = Menu.objects.get(cafe_name='뚝배기코너', time='석식').menu

        return "\n============\n석식\n============\n" \
               + "일품코너 \n" + sang_ill_dinner \
               + "------------\n" + "양식코너 \n" + sang_yang_dinner \
               + "------------\n" + "뚝배기코너 \n" + sang_dduk_dinner

    elif cafeteria_name == '그루터기':
        gru_a_dinner = Menu.objects.get(cafe_name='A코너', time='석식').menu
        gru_b_dinner = Menu.objects.get(cafe_name='B코너', time='석식').menu

        return "\n============\n석식\n============\n" \
               + "A코너 \n" + gru_a_dinner \
               + "------------\n" + "B코너 \n" + gru_b_dinner \

    elif cafeteria_name == '기숙사식당':
        dorm_a_dinner = Menu.objects.get(cafe_name='기숙사A코너', time='석식').menu

        return "\n============\n석식\n============\n" \
               + "A코너 \n" + dorm_a_dinner

    elif cafeteria_name == '교직원식당':
        kyo_jib_dinner = Menu.objects.get(cafe_name='집밥', time='석식').menu

        return "\n============\n석식\n============\n" \
               + "집밥 \n" + kyo_jib_dinner

    else:
        return "존재하지 않는 식당이거나 오류 발생중입니다."


def get_random_menu(time):
    if time == "dinner":
        cafe_name_list_dinner = [
            "A코너", "B코너", "기숙사A코너", "뚝배기코너", "양식코너", "일품코너", "집밥"
        ]
        random_corner = random.choice(cafe_name_list_dinner)
        corner_name = get_cafe_name_by_corner(random_corner)
        menu = Menu.objects.get(cafe_name=random_corner, time='석식')

        return corner_name + menu
    else:
        cafe_name_list_lunch = [
            "A코너", "B코너", "기숙사A코너", "기숙사B코너", "뚝배기코너", "백반코너", "양식코너", "일품코너", "집밥", "한그릇"
        ]
        random_corner = random.choice(cafe_name_list_lunch)
        corner_name = get_cafe_name_by_corner(random_corner)
        menu = Menu.objects.get(cafe_name=random_corner, time='중식').menu

        return corner_name + menu


def get_cafe_name_by_corner(corner):
    return {
        'A코너': '그루터기 A코너',
        'B코너': '그루터기 B코너',
        '기숙사A코너': '기숙사식당 A코너',
        '기숙사B코너': '기숙사식당 B코너',
        '뚝배기코너': '상록원 뚝배기코너',
        '백반코너': '상록원 백반코너',
        '양식코너': '상록원 양식코너',
        '일품코너': '상록원 일품코너',
        '집밥': '교직원식당 집밥코너',
        '한그릇': '교직원식당 한그릇코너'
    }.get(corner, 'None')


def crawl(request):
    #메뉴 DB 테이블 비우기
    flush_menu_db()

    #메뉴 테이블 추출
    html = urlopen('http://dgucoop.dongguk.edu/store/store.php?w=4&l=1')
    source = html.read().decode('cp949', 'ignore')
    html.close()
    soup = BeautifulSoup(source, "html.parser", from_encoding='utf-8')
    table_div = soup.find(id="sdetail")
    menu_tables = table_div.table.tr.td.p.find_all('table', {"bgcolor": "#CDD6B5"})

    #식당별 테이블 지정
    kyo_table = menu_tables[0]
    sang_table = menu_tables[1]
    gru_table = menu_tables[3]
    dorm_table = menu_tables[6]


    #교직원 식당
    if kyo_table.find(text="휴무"):
        create_menu_db_table('집밥', '중식', '휴무 \n')
        create_menu_db_table('한그릇', '중식', '휴무 \n')
        create_menu_db_table('집밥', '석식', '휴무 \n')
        create_menu_db_table('한그릇', '석식', '휴무 \n')

    else:
        # 중식이 검색이 안되는 문제 발생... 일단 원래 방법으로 구현해놓음
        kyo_trs = kyo_table.find_all('tr')
        kyo_tables = kyo_trs[1].find_all('table')

        kyo_jib_trs = kyo_tables[0].find_all('tr')
        kyo_jib_menu = kyo_jib_trs[0].text
        kyo_jib_price = kyo_jib_trs[1].text

        kyo_han_trs = kyo_tables[1].find_all('tr')
        kyo_han_menu = kyo_han_trs[0].text
        kyo_han_price = kyo_han_trs[1].text

        create_menu_db_table('집밥', '중식', kyo_jib_menu + kyo_jib_price)
        create_menu_db_table('한그릇', '중식', kyo_han_menu + kyo_han_price)

        for tr in kyo_trs:
            if tr.find(text='석식'):
                kyo_tables = tr.find_all('table')

                kyo_jib_trs = kyo_tables[0].find_all('tr')
                kyo_jib_menu = kyo_jib_trs[0].text
                kyo_jib_price = kyo_jib_trs[1].text

                create_menu_db_table('집밥', '석식', kyo_jib_menu + kyo_jib_price)


    #상록원
    if sang_table.find(text="휴무"):
        create_menu_db_table('백반코너', '중식', '휴무 \n')
        create_menu_db_table('일품코너', '중식', '휴무 \n')
        create_menu_db_table('양식코너', '중식', '휴무 \n')
        create_menu_db_table('뚝배기코너', '중식', '휴무 \n')
        create_menu_db_table('백반코너', '석식', '휴무 \n')
        create_menu_db_table('일품코너', '석식', '휴무 \n')
        create_menu_db_table('양식코너', '석식', '휴무 \n')
        create_menu_db_table('뚝배기코너', '석식', '휴무 \n')

    else:
        sang_trs = sang_table.find_all('tr')
        for tr in sang_trs:
            if tr.find(text="중식"):
                sang_lunch_tables = tr.find_all('table')

                sang_bek_trs = sang_lunch_tables[0].find_all('tr')
                sang_bek_menu = sang_bek_trs[0].text
                sang_bek_price = sang_bek_trs[1].text

                sang_ill_trs = sang_lunch_tables[1].find_all('tr')
                sang_ill_menu = sang_ill_trs[0].text
                sang_ill_price = sang_ill_trs[1].text

                sang_yang_trs = sang_lunch_tables[2].find_all('tr')
                sang_yang_menu = sang_yang_trs[0].text
                sang_yang_price = sang_yang_trs[1]. text

                sang_dduk_trs = sang_lunch_tables[3].find_all('tr')
                sang_dduk_menu = sang_dduk_trs[0].text
                sang_dduk_price = sang_dduk_trs[1].text

                create_menu_db_table('백반코너', '중식', sang_bek_menu + sang_bek_price)
                create_menu_db_table('일품코너', '중식', sang_ill_menu + sang_ill_price)
                create_menu_db_table('양식코너', '중식', sang_yang_menu + sang_yang_price)
                create_menu_db_table('뚝배기코너', '중식', sang_dduk_menu + sang_dduk_price)

            elif tr.find(text="석식"):
                sang_dinner_tables = tr.find_all('table')

                sang_ill_trs = sang_dinner_tables[1].find_all('tr')
                sang_ill_menu = sang_ill_trs[0].text
                sang_ill_price = sang_ill_trs[1].text

                sang_yang_trs = sang_dinner_tables[2].find_all('tr')
                sang_yang_menu = sang_yang_trs[0].text
                sang_yang_price = sang_yang_trs[1].text

                sang_dduk_trs = sang_dinner_tables[3].find_all('tr')
                sang_dduk_menu = sang_dduk_trs[0].text
                sang_dduk_price = sang_dduk_trs[1].text

                create_menu_db_table('일품코너', '석식', sang_ill_menu + sang_ill_price)
                create_menu_db_table('양식코너', '석식', sang_yang_menu + sang_yang_price)
                create_menu_db_table('뚝배기코너', '석식', sang_dduk_menu + sang_dduk_price)




    #그루터기
    if gru_table.find(text="휴무"):
        create_menu_db_table('A코너', '중식', '휴무 \n')
        create_menu_db_table('B코너', '중식', '휴무 \n')
        create_menu_db_table('A코너', '석식', '휴무 \n')
        create_menu_db_table('B코너', '석식', '휴무 \n')

    else:
        gru_trs = gru_table.find_all('tr')
        for tr in gru_trs:
            if tr.find(text="중식"):
                gru_lunch_tables = tr.find_all('table')

                gru_a_trs = gru_lunch_tables[0].find_all('tr')
                gru_a_menu = gru_a_trs[0].text
                gru_a_price = gru_a_trs[1].text

                gru_b_trs = gru_lunch_tables[1].find_all('tr')
                gru_b_menu = gru_b_trs[0].text
                gru_b_price = gru_b_trs[1].text

                create_menu_db_table('A코너', '중식', gru_a_menu + gru_a_price)
                create_menu_db_table('B코너', '중식', gru_b_menu + gru_b_price)

            elif tr.find(text='석식'):
                gru_dinner_tables = tr.find_all('table')

                gru_a_trs = gru_dinner_tables[0].find_all('tr')
                gru_a_menu = gru_a_trs[0].text
                gru_a_price = gru_a_trs[1].text

                gru_b_trs = gru_dinner_tables[1].find_all('tr')
                gru_b_menu = gru_b_trs[0].text
                gru_b_price = gru_b_trs[1].text

                create_menu_db_table('A코너', '석식', gru_a_menu + gru_a_price)
                create_menu_db_table('B코너', '석식', gru_b_menu + gru_b_price)


    #기숙사 식당
    if dorm_table.find(text="휴무"):
        create_menu_db_table('기숙사A코너', '중식', '휴무 \n')
        create_menu_db_table('기숙사B코너', '중식', '휴무 \n')
        create_menu_db_table('기숙사A코너', '석식', '휴무 \n')
        create_menu_db_table('기숙사B코너', '석식', '휴무 \n')

    else:
        # 중식이 검색이 안되는 문제 발생... 일단 원래 방법으로 구현해놓음
        dorm_trs = dorm_table.find_all('tr')
        dorm_lunch_tables = dorm_trs[5].find_all('table')

        dorm_a_trs = dorm_lunch_tables[0].find_all('tr')
        dorm_a_menu = dorm_a_trs[0].text
        dorm_a_price = dorm_a_trs[1].text

        dorm_b_trs = dorm_lunch_tables[1].find_all('tr')
        dorm_b_menu = dorm_b_trs[0].text
        dorm_b_price = dorm_b_trs[1].text

        create_menu_db_table('기숙사A코너', '중식', dorm_a_menu + dorm_a_price)
        create_menu_db_table('기숙사B코너', '중식', dorm_b_menu + dorm_b_price)

        for tr in dorm_trs:
            if tr.find(text='석식'):
                dorm_dinner_tables = tr.find_all('table')

                dorm_a_trs = dorm_dinner_tables[0].find_all('tr')
                dorm_a_menu = dorm_a_trs[0].text
                dorm_a_price = dorm_a_trs[1].text

                create_menu_db_table('기숙사A코너', '석식', dorm_a_menu + dorm_a_price)

    return JsonResponse({'status' : 'crawled'})


def create_menu_db_table(cafe_name, time, menu):
    Menu.objects.create(
        cafe_name=cafe_name,
        time=time,
        menu=menu,
        is_new=True
    )


def create_log(cafe_name):
    Log.objects.create(
        cafe_name = cafe_name
    )


def flush_menu_db():
    menu_db = Menu.objects.all()
    menu_db.delete()


#curl -XPOST 'http://127.0.0.1:8000/message' -d '{"user_key": "encryptedUserKey", "type": "text", "content": "뭐먹지?"}'
#curl -XGET 'http://127.0.0.1:8000/crawl/'


def analysis(request):

    context = {}
    context['date_pack'] = get_date_pack()
    context['total_request_data'] = get_total_request_data()
    context['seven_days_request_data'] = get_seven_days_request_data()
    context['request_data_by_cafe'] = get_request_data_by_cafe()
    context['weekday_request_data'] = get_weekday_request_data()
    context['hourly_request_data'] = get_hourly_request_data()
    context['request_by_time_data'] = get_time_request_data()

    return TemplateResponse(request, "index.html", context)


def get_today_date():

    return datetime.date.today()


def get_date_pack():
    days = 7
    today_date = get_today_date()
    date_pack = ['x']

    for i in reversed(range(days)):
        date = today_date - datetime.timedelta(days=i)
        date_pack.append(
            date.strftime('%Y-%m-%d')
        )

    return date_pack


def get_total_request_data():
    today_date = get_today_date()
    days_since_open = (today_date - datetime.date(2017, 9, 1)).days
    zero_data = ['요청횟수']
    total_request_data = ['요청횟수']

    for i in reversed(range(days_since_open)):
        total_request_data.append(
            Log.objects.filter(
                timestamp__range=[today_date - datetime.timedelta(days=i),
                                  today_date + datetime.timedelta(days=1 - i)]
            ).count()
        )
        zero_data.append(0)

    return dict(
        total_request_data=total_request_data,
        zero_data=zero_data,
    )


def get_seven_days_request_data():
    days = 7
    today_date = get_today_date()
    cnt_request = ['요청횟수']

    for i in reversed(range(days)):
        cnt_request.append(
            Log.objects.filter(
                timestamp__range = (today_date - datetime.timedelta(days=i),
                                    today_date + datetime.timedelta(days=1-i))
            ).count()
        )

    return cnt_request


def get_request_data_by_cafe():
    days = 7
    today_date = get_today_date()
    cnt_sang = ['상록원']
    cnt_gru = ['그루터기']
    cnt_dorm = ['기숙사식당']
    cnt_kyo = ['교직원식당']

    for i in reversed(range(days)):
        cnt_sang.append(
            Log.objects.filter(
                cafe_name='상록원',
                timestamp__range=(today_date - datetime.timedelta(days=i),
                                  today_date + datetime.timedelta(days=1 - i))
            ).count()
        )
        cnt_gru.append(
            Log.objects.filter(
                cafe_name='그루터기',
                timestamp__range=(today_date - datetime.timedelta(days=i),
                                  today_date + datetime.timedelta(days=1 - i))
            ).count()
        )
        cnt_dorm.append(
            Log.objects.filter(
                cafe_name='기숙사식당',
                timestamp__range=(today_date - datetime.timedelta(days=i),
                                  today_date + datetime.timedelta(days=1 - i))
            ).count()
        )
        cnt_kyo.append(
            Log.objects.filter(
                cafe_name='교직원식당',
                timestamp__range=(today_date - datetime.timedelta(days=i),
                                  today_date + datetime.timedelta(days=1 - i))
            ).count()
        )

    return dict(
        cnt_gru=cnt_gru,
        cnt_sang=cnt_sang,
        cnt_dorm=cnt_dorm,
        cnt_kyo=cnt_kyo
    )


def get_weekday_request_data():
    weekday_request_data = ['요청횟수']
    for i in range(1,8):
        weekday_request_data.append(
            Log.objects.filter(
                timestamp__week_day=i
            ).count()
        )

    return weekday_request_data


def get_hourly_request_data():
    hourly_request_data = ['요청횟수']
    for i in range(24):
        hourly_request_data.append(
            Log.objects.filter(
                timestamp__hour=i
            ).count()
        )

    return hourly_request_data


def get_time_request_data():
    days=7
    today_date = get_today_date()
    cnt_lunch = ['중식']
    cnt_dinner = ['석식']

    for i in reversed(range(days)):
        cnt_lunch.append(
            Log.objects.filter(
                timestamp__range=(today_date - datetime.timedelta(days=i),
                                  today_date + datetime.timedelta(days=1 - i)),
                timestamp__hour__lt = 15
            ).count()
        )
        cnt_dinner.append(
            Log.objects.filter(
                timestamp__range=(today_date - datetime.timedelta(days=i),
                                  today_date + datetime.timedelta(days=1 - i)),
                timestamp__hour__gte=15
            ).count()
        )

    return dict(
        cnt_lunch=cnt_lunch,
        cnt_dinner=cnt_dinner
    )
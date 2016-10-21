from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from dguhaksik.models import Menu, Log
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json, datetime


def keyboard(request):

    return JsonResponse({
        'type' : 'buttons',
        'buttons' : ['상록원', '그루터기', '기숙사식당', '교직원식당']
    })


@csrf_exempt
def answer(request):
    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    cafeteria_name = received_json_data['content']
    today_date = datetime.date.today().strftime("%m월 %d일")

    return JsonResponse({
        'message': {
            'text': today_date + '의 ' + cafeteria_name + '의 메뉴입니다. \n \n' + get_menu(cafeteria_name)
        },
        'keyboard': {
            'type': 'buttons',
            'buttons': ['상록원', '그루터기', '기숙사식당', '교직원식당']
        }

    })


def get_menu(cafeteria_name):
    create_log(cafeteria_name)
    if cafeteria_name == '상록원':
        sang_bek_lunch = Menu.objects.get(cafe_name='백반코너', time='중식').menu
        sang_ill_lunch = Menu.objects.get(cafe_name='일품코너', time='중식').menu
        sang_yang_lunch = Menu.objects.get(cafe_name='양식코너', time='중식').menu
        sang_dduk_lunch = Menu.objects.get(cafe_name='뚝배기코너', time='중식').menu

        sang_ill_dinner = Menu.objects.get(cafe_name='일품코너', time='석식').menu
        sang_yang_dinner = Menu.objects.get(cafe_name='양식코너', time='석식').menu
        sang_dduk_dinner = Menu.objects.get(cafe_name='뚝배기코너', time='석식').menu

        return "중식\n============\n" +  "백반코너 \n" + sang_bek_lunch \
               + "------------\n" + "일품코너 \n" + sang_ill_lunch \
               + "------------\n" + "양식코너 \n" + sang_yang_lunch \
               + "------------\n" + "뚝배기코너 \n" + sang_dduk_lunch \
               + "\n석식\n=============\n" + "일품코너 \n" + sang_ill_dinner \
               + "------------\n" + "양식코너 \n" + sang_yang_dinner \
               + "------------\n" + "뚝배기코너 \n" + sang_dduk_dinner




    elif cafeteria_name == '그루터기':
        gru_a = Menu.objects.get(cafe_name='A코너').menu
        gru_b = Menu.objects.get(cafe_name='B코너').menu

        return "------------\n" +  "A코너 \n" + gru_a \
               + "------------\n" + "B코너 \n" + gru_b

    elif cafeteria_name == '기숙사식당':
        dorm_a = Menu.objects.get(cafe_name='기숙사A코너').menu
        dorm_b = Menu.objects.get(cafe_name='기숙사B코너').menu

        return "------------\n" + "A코너 \n" + dorm_a \
               + "------------\n" + "B코너 \n" + dorm_b

    elif cafeteria_name == '교직원식당':
        kyo_jib = Menu.objects.get(cafe_name='집밥').menu
        kyo_han = Menu.objects.get(cafe_name='한그릇').menu

        return "------------\n" + "집밥 \n" + kyo_jib \
               + "------------\n" + "한그릇 \n" + kyo_han

    else:
        return "존재하지 않는 식당이거나 오류 발생중입니다."


def crawl(request):
    #메뉴 DB 테이블 비우기
    flush_menu_db()

    #메뉴 테이블 추출
    html = urlopen('http://dgucoop.dongguk.edu/store/store.php?w=4&l=1')
    source = html.read()
    html.close()
    soup = BeautifulSoup(source, "html.parser")
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

    else:
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


    #상록원
    if sang_table.find(text="휴무"):
        create_menu_db_table('백반코너', '중식', '휴무 \n')
        create_menu_db_table('일품코너', '중식', '휴무 \n')
        create_menu_db_table('양식코너', '중식', '휴무 \n')
        create_menu_db_table('뚝배기코너', '중식', '휴무 \n')

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


#curl -XPOST 'http://127.0.0.1:8000/message' -d '{"user_key": "encryptedUserKey", "type": "text", "content": "가든쿡"}'
#curl -XGET 'http://127.0.0.1:8000/crawl/'
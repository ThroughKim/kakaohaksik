from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from dguhaksik.models import Menu
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json, datetime


def keyboard(request):

    return JsonResponse({
        'type' : 'buttons',
        'buttons' : ['상록원', '그루터기', '아리수', '기숙사식당', '교직원식당']
    })


@csrf_exempt
def answer(request):
    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    cafeteria_name = received_json_data['content']
    today_date = datetime.date.today().strftime("%m월 %d일")

    if cafeteria_name == '상록원':
        return JsonResponse({
            'message':{
                'text': today_date + '의 상록원 중식 메뉴입니다. \n \n' + get_menu('상록원')
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['상록원', '그루터기', '아리수', '기숙사식당', '교직원식당']
            }

        })

    elif cafeteria_name == '그루터기':
        return JsonResponse({
            'message': {
                'text': today_date + '의 그루터기 중식 메뉴입니다. \n \n' + get_menu('그루터기')
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['상록원', '그루터기', '아리수', '기숙사식당', '교직원식당']
            }

        })

    elif cafeteria_name == '아리수':
        return JsonResponse({
            'message': {
                'text': today_date + '의 아리수 중식 메뉴입니다. \n \n' + get_menu('아리수')
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['상록원', '그루터기', '아리수', '기숙사식당', '교직원식당']
            }

        })

    elif cafeteria_name == '기숙사식당':
        return JsonResponse({
            'message': {
                'text': today_date + '의 기숙사식당 중식 메뉴입니다. \n \n' + get_menu('기숙사식당')
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['상록원', '그루터기', '아리수', '기숙사식당', '교직원식당']
            }

        })

    elif cafeteria_name == '교직원식당':
        return JsonResponse({
            'message': {
                'text': today_date + '의 교직원식당 중식 메뉴입니다. \n \n' + get_menu('교직원식당')
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['상록원', '그루터기', '아리수', '기숙사식당', '교직원식당']
            }

        })

    else:
        return JsonResponse({
            'message': {
                'text': '존재하지 않는 식당이거나 오류 발생중입니다.'
            }
        })


def get_menu(cafeteria_name):
    if cafeteria_name == '상록원':
        sang_bek = Menu.objects.get(cafe_name='백반코너').menu
        sang_ill = Menu.objects.get(cafe_name='일품코너').menu
        sang_yang = Menu.objects.get(cafe_name='양식코너').menu
        sang_dduk = Menu.objects.get(cafe_name='뚝배기코너').menu

        return "------------\n" +  "백반코너 \n" + sang_bek \
               + "------------\n" + "일품코너 \n" + sang_ill \
               + "------------\n" + "양식코너 \n" + sang_yang \
               + "------------\n" + "뚝배기코너 \n" + sang_dduk

    elif cafeteria_name == '그루터기':
        gru_a = Menu.objects.get(cafe_name='A코너').menu
        gru_b = Menu.objects.get(cafe_name='B코너').menu

        return "------------\n" +  "A코너 \n" + gru_a \
               + "------------\n" + "B코너 \n" + gru_b

    elif cafeteria_name == '아리수':
        ari = Menu.objects.get(cafe_name='아리수').menu

        return "------------\n" + "아리수 \n" + ari

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
    gru_table = menu_tables[4]
    ari_table = menu_tables[6]
    dorm_table = menu_tables[7]


    #교직원 식당
    if kyo_table.find(text="휴무"):
        Menu.objects.create(
            cafe_name='집밥',
            time='중식',
            menu='휴무 \n',
            is_new=True
        )
        Menu.objects.create(
            cafe_name='한그릇',
            time='중식',
            menu='휴무 \n',
            is_new=True
        )

    else:
        kyo_trs = kyo_table.find_all('tr')
        kyo_tables = kyo_trs[1].find_all('table')

        kyo_jib_trs = kyo_tables[0].find_all('tr')
        kyo_jib_menu = kyo_jib_trs[0].text
        kyo_jib_price = kyo_jib_trs[1].text

        kyo_han_trs = kyo_tables[1].find_all('tr')
        kyo_han_menu = kyo_han_trs[0].text
        kyo_han_price = kyo_han_trs[1].text

        Menu.objects.create(
            cafe_name='집밥',
            time='중식',
            menu=kyo_jib_menu + kyo_jib_price,
            is_new=True
        )
        Menu.objects.create(
            cafe_name='한그릇',
            time='중식',
            menu=kyo_han_menu + kyo_han_price,
            is_new=True
        )


    #상록원
    if sang_table.find(text="휴무"):
        Menu.objects.create(
            cafe_name='백반코너',
            time='중식',
            menu='휴무 \n',
            is_new=True
        )
        Menu.objects.create(
            cafe_name='뚝배기코너',
            time='중식',
            menu='휴무 \n',
            is_new=True
        )
        Menu.objects.create(
            cafe_name='일품코너',
            time='중식',
            menu='휴무 \n',
            is_new=True
        )
        Menu.objects.create(
            cafe_name='양식코너',
            time='중식',
            menu='휴무 \n',
            is_new=True
        )

    else:
        sang_trs = sang_table.find_all('tr')
        sang_tables = sang_trs[1].find_all('table')

        sang_bek_trs = sang_tables[0].find_all('tr')
        sang_bek_menu = sang_bek_trs[0].text
        sang_bek_price = sang_bek_trs[1].text

        sang_ill_trs = sang_tables[1].find_all('tr')
        sang_ill_menu = sang_ill_trs[0].text
        sang_ill_price = sang_ill_trs[1].text

        sang_yang_trs = sang_tables[2].find_all('tr')
        sang_yang_menu = sang_yang_trs[0].text
        sang_yang_price = sang_yang_trs[1]. text

        sang_dduk_trs = sang_tables[3].find_all('tr')
        sang_dduk_menu = sang_dduk_trs[0].text
        sang_dduk_price = sang_dduk_trs[1].text

        Menu.objects.create(
            cafe_name='백반코너',
            time='중식',
            menu=sang_bek_menu + sang_bek_price,
            is_new=True
        )
        Menu.objects.create(
            cafe_name='일품코너',
            time='중식',
            menu=sang_ill_menu + sang_ill_price,
            is_new=True
        )
        Menu.objects.create(
            cafe_name='양식코너',
            time='중식',
            menu=sang_yang_menu + sang_yang_price,
            is_new=True
        )
        Menu.objects.create(
            cafe_name='뚝배기코너',
            time='중식',
            menu=sang_dduk_menu + sang_dduk_price,
            is_new=True
        )


    #그루터기
    if gru_table.find(text="휴무"):
        Menu.objects.create(
            cafe_name='A코너',
            time='중식',
            menu='휴무 \n',
            is_new=True
        )
        Menu.objects.create(
            cafe_name='B코너',
            time='중식',
            menu='휴무 \n',
            is_new=True
        )

    else:
        gru_trs = gru_table.find_all('tr')
        gru_tables = gru_trs[1].find_all('tables')

        gru_a_trs = gru_tables[0].find_all('tr')
        gru_a_menu = gru_a_trs[0].text
        gru_a_price = gru_a_trs[1].text

        gru_b_trs = gru_tables[1].find_all('tr')
        gru_b_menu = gru_b_trs[0].text
        gru_b_price = gru_b_trs[1].text

        Menu.objects.create(
            cafe_name='A코너',
            time='중식',
            menu=gru_a_menu + gru_a_price,
            is_new=True
        )
        Menu.objects.create(
            cafe_name='B코너',
            time='중식',
            menu=gru_b_menu + gru_b_price,
            is_new=True
        )


    #아리수
    if ari_table.find(text="휴무"):
        Menu.objects.create(
            cafe_name='아리수',
            time='중식',
            menu='휴무 \n',
            is_new=True
        )


    else:
        ari_trs = ari_table.find_all('tr')
        ari_tables = ari_trs[1].find_all('tables')
        ari_trs = ari_tables[0].find_all('tr')
        ari_menu = ari_trs[0].text
        ari_price = ari_trs[1].text

        Menu.objects.create(
            cafe_name='아리수',
            time='중식',
            menu=ari_menu + ari_price,
            is_new=True
        )


    #기숙사 식당
    if dorm_table.find(text="휴무"):
        Menu.objects.create(
            cafe_name='기숙사A코너',
            time='중식',
            menu='휴무 \n',
            is_new=True
        )
        Menu.objects.create(
            cafe_name='기숙사B코너',
            time='중식',
            menu='휴무 \n',
            is_new=True
        )

    else:
        dorm_trs = dorm_table.find_all('tr')
        dorm_tables = dorm_trs[5].find_all('table')

        dorm_a_trs = dorm_tables[0].find_all('tr')
        dorm_a_menu = dorm_a_trs[0].text
        dorm_a_price = dorm_a_trs[1].text

        dorm_b_trs = dorm_tables[1].find_all('tr')
        dorm_b_menu = dorm_b_trs[0].text
        dorm_b_price = dorm_b_trs[1].text

        Menu.objects.create(
            cafe_name='기숙사A코너',
            time='중식',
            menu=dorm_a_menu + dorm_a_price,
            is_new=True
        )
        Menu.objects.create(
            cafe_name='기숙사B코너',
            time='중식',
            menu=dorm_b_menu + dorm_b_price,
            is_new=True
        )


    return JsonResponse({'status' : 'crawled'})


def flush_menu_db():
    menu_db = Menu.objects.all()
    menu_db.delete()


#curl -XPOST 'http://127.0.0.1:8000/message' -d '{"user_key": "encryptedUserKey", "type": "text", "content": "아리수"}'
#curl -XGET 'http://127.0.0.1:8000/crawl/'
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from dguhaksik.models import Menu
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json, datetime

# Create your views here.
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

    return JsonResponse({
        'message' : {
            'text' : cafeteria_name + '의 메뉴입니다 \n준비중입니다.'
        },
        'keyboard' : {
            'type' : 'buttons',
            'buttons' : ['상록원', '그루터기', '아리수', '기숙사식당', '교직원식당']
        }
    })

def crawl(request):
    today_date = datetime.date.today()
    today_span_num = today_date.isoweekday() + 2

    html = urlopen('http://dgucoop.dongguk.edu/store/store.php?w=4&l=1')
    source = html.read()
    html.close()
    soup = BeautifulSoup(source, "html.parser")
    table_div = soup.find(id="sdetail")
    menu_tables = table_div.table.tr.td.p.find_all('table', {"bgcolor": "#CDD6B5"})

    kyo_table = menu_tables[0]
    sang_table = menu_tables[1]
    gru_table = menu_tables[4]
    ari_table = menu_tables[6]
    dorm_table = menu_tables[7]

    if kyo_table.find(text="휴무"):
        Menu.objects.create(
            name='집밥',
            time='중식',
            menu='휴무'
        )
        Menu.objects.create(
            name='한그릇',
            time='중식',
            menu='휴무'
        )

    else:
        print("메뉴")


    if sang_table.find(text="휴무"):
        Menu.objects.create(
            name='백반코너',
            time='중식',
            menu='휴무'
        )
        Menu.objects.create(
            name='뚝배기코너',
            time='중식',
            menu='휴무'
        )
        Menu.objects.create(
            name='일품코너',
            time='중식',
            menu='휴무'
        )
        Menu.objects.create(
            name='양식코너',
            time='중식',
            menu='휴무'
        )

    else:
        print("메뉴")

    if gru_table.find(text="휴무"):
        Menu.objects.create(
            name='A코너',
            time='중식',
            menu='휴무'
        )
        Menu.objects.create(
            name='B코너',
            time='중식',
            menu='휴무'
        )

    else:
        print("메뉴")



    """
    sang_bek_tds = rs[8].find_all('td')
    try:
        sang_bek_today_spans = sang_bek_tds[today_span_num].find_all('span')
        sang_bek_menu = sang_bek_today_spans[0].text
        sang_bek_price = sang_bek_today_spans[1].text
    except IndexError:
        sang_bek_menu = "준비중입니다"
        sang_bek_price = "준비중입니다"

    Menu.objects.create(
        name='백반코너',
        menu=sang_bek_menu + '\r\n' + sang_bek_price
    )
    """

    return JsonResponse({})

def flush_menu_db():
    menu_db = Menu.objects.all()
    menu_db.delete()


#curl -XPOST 'http://127.0.0.1:8000/message' -d '{"user_key": "encryptedUserKey", "type": "text", "content": "차량번호등록"}'
#curl -XGET 'http://127.0.0.1:8000/crawl/'
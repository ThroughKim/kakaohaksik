from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

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
            'text' : cafeteria_name + '의 메뉴입니다 \r\n 준비중입니다.'
        }
    })

@csrf_exempt
def friend(request):

    return JsonResponse({

    })

#curl -XPOST 'http://127.0.0.1:8000/message' -d '{"user_key": "encryptedUserKey", "type": "text", "content": "차량번호등록"}'
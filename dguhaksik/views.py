from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.
def keyboard(request):

    return JsonResponse({
        'type' : 'buttons',
        'buttons' : ['상록원', '그루터기', '아리수', '기숙사식당', '교직원식당']})

@csrf_exempt
def answer(request):

    #cafeteria_name = request.POST.get("content")

    return JsonResponse({
        'message' : {
            'text' : '메뉴를 준비중입니다.'
        }
    })


#curl -XPOST 'https://127.0.0.1/message' -d '{"user_key": "encryptedUserKey", "type": "text", "content": "차량번호등록"}'
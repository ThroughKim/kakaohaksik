from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# Create your views here.

def keyboard(request):

    return JsonResponse({
        'type' : 'text',
        'content': '닉네임을 입력해주세요.'
    })

@csrf_exempt
def answer(request):
    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    nickname = received_json_data['content']

    return JsonResponse({
        'message': {
            'text': nickname + "의 전적"
        },
        'keyboard': {
            'type' : 'text',
            'content': '닉네임을 입력해주세요.'
        }
    })
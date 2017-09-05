from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.

def keyboard(request):

    return JsonResponse({
        'type' : 'text',
        'content': '닉네임을 입력해주세요.'
    })
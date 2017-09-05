from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.

def keyboard(request):

    return JsonResponse({
        'type' : 'buttons',
        'buttons' : ['닉네임입력']
    })
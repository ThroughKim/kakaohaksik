from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def keyboard(request):

    return JsonResponse({
        'type' : 'buttons',
        'buttons' : ['상록원', '그루터기', '아리수', '기숙사식당', '교직원식당']})

def answer(request):

    return JsonResponse({
        "text" : "메뉴를 준비중입니다"
    })
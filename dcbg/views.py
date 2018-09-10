from functools import reduce
from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db.models import Count, Q, Sum
from dcbg.models import Chat
from operator import or_
import dateutil.parser
import os, csv

def analysis(request):
    context = {}
    context['talker_data'] = get_talker_data()
    context['goma_data'] = get_goma_data()
    context['sex_data'] = get_sex_data()
    context['pic_data'] = get_pic_data()
    context['pubg_data'] = get_pubg_data()

    return TemplateResponse(request, 'analysis.html', context)

@csrf_exempt
def get_word_data(request):
    if request.POST.get('word'):
        word = request.POST.get('word')

        return JsonResponse(get_word_counts([word]), safe=False)


def get_talker_data():
    data = Chat.objects.values(
        'sender'
    ).exclude(
        sender='(알수없음)'
    ).annotate(
        count=Count('sender')
    ).order_by(
        '-count'
    )[:15]

    result = []
    for d in data:
        if d['sender'] == '972':
            d['sender'] = '정규철'
        arr = [
            d['sender'],
            d['count']
        ]
        result.append(arr)

    return result

def get_goma_data():
    return get_word_counts(['goma', '고마'])


def get_sex_data():
    return get_word_counts(['섹', '쎅', '쎆', 'sex'])


def get_pic_data():
    data = Chat.objects.values(
        'sender'
    ).exclude(
        sender='(알수없음)'
    ).filter(
        content='사진'
    ).annotate(
        count=Count('sender')
    ).order_by(
        '-count'
    )[:15]

    result = []

    for d in data:
        if d['sender'] == '972':
            d['sender'] = '정규철'
        arr = [
            d['sender'],
            d['count']
        ]
        result.append(arr)

    return result

def get_pubg_data():
    return get_word_counts(['사녹', '배그', '미라마', '에란겔'])


def get_word_counts(word_list):
    data = Chat.objects.values(
        'sender'
    ).exclude(
        sender='(알수없음)'
    ).filter(
        reduce(or_, [Q(content__icontains=q) for q in word_list])
    ).annotate(
        count=Count('sender')
    ).order_by(
        '-count'
    )[:15]

    result = []

    for d in data:
        if d['sender'] == '972':
            d['sender'] = '정규철'
        arr = [
            d['sender'],
            d['count']
        ]
        result.append(arr)

    return result

def crawl(request):
    file_path = os.path.join(settings.BASE_DIR, 'dcbg.csv')
    with open(file_path, encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)      #Skip header
        cnt = 0
        for row in reader:
            try:
                _, created = Chat.objects.get_or_create(
                    sender = row[1],
                    content = row[2],
                    time = dateutil.parser.parse(row[0])
                )
            except:
                print("ERROR")
                print(row)
            finally:
                cnt = cnt + 1
                print(str(cnt) + "개 완료")

    return JsonResponse({
        'crawl': 'done'
    })
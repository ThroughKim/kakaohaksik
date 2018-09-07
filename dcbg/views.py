from django.template.response import TemplateResponse
from django.http import JsonResponse
from django.conf import settings
from dcbg.models import Chat
import dateutil.parser
import os, csv

def analysis(request):
    context = {}

    return TemplateResponse(request, 'analysis.html', context)

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
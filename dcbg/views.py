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
        for row in reader:
            _, created = Chat.objects.get_or_create(
                sender = row[1],
                content = row[2],
                time = dateutil.parser.parse(row[0])
            )

    return JsonResponse({
        'crawl': 'done'
    })
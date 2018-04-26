from django.http import JsonResponse
from bs4 import BeautifulSoup
from urllib.request import urlopen
from dossa.models import Log, Post
import smtplib
from email.mime.text import MIMEText
import os
from django.conf import settings

def noti(request):

    urls = [
        'http://corearoadbike.com/board/board.php?t_id=Menu30Top6&category=%ED%8C%90%EB%A7%A4',
        'http://corearoadbike.com/board/board.php?t_id=Menu01Top6&category=%ED%8C%90%EB%A7%A4'
    ]

    keywords = [
        '파스포츠', '튜블리스', 'slr0', '튜브리스',
        'm/l', '56', '56', '55'
    ]

    posts = []
    for url in urls:
        post_list = get_post(url)
        for post in post_list:
            posts.append(post)

    new_posts = []

    for post in reversed(posts):
        saved_post, created = Post.objects.update_or_create(title=post["title"], link=post['link'])
        if created:
            for word in keywords:
                if word in post["title"]:
                    new_posts.append(post)

    if len(new_posts) > 0:
        send_mail(new_posts)

    Log.objects.create(success=True)
    return JsonResponse({

        'result': 'success'
    })


def get_post(url):
    html = urlopen(url)
    source = html.read()
    html.close()
    soup = BeautifulSoup(source, "html.parser", from_encoding='utf-8')
    title_tds = soup.find_all("td", {'class': 'list_title_B'})
    posts = list(map(lambda t: {
        "title":t.a.text,
        "link": "http://corearoadbike.com/board" + t.a["href"][1:]
    }, title_tds))

    return posts

def send_mail(new_posts):
    text = ""
    for post in new_posts:
        text += post['title'] + "- " + post['link'] + "\n"

    mail_addr = 'jsjsv@naver.com'
    msg = MIMEText(text)

    # me == 보내는 사람의 이메일 주소
    # you == 받는 사람의 이메일 주소
    msg['Subject'] = "도싸장터 새 글 알림"  # 이메일 제목
    msg['From'] = mail_addr
    msg['To'] = mail_addr

    # 로컬 SMTP 서버가 없을 경우 계정이 있는 다른 서버를 사용하면 된다.
    key = open(os.path.join(settings.BASE_DIR, 'key'))
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.login("sulewoo58", key.readline())
    s.sendmail('sulewoo59@gmail.com', mail_addr, msg.as_string())
    s.quit()

from django.conf.urls import url

urlpatterns = [
    url(r'^keyboard/', 'dguhaksik.views.keyboard'),
    url(r'^message', 'dguhaksik.views.answer'),
    url(r'^crawl/', 'dguhaksik.views.crawl'),
]
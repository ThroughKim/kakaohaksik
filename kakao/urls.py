from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^keyboard/', 'dguhaksik.views.keyboard'),
    url(r'^message', 'dguhaksik.views.answer'),
    url(r'^crawl/', 'dguhaksik.views.crawl'),
    url(r'^analysis/', 'dguhaksik.views.analysis'),
    url(r'^lda/', 'dguhaksik.views.lda'),
    url(r'^viewer/', 'dguhaksik.views.lda_view'),
    url(r'^pubg/keyboard', 'pubgbot.views.keyboard'),
]

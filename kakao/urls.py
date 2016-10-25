from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^keyboard/', 'dguhaksik.views.keyboard'),
    url(r'^message', 'dguhaksik.views.answer'),
    url(r'^crawl/', 'dguhaksik.views.crawl'),
    url(r'^', 'dguhaksik.views.analysis'),
]
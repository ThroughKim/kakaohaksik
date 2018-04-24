from django.conf.urls import url, include
from django.contrib import admin
from dguhaksik import views as dgu_views
from pubgbot import views as pubg_views
from dossa import views as dossa_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^keyboard/', dgu_views.keyboard),
    url(r'^message', dgu_views.answer),
    url(r'^crawl/', dgu_views.crawl),
    url(r'^analysis/', dgu_views.analysis),
    url(r'^lda/', dgu_views.lda),
    url(r'^viewer/', dgu_views.lda_view),
    url(r'^pubg/keyboard/', pubg_views.keyboard),
    url(r'^pubg/message', pubg_views.answer),
    url(r'^dossa/', dossa_views.noti),
]

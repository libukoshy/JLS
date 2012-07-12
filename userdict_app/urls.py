from django.conf.urls import patterns, include, url
import userdict_app.views

urlpatterns = patterns('',
    url(r'list/(?P<page>\d+)/$', 'userdict_app.views.kanji_list', name='kanji_list'),


)

from django.conf.urls import patterns, include, url
import userdict_app.views

urlpatterns = patterns('',
    url(r'list/(?P<page>\d+)/$', 'userdict_app.views.kanji_list', name='kanji_list'),
    url(r'add_to_user_dict/$', 'userdict_app.views.add_kanji_to_userdict', name='add_kanji_to_user_dict'),
    url(r'remove_from_user_dict/$', 'userdict_app.views.remove_kanji_from_userdict', name='remove_kanji_from_user_dict'),

)

from django.conf.urls import patterns, include, url
from django.contrib import admin
import userdict_app

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'userdict_app.views.mainpage', name='mainpage'),
    url(r'^profile/$', 'userdict_app.views.profile_page', name='profile'),
    url(r'^kanji/', include('userdict_app.urls')),
    # admin urls
    url(r'^admin/', include(admin.site.urls)),
    # auth urls                   
    url(r'^login/', 'django.contrib.auth.views.login', {'template_name':'login_page.html'}, name='login'),
    url(r'^logout/', 'django.contrib.auth.views.logout', name='logout'),

)

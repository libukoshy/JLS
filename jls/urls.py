from django.conf.urls import patterns, include, url
from django.contrib import admin
import userdict_app

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'userdict_app.views.mainpage', name='mainpage'),
    # url(r'^jls/', include('jls.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

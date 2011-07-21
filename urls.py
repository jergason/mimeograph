from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mimeograph.views.home', name='home'),
    # url(r'^mimeograph/', include('mimeograph.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', direct_to_template, { 'template': 'home.html' }),
    # url(r'^feed/$', 'mimeograph.mime.feed', 
)

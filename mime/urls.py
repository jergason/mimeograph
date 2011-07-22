from django.conf.urls.defaults import *

urlpatterns = patterns('mime.views',
    url(r'^$', 'own_feed'),
    url(r'^(?P<user_name>\w+)/$', 'other_feed'),
    url(r'^(?P<user_name>\w+)/follow$', 'follow'),
)

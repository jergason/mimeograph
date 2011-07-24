from django.conf.urls.defaults import *

urlpatterns = patterns('mime.views',
    url(r'^$', 'own_feed'),
    url(r'^create_mime/$', 'mime_create'),
    url(r'^delete_mime/$', 'mime_delete'),
    url(r'^(?P<user_name>\w+)/$', 'other_feed'),
    url(r'^(?P<user_name>\w+)/follow/$', 'follow'),
    url(r'^(?P<user_name>\w+)/unfollow/$', 'unfollow'),
)

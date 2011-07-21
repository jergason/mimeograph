from django.conf.urls.defaults import *

urlpatterns = patterns('mime.views',
    url(r'^$', 'feed'),
    # url(),
)

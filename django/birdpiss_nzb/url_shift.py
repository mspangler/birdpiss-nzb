from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^nzb/', include('urls')),
)

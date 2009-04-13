from django.conf.urls.defaults import *
from nzb.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^birdpiss_nzb/', include('birdpiss_nzb.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/(.*)', admin.site.root),
     
     url(r'^json/(?P<media>\w+)/$', get_json, name="get_json"),
     url(r'^upload/$', upload_nzb, name="upload_nzb"),
     
     (r'^$', index),
)

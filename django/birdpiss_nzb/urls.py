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
     url(r'^download/(?P<ids>.*)/$', download, name="download"),
     url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
     url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'registration/logout.html'}, name="logout"),
     url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="account_login"),
     url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'registration/logout.html'}, name="account_logout"),
     url(r'^accounts/$', 'django.contrib.auth.views.login', name="accounts_root"),
     
     
     url(r'^$', index, name="root_url"),
)

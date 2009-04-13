from django.contrib import admin
from nzb.models import *

class NzbAdmin(admin.ModelAdmin):
    list_display = ('title', 'media', 'newsgroup', 'size',)
    list_filter = ('media', 'newsgroup', )
    search_fields = ['title']


admin.site.register(Nzb, NzbAdmin)
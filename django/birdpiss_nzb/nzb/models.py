from django.db import models
from django.contrib.auth.models import User

class Nzb(models.Model):
    title = models.CharField(blank=False, max_length=50)
    newsgroup = models.CharField(blank=True, max_length=50)
    size = models.CharField(blank=True, max_length=10)
    xml_data = models.TextField(blank=False)
    # this media field should probably be a foreignkey
    # but as simple as it is right now meh....
    media = models.CharField(blank=False, max_length=25)
    user = models.ForeignKey(User)
    file_age = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ('-created',)

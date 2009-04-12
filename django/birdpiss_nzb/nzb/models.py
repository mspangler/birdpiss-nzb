from django.db import models

class Nzb(models.Model):
    title = models.CharField(blank=False, max_length=50)
    newsgroup = models.CharField(blank=True, max_length=25)
    size = models.CharField(blank=True, max_length=10)
    xml_data = models.TextField(blank=False)
    # this media field should probably be a foreignkey
    # but as simple as it is right now meh....
    media = models.CharField(blank=False, max_length=25)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

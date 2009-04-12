from django.db import models

class Nzb(models.Model):
    title = models.CharField(blank=False, max_length=50)
    newsgroup = models.CharField(blank=True, max_length=25)
    size = models.CharField(blank=True, max_length=10)
    xml_data = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

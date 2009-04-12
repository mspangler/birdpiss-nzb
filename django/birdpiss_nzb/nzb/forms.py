from django import forms

unit_choices = ( ('GB', 'GB'), ('MB', 'MB'))
media_choices = ( ('music', 'music'), ('movies', 'movies'), ('software', 'software'))

class NzbUpload(forms.Form):
    usenet_file = forms.FileField()
    title = forms.CharField()
    newsgroup = forms.CharField(required=False)
    media = forms.ChoiceField(choices=media_choices)
    size = forms.FloatField()
    unit = forms.ChoiceField(choices=unit_choices)

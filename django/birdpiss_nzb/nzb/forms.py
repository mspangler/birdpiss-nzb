from django import forms

unit_choices = ( ('GB', 'GB'), ('MB', 'MB'))

class NzbUpload(forms.Form):
    usenet_file = forms.FileField()
    title = forms.CharField()
    newsgroup = forms.CharField(required=False)
    size = forms.FloatField()
    unit = forms.ChoiceField(choices=unit_choices)

from django import forms

class ShortURLForm(forms.Form):
    original_url = forms.URLField(label='原網址', required=True)
    password = forms.CharField(label='密碼', required=False)
    note = forms.CharField(label='備註', required=False, widget=forms.Textarea)



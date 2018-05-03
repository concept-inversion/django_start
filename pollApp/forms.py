from django import forms

class UploadForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    your_address = forms.CharField(label='Your address', max_length=100)
from django import forms


class UploadFileForm(forms.Form):
    files = forms.FileField(label='Files to Upload', widget=forms.ClearableFileInput(attrs={'multiple': True}))

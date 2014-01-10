from django import forms

class PostForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)
    passphrase = forms.CharField(widget=forms.PasswordInput)

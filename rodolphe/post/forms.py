from django import forms

#class PostForm(forms.Form):
#    title = forms.CharField(max_length=100)
#    content = forms.CharField(widget=forms.Textarea)
#    passphrase = forms.CharField(widget=forms.PasswordInput)

from post.models import Post

class PostForm(forms.ModelForm):
    passkey = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Post
        fields = ('title', 'content')
    def save(self, commit=True):
        post = super().save(commit=False)
        if not post.hash_id:
            post.set_passkey(self.cleaned_data['passkey'])
        if commit:
            post.save()
        return post

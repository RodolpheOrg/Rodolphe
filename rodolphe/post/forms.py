from django import forms

from post.models import Post

class PostForm(forms.ModelForm):
    passkey = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Post
        fields = ('content', 'picture')
    def save(self, commit=True):
        post = super().save(commit=False)
        post.set_passkey(self.cleaned_data['passkey'])
        if commit:
            post.save()
        return post
    def clean(self):
        cleaned_data = super().clean()
        if hasattr(self, 'instance') and self.instance.hash_id:
            if self.instance.hash_id != Post.gen_passkey(self.instance.uuid, cleaned_data['passkey']):
                raise forms.ValidationError('passkeys differ')
        return cleaned_data

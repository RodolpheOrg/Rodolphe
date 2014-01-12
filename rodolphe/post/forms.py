from django import forms
from django.utils.translation import ugettext as _

from post.models import Post

class PostForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label=_('password'))
    class Meta:
        model = Post
        fields = ('content', 'picture')
    def save(self, commit=True):
        post = super().save(commit=False)
        post.set_password(self.cleaned_data['password'])
        post.set_author(self.cleaned_data['password'])
        if commit:
            post.save()
        return post
    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('content', None) and not cleaned_data.get('picture', None):
            raise forms.ValidationError(_('should put content or picture'))
        if hasattr(self, 'instance') and self.instance.hash_id:
            if self.instance.hash_id != Post.gen_password(self.instance.uuid, cleaned_data['password']):
                raise forms.ValidationError(_('passwords differ'))
        return cleaned_data

class DeletePostForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label=_('password'))
    class Meta:
        model = Post
        fields = ()
    def clean(self):
        cleaned_data = super().clean()
        if hasattr(self, 'instance') and self.instance.hash_id:
            if self.instance.hash_id != Post.gen_password(self.instance.uuid, cleaned_data['password']):
                raise forms.ValidationError(_('passwords differ'))
        return cleaned_data

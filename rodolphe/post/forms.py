from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _

from post.models import Post, Tag
from captcha.fields import CaptchaField


def check_password(form, password):
    if hasattr(form, 'instance') and form.instance.hash_id:
        if password == settings.MASTER_PASSWORD:
            return
        h = form.instance.hash_id
        if not isinstance(h, bytes):
            h = bytes(h)
        if h != Post.gen_password(form.instance.uuid, password):
            raise forms.ValidationError(_('passwords differ'))


class PostForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label=_('password'))
    captcha = CaptchaField()

    class Meta:
        model = Post
        fields = ('content', 'picture')

    def save(self, commit=True):
        post = super().save(commit=False)
        if not post.hash_id:
            post.set_password(self.cleaned_data['password'])
            post.set_author(self.cleaned_data['password'])
        for tag in post.tags:
            Tag.register(tag)
        if commit:
            post.save()
        return post

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('content', None) and \
           not cleaned_data.get('picture', None):
            raise forms.ValidationError(_('should put content or picture'))
        check_password(self, cleaned_data['password'])
        return cleaned_data


class DeletePostForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label=_('password'))
    captcha = CaptchaField()

    class Meta:
        model = Post
        fields = ()

    def clean(self):
        cleaned_data = super().clean()
        check_password(self, cleaned_data['password'])
        return cleaned_data

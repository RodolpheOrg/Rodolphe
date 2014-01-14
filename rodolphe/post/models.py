from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils import timezone

from utils.fields import UUIDField

from uuid import uuid4
import hashlib
import os.path
from faker import Faker

faker = Faker(settings.LANGUAGE_CODE)

# Create your models here.


def get_upload_image_name(_, filename):
    _, ext = os.path.splitext(filename)
    return 'pics/{}{}'.format(uuid4().int, ext)


class Author(models.Model):
    hash_id = models.BinaryField(max_length=20)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    uuid = UUIDField()
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('Post', blank=True, null=True,
                               related_name='post_parent')
    old_post = models.ForeignKey('Post', blank=True, null=True,
                                 related_name='post_old')
    content = models.TextField(blank=True, verbose_name=_('content'))
    picture = models.ImageField(upload_to=get_upload_image_name, blank=True,
                                verbose_name=_('picture'))
    hash_id = models.BinaryField(max_length=20)
    author = models.ForeignKey(Author)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)
    last_resp_at = models.DateTimeField()

    def __str__(self):
        return '#{}'.format(self.id)

    @property
    def responses(self):
        return Post.objects.filter(active=True, parent=self).order_by('created_at')

    @property
    def thread(self):
        return self.parent if self.parent else self

    @staticmethod
    def gen_password(uuid, key):
        h = hashlib.sha1(uuid.bytes)
        h.update(key.encode())
        return h.digest()

    def set_password(self, key):
        self.hash_id = self.gen_password(self.uuid, key)

    def set_author(self, key):
        hash_id = self.gen_password(self.thread.uuid, key)
        try:
            author = Author.objects.get(hash_id=hash_id)
        except Author.DoesNotExist:
            author = Author(hash_id=hash_id, name=faker.name())
            author.save()
        self.author = author

    @classmethod
    def default(cls, *args, **kwargs):
        now = timezone.now()
        return cls(uuid=uuid4(),
                   created_at=now,
                   last_resp_at=now,
                   *args,
                   **kwargs)

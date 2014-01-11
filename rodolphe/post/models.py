from django.db import models

from rodolphe.fields import UUIDField

from uuid import uuid4
import hashlib
import datetime
import os.path

# Create your models here.

def get_upload_image_name(_, filename):
    _, ext = os.path.splitext(filename)
    return 'pics/{}{}'.format(uuid4().int, ext)

class Post(models.Model):
    uuid = UUIDField()
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('Post', blank=True, null=True, related_name='post_parent')
    old_post = models.ForeignKey('Post', blank=True, null=True, related_name='post_old')
    content = models.TextField(blank=True)
    picture = models.ImageField(upload_to=get_upload_image_name, blank=True)
    hash_id = models.BinaryField(max_length=20)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return '#{}'.format(self.id)

    @property
    def responses(self):
        return Post.objects.filter(active=True, parent=self)
    @property
    def thread(self):
        return self.parent if self.parent else self

    @staticmethod
    def gen_passkey(uuid, key):
        h = hashlib.sha1(uuid.bytes)
        h.update(key.encode())
        return h.digest()
    def set_passkey(self, key):
        self.hash_id = self.gen_passkey(self.uuid, key)

    @classmethod
    def default(cls, *args, **kwargs):
        return cls(uuid=uuid4(), created_at=datetime.datetime.now(), *args, **kwargs)

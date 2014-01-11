from django.db import models

from rodolphe.fields import UUIDField

from uuid import uuid4
import hashlib

# Create your models here.

class Post(models.Model):
    uuid = UUIDField()
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('Post', blank=True, null=True)
    content = models.TextField()
    picture = models.ImageField(upload_to='pics/', blank=True)
    hash_id = models.BinaryField(max_length=20)

    def __str__(self):
        return '#{}'.format(self.id)

    @property
    def responses(self):
        return Post.objects.filter(parent=self)
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
        return cls(uuid=uuid4(), *args, **kwargs)

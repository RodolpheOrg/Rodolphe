from django.db import models
from django.conf import settings
from django.core.validators import MaxLengthValidator
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from utils.fields import UUIDField

from uuid import uuid4
import hashlib
import os.path
import re
from faker import Faker
#from PIL import Image

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


class Tag(models.Model):
    name = models.CharField(max_length=100)
    count = models.IntegerField(default=1)

    @classmethod
    def register(cls, name):
        try:
            tag = cls.objects.get(name=name)
            tag.count += 1
        except ObjectDoesNotExist:
            tag = Tag(name=name)
        tag.save()
        return tag


class Post(models.Model):
    uuid = UUIDField()
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('Post', blank=True, null=True,
                               related_name='post_parent')
    old_post = models.ForeignKey('Post', blank=True, null=True,
                                 related_name='post_old')
    content = models.TextField(blank=True,
                               validators=[MaxLengthValidator(5000)],
                               verbose_name=_('content'))
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

    @property
    def is_parent(self):
        return False if self.parent else True

    @property
    def tags(self):
        match = re.findall(r'(\A|\s)\.(\w+)', self.content)
        return [m[1] for m in match]

    #@property
    #def thumbnail(self):
    #    if not self.picture:
    #        return None
    #    base, ext = os.path.splitext(self.picture.url)
    #    thumb_url = '{}_thumb{}'.format(base, ext)
    #    thumb_rel = os.path.normpath('./' + thumb_url)
    #    if not os.path.exists(thumb_rel):
    #        pic_rel = os.path.normpath('./' + self.picture.url)
    #        print(pic_rel, thumb_rel)
    #        image = Image.open(pic_rel)
    #        image.thumbnail((300, 300), Image.ANTIALIAS)
    #        image.save(thumb_rel)
    #    return thumb_url

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

from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('Post', blank=True, null=True)
    content = models.TextField()
    hash_id = models.BigIntegerField()

    def __str__(self):
        return '#{}'.format(self.id)

    @property
    def responses(self):
        return Post.objects.filter(parent=self)

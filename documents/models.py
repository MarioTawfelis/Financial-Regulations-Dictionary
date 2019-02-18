from django.db import models
from accounts.models import User
from django.db.models import PROTECT
from taggit.managers import TaggableManager


class Document(models.Model):
    name = models.CharField(max_length=4000)
    url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=True)
    tags = TaggableManager()
    user = models.ForeignKey(User, on_delete=PROTECT)

    def __str__(self):
        return self.name

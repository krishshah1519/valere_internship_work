import datetime

from django.utils import timezone

from django.db import models


# Create your models here.
class Blog(models.Model):
    blog_text = models.TextField(max_length=1000)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.blog_text

    def was_published_today(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

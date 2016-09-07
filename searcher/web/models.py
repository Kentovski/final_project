# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils import timezone


class SpiderTask(models.Model):
    query = models.CharField(max_length=512)
    is_google_done = models.BooleanField(default=False)
    is_yandex_done = models.BooleanField(default=False)
    is_instagram_done = models.BooleanField(default=False)
    done_time = models.DateTimeField(default=None, null=True)
    
    def save(self, *args, **kwargs):
        if all([self.is_google_done, self.is_instagram_done, self.is_yandex_done]):
            self.done_time = timezone.now()
        super(SpiderTask, self).save(*args, **kwargs)


class Item(models.Model):
    url = models.URLField()
    image_source = models.URLField()
    source = models.CharField(max_length=128)
    number = models.PositiveIntegerField(default=0)

    task = models.ForeignKey('SpiderTask')

# class Statistic(models.Model):
#     query =
#     amount =

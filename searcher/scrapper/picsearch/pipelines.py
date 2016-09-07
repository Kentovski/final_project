# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from web.models import Item, SpiderTask


class DjangoPipeline(object):

    def process_item(self, item, spider):
        task = SpiderTask.objects.get(id=spider.task_id)
        dj_item = Item.objects.create(task=task, **item)
        return dj_item

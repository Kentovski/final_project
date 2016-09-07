# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request


class BaseImageSpider(RedisSpider):
    search_url = None
    task_id = None

    def make_request_from_data(self, data):
        query, task_id = self._parse_query(data)
        self.task_id = task_id
        return Request(self.search_url.format(query=query), dont_filter=True)

    def schedule_next_requests(self):
        return super(BaseImageSpider, self).schedule_next_requests()

    @classmethod
    def _parse_query(cls, data):
        return data.split('::')

from scrapy import signals
from web.models import SpiderTask
from logger import log

SPIDER_MAPPING = {
    'google': 'is_google_done',
    'yandex': 'is_yandex_done',
    'instagram': 'is_instagram_done',
}


class CloseTaskExtension(object):

    @classmethod
    def from_crawler(cls, crawler):
        ext = CloseTaskExtension()
        crawler.signals.connect(ext.spider_idle, signal=signals.spider_idle)
        return ext

    def spider_idle(self, spider):
        if spider.task_id:
            task = SpiderTask.objects.get(id=spider.task_id)
            setattr(task, SPIDER_MAPPING.get(spider.name), True)
            task.save()
            spider.task_id = None


class LogEntriesExtensions(object):

    @classmethod
    def from_crawler(cls, crawler):
        ext = LogEntriesExtensions()
        crawler.signals.connect(ext.engine_started, signal=signals.engine_started)
        crawler.signals.connect(ext.engine_stopped, signal=signals.engine_stopped)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(ext.item_dropped, signal=signals.item_dropped)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_error, signal=signals.spider_error)
        crawler.signals.connect(ext.request_dropped, signal=signals.request_dropped)
        crawler.signals.connect(ext.response_received, signal=signals.response_received)
        return ext

    @staticmethod
    def engine_started():
        log.info('Engine started')

    @staticmethod
    def engine_stopped():
        log.info('Engine stopped')

    @staticmethod
    def item_scraped(item, response, spider):
        log.info('Item=%s scraped, task=%s, response=%s', item.id, spider.task_id, response)

    @staticmethod
    def item_dropped(item, response, exception, spider):
        log.exception(
            'ITEM DROPPED. Item=%s, Response=%s, Exception=%s, Spider=%s', item.id, response, exception, spider.name
        )

    @staticmethod
    def spider_closed(spider, reason):
        log.info('Spider=%s closed. Reason=%s', spider.name, reason)

    @staticmethod
    def spider_opened(spider):
        log.info('Spider=%s opened.', spider.name)

    @staticmethod
    def spider_error(failure, response, spider):
        log.exception('Spider=%s raised error=%s. Response=%s', spider.name, failure, response)

    @staticmethod
    def request_dropped(request, spider):
        log.exception('Request=%s dropped. Spider==%s', request, spider.name)

    @staticmethod
    def response_received(response, request, spider):
        log.info('Response=%s received. Request=%s. Spider=%s', response, request, spider.name)

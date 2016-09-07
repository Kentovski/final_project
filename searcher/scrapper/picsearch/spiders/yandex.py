# -*- coding: utf-8 -*-
import json
from picsearch.base import BaseImageSpider
from picsearch.items import PicsearchItem
from picsearch.config import RESULT_SIZE


class YandexImageSpider(BaseImageSpider):
    name = "yandex"
    allowed_domains = ["yandex.ru"]
    search_url = 'https://yandex.ua/images/search?text={query}'
    redis_key = 'yandex:search'

    def parse(self, response):
        results = response.xpath('//div[contains(@class, "serp-item_type_search")]')[:RESULT_SIZE]
        for index, image_td in enumerate(results):
            data = json.loads(image_td.xpath('@data-bem').extract_first())
            yield PicsearchItem(
                source=self.name,
                number=index,
                url='http://%s' % data['serp-item']['thumb']['url'].split('//')[1],
                image_source=data['serp-item']['preview'][0]['url']
            )

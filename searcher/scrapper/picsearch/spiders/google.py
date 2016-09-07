# -*- coding: utf-8 -*-
from picsearch.base import BaseImageSpider
from picsearch.items import PicsearchItem
from picsearch.config import RESULT_SIZE


class GoogleImageSpider(BaseImageSpider):
    name = "google"
    allowed_domains = ["google.com"]
    search_url = 'https://www.google.com.ua/search?tbm=isch&q={query}'
    redis_key = 'google:search'

    def parse(self, response):
        results = response.xpath('//table[@class="images_table"]//td')[:RESULT_SIZE]
        for index, image_td in enumerate(results):
            yield PicsearchItem(
                source=self.name,
                number=index,
                url=image_td.xpath('a/img/@src').extract_first(),
                image_source=image_td.xpath('a/@href').extract_first().split('q=')[1]
            )

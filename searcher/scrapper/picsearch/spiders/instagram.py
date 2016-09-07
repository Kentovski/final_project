# -*- coding: utf-8 -*-
import json
import re
from picsearch.base import BaseImageSpider
from picsearch.items import PicsearchItem
from picsearch.config import RESULT_SIZE


USE_TOP_POSTS = True


class InstagramImageSpider(BaseImageSpider):
    name = "instagram"
    allowed_domains = ["instagram.com"]
    search_url = 'https://www.instagram.com/explore/tags/{query}/'
    redis_key = 'instagram:search'

    def parse(self, response):
        json_data = self._get_json_data(response)
        results = self._get_results(json_data)
        for index, image in enumerate(self._get_image_results(results)[:RESULT_SIZE]):
            yield PicsearchItem(
                source=self.name,
                number=index,
                url=image['thumbnail_src'],
                image_source=image['display_src']
            )

    @classmethod
    def _parse_query(cls, data):
        query, key = data.split('::')
        query = query.replace(' ', '')
        return query, key

    @staticmethod
    def _get_image_results(results):
        return [result for result in results if not result['is_video']]

    @staticmethod
    def _get_json_data(response):
        """
        Joins JS and parse json data into dict
        """
        javascript = "".join(response.xpath('//script[contains(text(), "sharedData")]/text()').extract())
        return json.loads("".join(re.findall(r'window._sharedData = (.*);', javascript)))

    @staticmethod
    def _get_results(json_data):
        if USE_TOP_POSTS:
            return json_data['entry_data']['TagPage'][0]['tag']['top_posts']['nodes']
        return json_data['entry_data']['TagPage'][0]['tag']['media']['nodes']

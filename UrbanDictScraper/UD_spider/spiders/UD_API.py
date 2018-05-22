# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import UdSpiderItem

import string, requests
from urllib.parse import urljoin

class UdApiSpider(CrawlSpider):
    name = 'UD-API'
    allowed_domains = ['urbandictionary.com']

    start_urls = []
    base_url = 'https://www.urbandictionary.com'
    url_prefix = '/browse.php?character='
    # only consider alphabets as the beginning, excluding * symbol
    for ch in string.ascii_uppercase:
        start_url = urljoin(base_url, url_prefix + ch)
        start_urls.append(start_url)

    rules = (
        # extract pagination
        Rule(LinkExtractor(allow=r'\/browse.php\?character=[\w|\*](\&page=\d+)*'), callback='_parse_token',follow=True),
        # extract UD definition item
        # # filter out phrase (token num >= 2, i.e. contains %20(plus sign))
        # Rule(LinkExtractor(allow=r'\/define.php\?term=\S+', deny='(\%20)+',
        #                    restrict_xpaths='//div[@id="columnist"]//li/a'), callback='parse_item')
    )

    def _parse_token(self, response):
        response

    def _api_fetch(self):
        item = UdSpiderItem()




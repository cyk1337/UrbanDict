# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import UdSpiderItem

import string
from urllib.parse import urljoin
import logging

class UdSpider(CrawlSpider):
    name = 'UD'
    allowed_domains = ['urbandictionary.com']
    start_urls = []
    base_url = 'https://www.urbandictionary.com'
    url_prefix = '/browse.php?character='
    # only consider alphabets as the beginning, excluding * symbol
    for ch in string.ascii_uppercase:
        start_url = urljoin(base_url, url_prefix+ch)
        start_urls.append(start_url)

    rules = (
        # extract pagination
        Rule(LinkExtractor(allow=r'\/browse.php\?character=[\w|\*](\&page=\d+)*'),  follow=True),
        # extract UD definition item
        # # filter out phrase (token num >= 2, i.e. contains %20(plus sign))
        Rule(LinkExtractor(allow=r'\/define.php\?term=\S+', deny='(\%20)+', restrict_xpaths='//div[@id="columnist"]//li/a'), callback='parse_item')
    )

    def parse_item(self, response):
        """
        parse definition web page
        :param response: response from downloader module.
        :return: item
        """
        item = UdSpiderItem()

        # dict to save all the results and zip according to their index order
        results = dict()
        print("Start parsing {}...".format(response.url))
        # main field
        results['defid'] = response.css('div.def-panel::attr(data-defid)').extract()
        results['word'] = response.css('.word::text').extract()
        results['definition'] = response.xpath('//div[@class="meaning"]').xpath('normalize-space(string(.))').extract()

        # others
        results['thumbs_up'] = response.css('.left.thumbs .up span.count::text').extract()
        results['thumbs_down'] = response.css('.left.thumbs .down span.count::text').extract()
        results['author'] = response.css('.contributor a::text').extract()
        results['written_date'] = response.css('.contributor::text').extract()[1::2]
        results['egs'] = response.css('.example').xpath('normalize-space(string(.))').extract()

        # check if the length of lists are the same, all the same or empty
        if len(set(len(x) for x in (results['defid'], results['word'], results['definition']))) <= 1:

            for item['defid'], item['word'], item['definition'] in \
                    zip(results['defid'], results['word'], results['definition']):
                # save url
                # item['url'] = response.url
                yield item


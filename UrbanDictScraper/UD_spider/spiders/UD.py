# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.project import get_project_settings
from ..items import UdSpiderItem
from .._crawl_utils import _filter_word_log

import string, bleach, re
from datetime import datetime
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
       # uncomment this to test 'A'
        # for ch in 'A':
        start_url = urljoin(base_url, url_prefix+ch)
        start_urls.append(start_url)

    # test url
    # start_urls = ['https://www.urbandictionary.com/browse.php?character=U&page=98']

    rules = (
        # 1. extract only next pagination
        Rule(LinkExtractor(allow=r'\/browse.php\?character=[\w|\*](\&page=\d+)*', restrict_xpaths='//ul[@class="pagination"]//a[@rel="next"]'), follow=True),
        # 2. extract UD definition item

        # ----------------------------------
         # the 1st step of filtering out words containing whitespace(s) in href
         # i.e. filter out phrase (token num >= 2, i.e. contains %20(plus sign))
        # -----------------------------------
        Rule(LinkExtractor(
            allow=r'\/define.php\?term=\S+', deny=('(\%20)+', ), restrict_xpaths='//div[@id="columnist" and not(contains(@class,"trending-words-panel"))]//li/a'),
             callback='parse_item', follow=True),

        # if exists pagination, iteratively parse
        Rule(LinkExtractor(allow=r'\/define.php\?term=\w+&page=[0-9]+',
                           restrict_xpaths='//div[@id="content"]/div[@class="pagination-centered"]/ul[@class="pagination"]//a[@rel="next"]'),
             callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        """
        parse definition web page
        :param response: response from downloader module.
        :return: item
        """
        item = UdSpiderItem()

        settings = get_project_settings()

        # -------------------------------------------------------------------
        # dict to save all the results and zip according to their index order
        # -------------------------------------------------------------------
        results = dict()
        print("Start parsing {}...".format(response.url))
        # main field
        results['defid'] = response.css('div.def-panel::attr(data-defid)').extract()
        results['word'] = response.css('.word::text').extract()

        # check whether add HTML tag *a* INFO
        if settings.get('ADD_LINK_INFO'):
            raw_definition = response.xpath('//div[@class="meaning"]').extract()
            defn_list = []
            for defn in raw_definition:
                defn = bleach.clean(defn, tags=['a'], attributes=[], strip=True)
                defn = re.sub('<a>', ' <a> ', defn)
                defn = re.sub('</a>', ' </a> ', defn)
                defn = re.sub( '\s+', ' ', defn).strip()
                defn_list.append(defn)
            results['definition'] = defn_list
        else:
            results['definition'] = response.xpath('//div[@class="meaning"]').xpath('normalize-space(string(.))').extract()

        parse_full_field = settings.get('PARSE_FULL_FIELD')
        if parse_full_field:
            #----------
            # parse full fields
            #----------
            results['thumbs_up'] = response.css('.left.thumbs .up span.count::text').extract()
            results['thumbs_down'] = response.css('.left.thumbs .down span.count::text').extract()
            results['author'] = response.css('.contributor a::text').extract()
            results['written_date'] = response.css('.contributor::text').extract()[1::2]
            results['example'] = response.css('.example').xpath('normalize-space(string(.))').extract()

            # check if the length of lists are the same, all the same or empty
            if len(set(len(x) for x in (results['defid'], results['word'], results['definition']))) == 1:

                for defid, word, definition, thumbs_up, thumbs_down, author, written_date_raw, example in \
                        zip(results['defid'], results['word'], results['definition'],
                            results['thumbs_up'],results['thumbs_down'], results['author'],
                            results['written_date'], results['example']):

                    # the 2nd step of filtering out words containing whitespace(s) in word list
                    if ' ' in word.strip():
                        _filter_word_log("word:{}, defid:{}\n".format(word, defid))
                        continue

                    item['defid'] = defid
                    item['word'] = word
                    item['definition'] = definition
                    item['thumbs_up'] = thumbs_up
                    item['thumbs_down'] = thumbs_down
                    item['author'] = author
                    item['example'] = example

                    datetime_obj = datetime.strptime(written_date_raw.strip(),'%B %d, %Y')
                    written_date = datetime_obj.strftime("%Y-%m-%d")
                    item['written_date'] = written_date

                    # save url
                    # item['url'] = response.url
                    yield item
        else:
            # parse only three fields: defid, definition, word
            # --------------------------
            # check if the length of lists are the same, all the same or empty
            if len(set(len(x) for x in (results['defid'], results['word'], results['definition']))) == 1:

                for  defid, word, definition in \
                        zip(results['defid'], results['word'], results['definition']):

                    # the 2nd step of filtering out words containing whitespace(s) in word list
                    if ' ' in word.strip():
                        _filter_word_log("word:{}, defid:{}\n".format(word, defid))
                        continue
                    # TODO
                    # filter out common names
                    # ---------

                    item['defid'], item['word'], item['definition'] = defid, word, definition
                    # save url
                    # item['url'] = response.url

                    yield item


# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import UdSpiderItem

import string, requests, re, logging
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
        # extract next pagination
        Rule(LinkExtractor(allow=r'\/browse.php\?character=[\w|\*](\&page=\d+)*', restrict_xpaths='//ul[@class="pagination"]//a[@rel="next"]'), callback='_parse_word',follow=True),
    )

    def _parse_word(self, response):
        # ----------------------------------------------------------------------
        #  the 1st step of filtering out words containing whitespace(s) in href
        #  i.e. filter out phrases (token num >= 2, i.e. contains %20(plus sign))
        # ----------------------------------------------------------------------
        href_list = response.xpath('//div[@id="columnist"]//li/a[not(contains(@href,"%20"))]/@href').extract()
        pattern =  '\/define.php\?term=(\S+)'
        word_list = list(map(lambda href: re.match(pattern, href).group(1), href_list))

        item = UdSpiderItem()

        # -------------------------------------
        # fetch json data from Urban Dict API
        # -------------------------------------
        def _api_fetch(word):
            url_api = 'http://api.urbandictionary.com/v0/define?term=%s' % word
            r = requests.get(url_api)
            data = r.json()
            # -----------------------------
            # check if successfully connect
            # -----------------------------
            if r.status_code == 200 and data['result_type'] == 'exact':
                for meaning in data.get('list'):
                    item['defid'] = meaning['defid']
                    # -----------------------
                    # main fields
                    # -----------------------
                    item['word'] = meaning['word']
                    item['definition'] = meaning['definition']

                    # -----------------------
                    # other fields
                    ##-----------------------
                    # item['url'] = url_api
                    # item['permalink'] = meaning['permalink']
                    # item['thumbs_up'] = meaning['thumbs_up']
                    # item['thumbs_down'] = meaning['thumbs_down']
                    # item['author'] = meaning['author']
                    # item['written_date'] = meaning['written_on']
                    # item['egs'] = meaning['example']
                    ##-----------------------
                    print('Item:{}'.format(item))
                    print('Finish parsing', '-' * 10)
                    return item
            else:
                # TODO
                # code 429 -> Too many requests!
                # --------------------------------
                print('Fail to parse %s :(' % word)
                logging.warning('Status code: {}'.format(r.status_code))

        for word in word_list:
            # the 2nd step of filtering out words containing whitespace(s) in word list
            if ' ' in word.strip():
                continue

            print('Start parsing %s ...' % word)
            yield_item = _api_fetch(word)
            if isinstance(yield_item, UdSpiderItem):
                yield yield_item
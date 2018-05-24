# -*- coding: utf-8 -*-

# Define here the models for scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UdSpiderItem(scrapy.Item):
    """
    fields to scrape,
        1. defid: definition id,
        ------------------------
        2. word: dict entry,
        3. definition: word meaning,
        ------------------------
        4. url: current web page URL,
        5. thumbs_up: thumbs-up counts,
        6. thumbs_down: thumbs-down counts,
        7. permalink: link got from API (only parsed when using UD API to scrape),
        8. author: definition editor,
        9. written_date: definition editing date.
    """
    # main fields
    defid = scrapy.Field()
    word = scrapy.Field()
    definition = scrapy.Field()

    # fields for analysis
    thumbs_up = scrapy.Field()
    thumbs_down = scrapy.Field()
    permalink = scrapy.Field()
    url = scrapy.Field()  # 'https://www.urbandictionary.com/define.php?term=%s' % word
    author = scrapy.Field()
    written_date = scrapy.Field()
    example = scrapy.Field()
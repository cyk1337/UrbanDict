# -*- coding: utf-8 -*-

# item pipelines
#
# Don't forget to add pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql, logging, os, datetime
from twisted.enterprise import adbapi
from scrapy.exporters import CsvItemExporter
from scrapy.utils.project import get_project_settings

from ._crawl_utils import _time_log

from scrapy.statscollectors import StatsCollector, DummyStatsCollector

class SyncMySQLPipeline(object):
    def __init__(self, stats):
        self.start_time = None
        self.stats = stats

        self.conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            passwd='admin',
            db='UrbanDict',
            # charset='utf8',
        )
        if self.conn:
            logging.info("MySQL connect correctly!")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)

    def process_item(self, item, spider):

        try:
            with self.conn.cursor() as cur:
                settings = get_project_settings()
                parse_full_field = settings.get('PARSE_FULL_FIELD')
                if parse_full_field:
                    insert_sql = 'INSERT INTO UD_full(defid, word, definition, ' \
                                 'thumbs_up, thumbs_down, author, written_date, example)' \
                                 ' VALUES(%s, %s, %s, %s, %s, %s, %s, %s);'
                    params = (item['defid'], item['word'], item['definition'],
                              item['thumbs_up'],item['thumbs_down'], item['author'],
                              item['written_date'], item['example'])
                else:
                    insert_sql = 'INSERT INTO UrbanDict(defid, word, definition) VALUES(%s, %s, %s);'
                    params = (item['defid'], item['word'], item['definition'])
                cur.execute(insert_sql, params)
            self.conn.commit()
        except Exception as e:
            print("Mysql Insert Error:\t {}:{}, word:{}, defid:{}".format(e.args[0], e.args[1], item['word'], item['defid']))
            # self.conn.rollback()
        return item

    def open_spider(self, spider):
        self.start_time = datetime.datetime.now()

    def close_spider(self, spider):
        # compute running time
        finish_time = datetime.datetime.now()
        print(self.__class__.__name__, self.start_time, finish_time)
        settings = get_project_settings()
        parse_full_field = settings.get('PARSE_FULL_FIELD')
        _time_log(parse_full_field, spider.name, self.__class__.__name__, self.start_time, finish_time)

        # 2. status collector
        # TODO: cann't get finish time in
        # start_time = self.stats.get_value('start_time')
        # finish_time = datetime.datetime.now()
        # print(self.__class__.__name__, start_time, finish_time)
        # _time_log(self.__class__.__name__, start_time, finish_time)

    def spider_closed(self, spider):
        self.conn.close()




class CsvExporterPipeline(object):
    def __init__(self):
        # export to the path -> ./csv_dir/csv_file
        csv_file = 'UD_CSV_export.csv'
        csv_dir = 'CSV_exporter'
        if not os.path.exists(csv_dir):
            os.mkdir(csv_dir)
        csv_file = os.path.join(csv_dir, csv_file)

        self.file = open(csv_file, 'w+b')
        self.fields_to_export = ['defid', 'word', 'definition']
        self.exporter = CsvItemExporter(self.file, fields_to_export=self.fields_to_export, encoding='utf8')
        self.exporter.start_exporting()


    def close_spider(self):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


# TODO Bug: sometimes lose some item to be written!
class AsyncMySQLPipeline(object):
    """
    asynchronous MySQL pipeline using twisted,
    """
    def __init__(self, dbpool):
        self.dbpool = dbpool
        self.starttime = None

    @classmethod
    def from_settings(cls, settings):
        db_params = dict(
            host = settings["MYSQL_HOST"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWD"],
            db = settings["MYSQL_DBNAME"],
            charset = settings["MYSQL_CHARSET"],
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode = True,
        )
        dbpool = adbapi.ConnectionPool("pymysql", **db_params)
        return cls(dbpool)

    def process_item(self, item, spider):
        """
        asynchronous insertion using twisted connection pool
        """
        query = self.dbpool.runInteraction(self._add_record, item)
        # handle error
        query.addErrback(self.handle_error)
        return item

    def handle_error(self, failure):
        """
        asynchronous error
        """
        logging.ERROR(failure)

    def _add_record(self, cursor, item):
        try:
            insert_sql = 'INSERT INTO UrbanDict(defid, word, definition) VALUES(%s, %s, %s);'
            params = (item['defid'], item['word'], item['definition'])
            cursor.execute(insert_sql, params)
        except Exception as e:
            err = "Mysql Insert Error: "+ str(e.args[0])+", "+ str(e.args[1])
            print(err)
            print('Failed to insert records\n','-'*30)

            # write insert error to log file
            # err = err + ', defid:{}, word:{}\n'.format(item['defid'], item['word'])
            # _err_log(err)

            # self.conn.rollback()

    def open_spider(self, spider):
        self.start_time = datetime.datetime.now()

    def close_spider(self, spider):
        """
        Close ConnectionPool after crawling.
         """
        self.dbpool.close()
        # compute running time
        finish_time = datetime.datetime.now()
        print(self.__class__.__name__, self.start_time, finish_time)
        _time_log(spider.name, self.__class__.__name__, self.start_time, finish_time)

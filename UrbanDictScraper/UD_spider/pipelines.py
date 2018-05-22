# -*- coding: utf-8 -*-

# item pipelines
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql, logging, os
from twisted.enterprise import adbapi
from scrapy.exporters import CsvItemExporter

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


class AsyncMySQLPipeline(object):
    """
    asynchronous MySQL pipeline using twisted
    """
    def __init__(self, dbpool):
        self.dbpool = dbpool

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
            if item.get('url') is None:
                insert_sql = 'INSERT INTO UrbanDict(defid, word, definition) VALUES(%s, %s, %s);'
                params = (item['defid'], item['word'], item['definition'])
            else:
                insert_sql = 'INSERT INTO UrbanDict(defid, word, definition, url) VALUES(%s, %s, %s, %s);'
                params = (item['defid'], item['word'], item['definition'], item['url'])
            cursor.execute(insert_sql, params)
        except Exception as e:
            print("Mysql Insert Error:"+ str(e.args[0])+ str(e.args[1]))
            print('Failed to insert records\n','-'*30)
            # self.conn.rollback()

    def spider_closed(self, spider):
        """
        Close ConnectionPool after crawling.
         """
        self.dbpool.close()


class SyncMySQLPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            passwd='admin',
            db='UrbanDict',
            # charset='utf8',
        )
        if self.conn:
            logging.info("MySQL connect correctly!")

    def process_item(self, item, spider):

        try:
            with self.conn.cursor() as cur:
                insert_sql = 'INSERT INTO UrbanDict(defid, word, definition, url) VALUES(%s, %s, %s, %s);'
                cur.execute(insert_sql, (item['defid'], item['word'], item['definition'], item['url']))
            self.conn.commit()
        except Exception as e:
            logging.ERROR("Mysql Insert Error:\t {}:{}".format(e.args[0], e.args[1]))
            # self.conn.rollback()
        return item

    def spider_closed(self, spider):
        self.conn.close()
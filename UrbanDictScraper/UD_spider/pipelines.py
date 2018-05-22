# -*- coding: utf-8 -*-

# item pipelines
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql, logging
from twisted.enterprise import adbapi

class UdSpiderPipeline(object):
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
            logging.ERROR("Mysql Insert Error:" + str(e.args[0]) + str(e.args[1]))
            # self.conn.rollback()
        return item

    def spider_closed(self, spider):
        self.conn.close()



class AsyncMySQLPipeline(object):
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

    def handle_error(self, e):
        """
        asynchronous error
        """
        logging.ERROR(e.args[1])

    def _add_record(self, cursor, item):
        try:
            insert_sql = 'INSERT INTO UrbanDict(defid, word, definition, url) VALUES(%s, %s, %s, %s);'
            cursor.execute(insert_sql, (item['defid'], item['word'], item['definition'], item['url']))
        except Exception as e:
            logging.ERROR("Mysql Insert Error:"+ str(e.args[0])+ str(e.args[1]))
            # self.conn.rollback()

    def spider_closed(self, spider):
        """
        Close ConnectionPool after crawling.
         """
        self.dbpool.close()
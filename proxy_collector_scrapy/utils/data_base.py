import configparser

import pymysql
from itemadapter import ItemAdapter


# noinspection SqlNoDataSourceInspection,SqlResolve
class Database:
    _connection = None
    _cursor = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def _get_conn(self):
        config = configparser.ConfigParser()
        config.read('config/app.cfg')
        if 'db_conn' not in config:
            print('db config error')  # TODO correct handling
            exit(1)
        props = dict(config.items('db_conn'))
        return pymysql.connect(cursorclass=pymysql.cursors.DictCursor, **props)

    def connect(self):
        if self._connection is None:
            self._connection = self._get_conn()
            self._cursor = self._connection.cursor()
            print('connected')

    def disconnect(self):
        if self._connection is not None:
            self._connection.commit()
            self._connection.close()
            print('disconnected')

    def truncate_proxy(self, table_name):
        sql = "TRUNCATE TABLE proxy.{}".format(table_name)
        self._cursor.execute(sql)
        self._connection.commit()
        print('command truncate')

    @staticmethod
    def __clean_dict(item_dict):
        dict((k, ','.join(v)) for k, v in item_dict.items() if isinstance(v, (list, set)))
        return dict((k, v) for k, v in item_dict.items() if v)

    def save_proxy(self, items, table_name):
        for item in items:
            sql = """INSERT INTO proxy.{} VALUES (%s, %s, %s, %s)""".format(table_name)
            self._cursor.execute(sql, (item['host'], item['port'], item['type'], item['ping']))
        self._connection.commit()

    def save_unchecked(self, items):
        print()
        self.save_proxy(items, 'proxy_unchecked')

    def save_checked(self, items):
        self.save_proxy(items, 'proxy_checked')

    def truncate_unchecked(self):
        self.truncate_proxy('proxy_unchecked')

    def truncate_checked(self):
        self.truncate_proxy('proxy_checked')

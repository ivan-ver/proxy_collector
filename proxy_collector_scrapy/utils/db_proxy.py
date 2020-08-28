import configparser
import pymysql
from pymysql.cursors import DictCursor

# noinspection SqlNoDataSourceInspection,SqlResolve
class DB_proxy():
    _connection = None
    _cursor = None

    def __init__(self):
        self.connect()

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

    def get_all_proxy(self):
        self._cursor.execute("""
            SELECT host, port FROM `proxy`.`proxy` order by ping
        """)
        return ['http://' + i['host'] + ':' + str(i['port']) for i in self._cursor.fetchall()]










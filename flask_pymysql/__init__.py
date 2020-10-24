import flask
from flask import (
    _app_ctx_stack,
)


class MySQL(object):

    def __init__(self, app=None):
        self.app = app
        self.config = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app, prefix='MYSQL_'):
        # type: (flask.Flask, str) -> None
        """
        Initialize this class to use the app.

        :param flask.Flask app: Application to initialize
        :param str prefix: config prefix
        """
        config = self.config = app.config.get_namespace(prefix)

        config.setdefault('host', 'localhost')
        config.setdefault('user', None)
        config.setdefault('password', None)
        config.setdefault('db', None)
        config.setdefault('port', 3306)
        config.setdefault('unix_socket', None)
        config.setdefault('connect_timeout', 10)
        config.setdefault('read_default_file', None)
        config.setdefault('use_unicode', True)
        config.setdefault('charset', 'utf8')
        config.setdefault('sql_mode', None)
        config.setdefault('cursorclass', 'Cursor')
        config.setdefault('driver', 'pymysql')

        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)

    def connect_pymysql(self):
        import pymysql

        return pymysql.connect(
            host=self.config['host'],
            port=self.config['port'],
            database=self.config['db'],
            user=self.config['user'],
            password=self.config['password'],
            unix_socket=self.config['unix_socket'],
            connect_timeout=self.config['connect_timeout'],
            read_default_file=self.config['read_default_file'],
            use_unicode=self.config['use_unicode'],
            charset=self.config['charset'],
            sql_mode=self.config['sql_mode'],
            cursorclass=getattr(pymysql.cursors, self.config['cursorclass']),
        )

    def connect_cymysql(self):
        import cymysql

        return cymysql.connect(
            host=self.config['host'],
            port=self.config['port'],
            database=self.config['db'],
            user=self.config['user'],
            passwd=self.config['password'],
            unix_socket=self.config['unix_socket'],
            connect_timeout=self.config['connect_timeout'],
            read_default_file=self.config['read_default_file'],
            use_unicode=self.config['use_unicode'],
            charset=self.config['charset'],
            sql_mode=self.config['sql_mode'],
            cursorclass=getattr(cymysql.cursors, self.config['cursorclass']),
        )

    @property
    def connect(self):
        return getattr(self, 'connect_' + self.config['driver'])()

    @property
    def connection(self):
        """Attempts to connect to the MySQL server.

        :return: Bound MySQL connection object if successful or ``None`` if
            unsuccessful.
        """

        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'mysql_db'):
                ctx.mysql_db = self.connect
            return ctx.mysql_db

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'mysql_db'):
            ctx.mysql_db.close()

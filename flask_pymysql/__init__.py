# coding=utf-8
import flask
from flask import (
    _app_ctx_stack,
)
from typing import (
    Union,
)


class MySQL(object):

    def __init__(self, app=None, prefix=None):
        self.app = app
        self.config = None
        self.attribute = 'mysql_db'
        self.prefix = prefix or 'MYSQL_'
        if app is not None:
            self.init_app(app)

    def init_app(self, app, prefix=None):
        # type: (Union[flask.Flask, flask.Blueprint], str) -> None
        """
        Initialize this class to use the app.

        :param flask.Flask app: Application to initialize
        :param str prefix: config prefix
        """
        self.prefix = prefix or self.prefix
        if isinstance(app, flask.Blueprint):
            self.attribute = '{}_{}'.format(self.attribute, app.name)
            app.record_once(self._record_once)
        elif isinstance(app, flask.Flask):
            self._configure(app)
        else:
            raise TypeError(
                '`app` should be either flask.Flask or flask.Blueprint, '
                'got {} instead'.format(type(app))
            )

    def _record_once(self, state):
        # type: (flask.blueprints.BlueprintSetupState) -> None
        self._configure(state.app)

    def _configure(self, app):
        # type: (flask.Flask) -> None
        config = self.config = app.config.get_namespace(self.prefix)

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
            db=self.config['db'],
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
            if not hasattr(ctx, self.attribute):
                setattr(ctx, self.attribute, self.connect)
            return getattr(ctx, self.attribute)

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, self.attribute):
            getattr(ctx, self.attribute).close()

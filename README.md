Flask-pymysql
================

Flask-pymysql provides MySQL connection for Flask.

Quickstart
----------

First, install Flask-pymysql:
    
    $ pip install flask-mysqldb
    
Flask-pymysql depends, and will install for you, recent versions of Flask
(0.10.1 or later) and [mysqlclient](https://github.com/PyMySQL/mysqlclient-python). Flask-pymysql is compatible
with and tested on Python 2.7, 3.4, 3.5 and 3.6.

Next, add a ``MySQL`` instance to your code:

```python
from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'database'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def users():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT user, host FROM mysql.user''')
    rv = cur.fetchall()
    return str(rv)

if __name__ == '__main__':
    app.run(debug=True)
```

Other configuration directives can be found [here](http://flask-mysqldb.readthedocs.io/en/latest/#configuration).

Why
---
Why would you want to use this extension versus just using pymysql by itself? The only reason is that the extension was made using Flask's best pratices in relation to resources that need caching on the [app context](http://flask.pocoo.org/docs/0.12/appcontext/#context-usage). What that means is that the extension will manage creating and teardown the connection to MySQL for you while with if you were just using pymysql you would have to do it yourself.


Resources
---------

- [Documentation](http://flask-mysqldb.readthedocs.org/en/latest/)
- [PyPI](https://pypi.python.org/pypi/Flask-pymysql)

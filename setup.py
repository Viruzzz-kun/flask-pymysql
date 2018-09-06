"""
Flask-pymysql
----------------

pymysql extension for Flask
"""
from setuptools import setup


setup(
    name='Flask-pymysql',
    version='0.2.0',
    url='https://github.com/Viruzzz-kun/flask-pymysql',
    license='MIT',
    author='Mikhsql Malkov, Alexandre Ferland',
    author_email='viruzzz-kun@gmail.com',
    description='pymysql extension for Flask',
    long_description=__doc__,
    packages=['flask_pymysql'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.10.1',
        'pymysql'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

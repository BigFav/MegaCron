#!/usr/bin/python2

from setuptools import setup, find_packages

setup(
    name='Megacron',
    version='0.1',
    description='Distributed Cron Replacement',
    author='John Tanner, Favian Contreras, Ben Zeghers',
    author_email='megacronteam@gmail.com',
<<<<<<< HEAD
    packages=['API','edit','scheduler','status','worker'],
    url='https://pypi.python.org/pypi/Megacron',
=======
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'megacrond = megacron.daemon.main:main',
            'megacrontab = megacron.edit:main',
            'megacron-status = megacron.status:main'
        ]
    },
    install_requires=['croniter'],
    package_data={
        'megacron': ['conf/megacron.conf']
    },
    data_files=[
        ('/etc', ['megacron/conf/megacron.conf'])
    ],
    url='https://www.mediawiki.org/wiki/Facebook_Open_Academy/Cron',
>>>>>>> 7af99e2aa20a339c941e45c90628c902839ebe26
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.rst').read()
)

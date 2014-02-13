#!/usr/bin/python

from distutils.core import setup

setup(
    name='Megacron',
    version='0.1',
    description='Distributed Cron Replacement',
    author='John Tanner',
    author_email='jctanner@interchange.ubc.ca',
    packages=['API','edit','scheduler','status','worker'],
    url='https://www.mediawiki.org/wiki/Facebook_Open_Academy/Cron',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
)

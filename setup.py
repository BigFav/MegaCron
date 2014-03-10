#!/usr/bin/python

from setuptools import setup, find_packages

setup(
    name='Megacron',
    version='0.1',
    description='Distributed Cron Replacement',
    author='John Tanner, Favian Contreras, Ben Zeghers',
    author_email='megacronteam@gmail.com',
    packages=find_packages(),
    url='https://www.mediawiki.org/wiki/Facebook_Open_Academy/Cron',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read()
)

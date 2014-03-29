#!/usr/bin/python2

from setuptools import setup, find_packages

setup(
    name='Megacron',
    version='0.4',
    description='Distributed Cron Replacement',
    author='John Tanner, Favian Contreras, Ben Zeghers',
    author_email='megacronteam@gmail.com',
    packages=find_packages(),
    include_package_data=True,
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
    # Tests
    #
    # Tests must be wrapped in a unittest test suite by either a
    # function, a TestCase class or method, or a module or package
    # containing TestCase classes. If the named suite is a package,
    # any submodules and subpackages are recursively added to the
    # overall test suite.
    test_suite = 'tests.unit_tests',

    setup_requires = [ "setuptools_git >= 0.3"],
    url='https://www.mediawiki.org/wiki/Facebook_Open_Academy/Cron',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.rst').read()
)

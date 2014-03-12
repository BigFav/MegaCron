Megacron
========

Introduction
------------

Wikimedia Distributed Cron

Installation
------------

To install just run:

::

    sudo pip install megacron

or clone this repo and run:

::

    sudo ./setup.py install

Usage
-----

Set the location of the database file to a shared filesystem in
``/etc/megacron.conf`` then run:

::

    sudo megacrond&
    sudo megacrontab

Commands
--------

megacrontab - Gets any existing crontab entries and allows the user to 
add, modify or remove tasks using a standard text editor.

megacrond - Daemon that runs in the background and executes the jobs.
This must run as root.

megacron-status - Prints out details about the current status.

Development
-----------

Clone this repo and run:

::

    sudo ./setup.py develop

To uninstall:

::

    sudo ./setup.py develop --uninstall
    sudo rm /etc/megacron.conf /usr/bin/megacron*

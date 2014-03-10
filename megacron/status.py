import sys

from megacron import api


def get_worker_status():
    L = len(api.get_workers())
    if L == 1:
        print "1 worker is up"
    else:
        print "%d workers are up" % L


def main():
    get_worker_status()

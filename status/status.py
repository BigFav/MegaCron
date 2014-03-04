#!/usr/bin/python2

import sys

sys.path.append("../api")
import api


def get_worker_status():
    L = len(api.get_workers())
    if L == 1:
        print "1 worker is up"
    else:
        print "%d workers are up" % L


if __name__ == '__main__':
    get_worker_status()

#!/usr/bin/python

import sys
sys.path.append("../API")

import API

def getWorkerStatus():
    L = len(API.getWorkers())
    if (L == 1):
        print "1 worker is up"
    else:
        print "%d workers are up" % L

if __name__ == '__main__':
    getWorkerStatus()


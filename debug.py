#!/usr/bin/python
#coding:utf-8

__author__ = "Linwei Li"

from query import genCandidate as gc
from pylab import *

sf = array([0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1,
       1, 0, 1, 1, 1, 1, 1, 1, 0])
ed = arange(32)
a = gc(sf, ed)

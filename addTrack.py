#!/usr/bin/python
#coding:utf-8

__author__ = "Linwei Li"

from pylab import *
from collections import defaultdict
import time

from SAF import SAFP

dataBase = {}
dataBase['trackNum'] = 0
dataBase['isAdded'] = defaultdict(bool)
dataBase['id-filename'] = {}
dataBase['id-fingerprint'] = []
dataBase['subfingerprint-id'] = defaultdict(list)
assist = array([2**i for i in range(32)])

def addTrack(filename, version=2):
    if dataBase['isAdded'][filename] == True:
        print("%s already exists!" % filename)
        return
    try:
        print("extracting fingerprint of %s..." % filename)
        fingerprint = SAFP.extractFingerprint(filename, version)
    except Exception as e:
        print("faild to extract fingerprint of %s : %s" % (filename, e))
        return
    timeStart = time.time()
    num = dataBase['trackNum']
    dataBaseRef = dataBase['subfingerprint-id']
    fingerDec = fingerprint.dot(assist)
    for i, value in enumerate(fingerDec):
        if value>0:
            dataBaseRef[value].append((num,i))
    dataBase['id-filename'][num] = filename
    dataBase['id-fingerprint'].append(None)
    dataBase['id-fingerprint'][num] = fingerprint
    dataBase['isAdded'][filename] = True
    dataBase['trackNum'] += 1
    timeUsed = time.time() - timeStart
    print("added track %s to database, using %.2f seconds" % (filename, timeUsed))
    #try:
        #timeStart = time.time()
        #num = dataBase['trackNum']
        #dataBaseRef = dataBase['subfingerprint-id']
        #fingerDec = fingerprint.dot(assist)
        #for i, value in enumerate(fingerDec):
            #dataBaseRef[value].append((num,i))
        #dataBase['id-filename'][num] = filename
        #dataBase['id-fingerprint'][num] = fingerprint
        #dataBase['isAdded'][filename] = True
        #dataBase['trackNum'] += 1
        #timeUsed = time.time() - timeStart
        #print("added track %s to database, using %.2f seconds" % (filename, timeUsed))
    #except Exception as e:
        #print("faild to add track %s to database : %s" % (filename, e))

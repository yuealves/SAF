#!/usr/bin/python
#coding:utf-8

__author__ = "Linwei Li"

from pylab import *
from addTrack import assist, dataBase as db
from SAF import bits

bitsUnreliable = 3
candidatesNum = 2 ** bitsUnreliable
fp2ID = db['subfingerprint-id']

def findExactOneSubFP(subFingerprint):
    subFingerprintDec = subFingerprint.dot(assist)
    return fp2ID[subFingerprintDec]

def genCandidate(subFingerprint, energyDifference):
    result = ones((candidatesNum, bits)) * subFingerprint
    unreliablePos = abs(energyDifference).argsort()[:bitsUnreliable]
    i = 1
    while i < candidatesNum:
        for j in range(bitsUnreliable):
            for k in range(j, bitsUnreliable):
                h = j
                while h <= k:
                    result[i][unreliablePos[h]] = not result[i][unreliablePos[h]]
                    i += 1
                    h += 1
    return result

def findFingerprintBlock(fingerprintBlock, energyDifference):
    return


#!/usr/bin/python
#coding:utf-8
__author__ = "Linwei Li"

import time
from pylab import *
from scipy.io import wavfile

# define constant variables here
# subframeLength = 0.0116
n = 64
overlapping = 32
freqMin = 300
freqMax = 2000
bits = 32
logSteps1 = 1 + 32
logSteps2 = 1 + 512
fsWorkWith = 5000 # must larger than 2 * 2000

N = n * overlapping
r1 = log(freqMax/freqMin)/logSteps1
freqBands1 = freqMin * e ** (r1 * arange(logSteps1+1))
r2 = log(freqMax/freqMin)/logSteps2
freqBands2 = freqMin * e ** (r2 * arange(logSteps2+1))
assist = {}
assist[1] = None
assist[2] = None

def changeSpace(origin, newBands):
    """origin[0] < newBands[0], origin[-1] > newBands[-1]"""
    # 即使是处理一万首歌，这个函数也只会执行一次，所以不用刻意在意此处效率
    bandElemList = zeros((len(newBands)-1, 4))
    for i in range(len(newBands)-1):
        bandElemList[i][3] = newBands[i+1]-newBands[i]
    def findPos(value):
        for i in range(len(origin)):
            if value >= origin[i] and value < origin[i+1]:
                return i
    i, j, iMax = 0, findPos(newBands[0]), len(bandElemList)
    for i in range(len(bandElemList)):
        bandElemList[i][0] = findPos(newBands[i])
        bandElemList[i][1] = findPos(newBands[i+1])
        bandElemList[i][2] = bandElemList[i][1] - bandElemList[i][0] + 1
    assist[1] = zeros((len(origin), iMax))
    assist[2] = bandElemList[:,3] / bandElemList[:,2]
    for i in range(iMax):
        assist[1][bandElemList[i][0]:bandElemList[i][1],i] = 1

class SAFP(object):
    fs = None
    version = None
    getLogSpectrum = None
    downSampleFunc = None
    freqBand = None
    M, K = 64, 96
    downSampleFactor = (logSteps2 - M)/(bits+1)
    
    def refreshBandsElemList(fs, version):
        if fs == SAFP.fs and version == SAFP.version:
            return
        SAFP.fs = fs
        SAFP.version = version
        freqList = fs * arange(N) / N
        if version == 2:
            freqBands = freqBands2
        else:
            freqBands = freqBands1
        changeSpace(freqList, freqBands)

    def getOneEntry(subframeData, version):
        freqIntensityList = abs(fft(subframeData))
        logSpectrum = freqIntensityList.dot(assist[1]) * assist[2]
        M, K, dsf = SAFP.M, SAFP.K, SAFP.downSampleFactor
        if version == 2:
            tmp = zeros(bits + 1)
            tmp2 = logSpectrum[K:K+M]
            for i in range(bits + 1):
                tmp[i] = logSpectrum[int(i*dsf):int(i*dsf)+M].dot(tmp2)
            return tmp
        else:
            return logSpectrum
    
    def extractFingerprint(filename, version=1):
        timeStart = time.time()
        try:
            print(filename)
            fs, wavData = wavfile.read(filename)
            # cause we only care the energybands between 300~2000Hz,
            # downsample the signal data to 5000Hz
            downFactor = fs / fsWorkWith
            newLength = int(len(wavData) / downFactor)
            wavData = [wavData[int(i*downFactor)] for i in range(newLength)]
            print(len(wavData))
        except:
            print("can't open file %s !!!" % filename)
            return
        if len(wavData) <= N:
            raise ValueError("wavData is too small!")
        SAFP.refreshBandsElemList(fsWorkWith, version)
        tempSpectrum = empty((int((len(wavData)-N)/n),bits+1))
        fingerprint = empty((int((len(wavData)-N)/n)-1,bits),dtype=bool_)
        for i in range(len(tempSpectrum)):
            tempSpectrum[i] = SAFP.getOneEntry(wavData[i*n:i*n+N], version)
        for i in range(len(tempSpectrum)-1):
            for m in range(bits):
                fingerprint[i][m] = ((tempSpectrum[i+1][m] - tempSpectrum[i+1][m+1]) > (tempSpectrum[i][m] - tempSpectrum[i][m+1]))
        timeUsed = time.time() - timeStart
        print("%s extracted in %.2f seconds! fingerprint size: %s bytes" % (filename, timeUsed, fingerprint.nbytes))
        return fingerprint

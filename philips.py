#!/usr/bin/python
#coding:utf-8
__author__ = "Linwei Li"

#from extractFingerprint import *
from SAF import SAFP
from scipy.io import wavfile

#tmp = extractFingerprint("sunday.wav")
#print(type(tmp))
#fs, temp = wavfile.read("sunday.wav")
#print(len(temp))


#fs, noise = wavfile.read("noise.wav")
#print(len(noise))
#print(type(noise))
#print(fs)
#print(noise.dtype)


origin = SAFP.extractFingerprint("1.wav",2)
print(len(origin))
print(origin)
 

origin = SAFP.extractFingerprint("1.wav",2)
print(len(origin))
print(origin)
origin = SAFP.extractFingerprint("1.wav",2)
print(len(origin))
print(origin)
origin = SAFP.extractFingerprint("1.wav",2)
print(len(origin))
print(origin)
#origin = extractFingerprint("origin.wav")
#print(len(origin))
#print(origin)
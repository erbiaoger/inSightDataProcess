#!/usr/bin/env python
# coding: utf-8

# Massive downloader of InSight data from IRIS
# Contributors: Foivos Karakostas, Doyeon Kim, Ross Maguire, Aisha Khatib and the UMD InSight group
import os
import requests
import numpy as np
from obspy import UTCDateTime
from obspy.clients.fdsn import Client
import obspy
from obspy import read
from obspy import read_inventory
from shutil import copyfile
from .eventDownloader import eventDownloader  

def download(path_Catalog, quality2find, class2find, save_path):

    #quality2find = input('Select quality: ')
    #class2find = input('Select class: ')
    data = np.loadtxt(path_Catalog,dtype=str,usecols=(0,1,3,4)).T
    eventtime = data[1]
    event = data[0]
    eventclass = data[3]
    quality = data[2]


    for i in range(0,len(event)):
        class_s = str(eventclass[i])
        if class_s == class2find:
            quality_s = str(quality[i])
            if quality_s == quality2find:
                event2find = str(event[i])
                eventDownloader(path_Catalog, event2find, save_path)



def downloadAll(path_Catalog, event_qualitys, event_classs, save_path):
    for event_quality in event_qualitys:
        for event_class in event_classs:
            download(path_Catalog, event_quality, event_class, save_path)
        



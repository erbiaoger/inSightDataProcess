
import os
import numpy as np
import obspy
from obspy import read
from obspy import read_inventory
from obspy import UTCDateTime
from obspy.signal.rotate import rotate2zne
from obspy.clients.fdsn import Client
from scipy import signal
from shutil import copyfile

#event2find = input('Enter event: ')
def eventDownloader(path_Catalog, event2find, save_path):
    print('Running code for: Event ' + event2find);

    #fname = 'SeismicCatalog'
    data = np.loadtxt(path_Catalog, dtype=str, usecols=(0,1,3,4)).T
    eventtime = data[1]
    event = data[0]
    eventclass = data[3]
    quality = data[2]
    for i in range(0,len(event)):
        event1 = str(event[i])
        if event1 == event2find:
            a=i
    time_1 = str(eventtime[a])
    t1l=len(time_1)-3
    time_2 = time_1
    class_1 = str(eventclass[a])
    c1l = len(class_1)-3
    class_2 = class_1
    quality_1 = str(quality[a])
    q1l = len(quality_1)-3
    quality_2 = quality_1
    print ('Event: ' + event2find)
    print ('Datetime of the event: ' + time_2)
    print ('Class: ' + class_2)
    print ('Quality: ' + quality_2)

    time = UTCDateTime(time_2)
    starttime = time - 60*30
    print(starttime)
    endtime = time + 60*90
    print(endtime)
    net = 'XB'
    sta = 'ELYSE'
    loc = '02'
    chan = 'BH*'

    client = Client('IRIS')
    st = client.get_waveforms(net, sta, loc, chan, starttime, endtime, attach_response = True)
    print(st)
    for tr in st.select(component='U'):
        st.merge(tr)
    print ('----------------------')
    print('Streams after merging')
    print ('----------------------')
    print(st)
    timeE1=st[0].stats.starttime;
    timeN1=st[1].stats.starttime;
    timeZ1=st[2].stats.starttime;
    stime=max(timeE1, timeN1, timeZ1)
    timeEe=st[0].stats.endtime;
    timeNe=st[1].stats.endtime;
    timeZe=st[2].stats.endtime;
    etime=min(timeEe, timeNe, timeZe)
    st[0].trim(stime, etime);
    st[1].trim(stime, etime);
    st[2].trim(stime, etime);
    print ('----------------------')
    print ('Streams after trimming')
    print ('----------------------')
    print(st)
    module_path = os.path.abspath(__file__)

    ELYSE_path = os.path.join(os.path.dirname(module_path), 'ELYSE.dataless')
    inv = obspy.read_inventory(ELYSE_path)
    for q in range(1,4):
        if q==1:
            comp=('DISP')
        elif q==2:
            comp=('VEL')
        elif q==3:
            comp=('ACC')
        st_rem1=st.copy()
        pre_filt = [0.005, 0.01, 8, 10] #for 20 Hz data
        st_rem1.remove_response(output = comp, taper_fraction=0.05, pre_filt = pre_filt, inventory = inv);
        sta = inv[0][0]
        azs = []
        dips = []
        trs = []
        channels = ['BHU','BHV','BHW']
        for chn in channels:
            chndata = sta.select(channel=chn)[0]
            print ('CHNDATA--------------------------------')
            print (chndata)
            azs.append(chndata.azimuth)
            dips.append(chndata.dip)
        
        (z, n, e) = rotate2zne(st_rem1[0], azs[0], dips[0], st_rem1[1], azs[1], dips[1], st_rem1[2], azs[2], dips[2])
        
        lenz = len(z)
        alp = 5e-2
        window = signal.tukey(len(z), alpha = alp)
        z = z * window
        n = n * window
        e = e * window
        st_new1=st_rem1.copy()
        st_new1[0].data = z;
        st_new1[0].stats.channel = 'BHZ'
        st_new1[1].data = n;
        st_new1[1].stats.channel = 'BHN'
        st_new1[2].data = e;
        st_new1[2].stats.channel = 'BHE'
        print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
        print(st_new1[0].stats)
        print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
        print(st_new1[1].stats)
        print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
        print(st_new1[2].stats)

        #path = ('DATA/')
        check = os.path.isdir(save_path)
        if check == False:
            os.mkdir(save_path)
        path = (os.path.join(save_path, class_2))
        check = os.path.isdir(path)
        if check == False:
            os.mkdir(path)
        path = (os.path.join(save_path, class_2, quality_2))
        check = os.path.isdir(path)
        if check == False:
            os.mkdir(path)
        path = (os.path.join(save_path, class_2, quality_2, event2find))
        check = os.path.isdir(path)
        if check == False:
            os.mkdir(path)
        filename1 = (path + '/' + event2find + '_' + comp + '.mseed')
        st_new1.write(filename1, format = 'MSEED')

    targetfile=(path + '/' + event2find + '.mseed')

    #copyfile('fdsnws_msds.mseed', targetfile)
    st.write(targetfile, format='MSEED')

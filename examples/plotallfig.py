import os

import numpy as np
import obspy
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
from scipy import signal, fft
import pprint as pp

import utils

plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = 20, 5
plt.rcParams['lines.linewidth'] = 0.5


cwd = os.getcwd()
paths = os.path.join(cwd, 'InSight-seismic-data-downloader/', 'DATA')

def to_type(paths): 
    for event_type in os.listdir(paths):
        path_type = os.path.join(paths, event_type)
        to_quality(path_type, event_type)

def to_quality(path_type, event_type):
    for event_quality in os.listdir(path_type):
        path_quality = os.path.join(path_type, event_quality)
        to_solar(path_quality, event_type, event_quality)

def to_solar(path_quality, event_type, event_quality):
    for solar in os.listdir(path_quality):
        path_solar = os.path.join(path_quality, solar)
        get_mseed(path_solar, event_type, event_quality, solar)

def get_mseed(path_solar, event_type, event_quality, solar):
    for mseed in os.listdir(path_solar):
        path_mseed = os.path.join(path_solar, mseed)
        data = obspy.read(path_mseed)
        plot_fig(data, event_type, event_quality, solar, mseed)
        
def plot_fig(data, event_type, event_quality, solar, mseed):
    ENZ = {0: 'E', 1: 'N', 2: 'Z'}
    path_fig = './fig/' + event_type + '/' + event_quality + '/' + solar + '/'
    os.system('mkdir -p ' + path_fig)
    name = mseed.split('.')
    for i in range(len(data)):
        figname = path_fig + name[0] + ENZ[i] + '.png'
        x = np.arange(0, data[i].stats.npts*data[i].stats.delta, data[i].stats.delta)
        plt.plot(x, data[i].data)
        plt.xlabel('Time [s]'); plt.title('traceN raw signal')
        plt.savefig(figname)
        plt.show()

os.system('rm -rf ./fig/*')
to_type(paths)

# Brian Blaylock
# August 28, 2017

"""
Copy files from OSG to Local drive
"""

import os 
from datetime import datetime
import multiprocessing # :)



def move_from_OSG_to_local(inputs):
    var, month, day, hour = inputs                     # TMP:2 m
    variable = var.replace(':', '_').replace(' ', '_') # TMP_2_m

    
    # Make the directory we want to store the OSG product in if it doens't exist
    DIR = '/uufs/chpc.utah.edu/common/home/horel-group2/blaylock/HRRR_OSG/daily30_20150418-20170801/%s/' % variable
    if not os.path.exists(DIR):
        os.makedirs(DIR)
    
    # This is the file we are looking for...
    FILE = 'OSG_HRRR_%s_m%02d_d%02d_h%02d_f00.h5' % (variable, month, day, hour) 

    # If file does not exist locally, try to retreive it from OSG
    if not os.path.isfile(DIR+FILE):
        os.system('scp blaylockbk@login.osgconnect.net:~/%s/%s %s' % (OSGpath, FILE, DIR))
        print 'SAVED:', DIR+FILE
    else:
        print FILE, 'is in local path. Moving on'

def rerun_in_serial(inputs):
    var, month, day, hour = inputs                     # TMP:2 m
    variable = var.replace(':', '_').replace(' ', '_') # TMP_2_m

    # Make the directory we want to store the OSG product in if it doens't exist
    DIR = '/uufs/chpc.utah.edu/common/home/horel-group2/blaylock/HRRR_OSG/daily30_20150418-20170801/%s/' % variable
    if not os.path.exists(DIR):
        os.makedirs(DIR)

    # This is the file we are looking for...
    FILE = 'OSG_HRRR_%s_m%02d_d%02d_h%02d_f00.h5' % (variable, month, day, hour) 

    # If the file still doesn't exist (i.e. scp didn't didn't fine the file), then run the statistics locally
    if not os.path.isfile(DIR+FILE):
        print "Can't get", variable, month, day, hour, "from OSG. Running the statistics locally."
        SCRIPTDIR = '/uufs/chpc.utah.edu/common/home/u0553130/pyBKB_v2/OpenScienceGrid/OSG_daily_30/'
        SCRIPT = 'OSG_HRRR_composite_daily30.py %s %s %s %s %s' % (var.replace(' ', '_'), month, day, hour, 0)
        os.system('python %s' % (SCRIPTDIR + SCRIPT))
    
if __name__ == '__main__':

    OSGpath = 'daily_30'
    var = 'WIND:10 m'
    variable = var.replace(':', '_').replace(' ', '_')

    months = range(1,13)
    days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    hours = range(0,24)

    args = [[var, month, day, hour] for month in months for day in range(1,days[month-1]+1) for hour in hours]

    num_proc = multiprocessing.cpu_count() # use all processors
    p = multiprocessing.Pool(num_proc)
    p.map(move_from_OSG_to_local, args)
    p.close()

    for i in args:
        rerun_in_serial(i)

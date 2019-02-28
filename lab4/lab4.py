'''
Assignment to learn how to interpolate data1
'''
import sys
import matplotlib.pyplot as plt
import numpy as np 
import scipy
import pandas as pd
import pprint as pp

#https://youtu.be/-zvHQXnBO6c
def read_wx_data(wx_file, harbor_data):
    """
    Read temperature and time data from file.
    Populates the harbor_data dictionary with two lists: wx_times and wx_temperatures
    :param wx_file: File object with data
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """   
    wx_times= []    #list of times in HH:MM:SS format
    wx_temperatures = []    #list of temps as floats

    with open(wx_file, mode='r') as file:        #open file
        file.readline() #skip first line
        for line in file:
            line_words = line.split(',')       #separate entries by space
            wx_times.append(line_words[1])    #add times to wx_times list
            wx_temperatures.append(float(line_words[3])) #add temperature to wx_temperatures list
    
    harbor_data["wx_times"] = wx_times  #store list of times in data dictionary
    harbor_data["wx_temperatures"] = wx_temperatures    #store list of temps in data dictionary
            



def read_gps_data(gps_file, harbor_data):
    """
    Read gps and altitude data from file.
    Populates the harbor_data dictionary with two lists: gps_times and gps_altitude
    :param gps_file: File object with gps data
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """
    gps_times = []  #list of times in HH:MM:SS format
    gps_altitude = []   #list of altitudes as ints

    with open(gps_file, mode='r') as file:        #open file
        file.readline()     #skip two lines
        file.readline()
        for line in file:
            line_words = line.split()       #separate entries by space
            gps_times.append("{0}:{1}:{2}".format(line_words[0], line_words[1], line_words[2]))    #add times to gps_times list
            gps_altitude.append(int(line_words[6]))  #add altitude to gps_altitude list
    harbor_data["gps_times"] = gps_times    #store list of times in data dictionary
    harbor_data["gps_altitude"] = gps_altitude #store list of altitudes in data dictionary
    
    


def interpolate_wx_from_gps(harbor_data):
    """
    Compute wx altitudes by interpolating from gps altitudes
    Populates the harbor_data dictionary with four lists:
        1) wx correlated altitude up
        2) wx correlated temperature up
        3) wx correlated altitude down
        4) wx correlated temperature down
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """
    wx_times = harbor_data["wx_times"]
    gps_times = harbor_data["gps_times"]
    gps_altitudes = harbor_data["gps_altitude"]
    alts_up = list(np.linspace(0, gps_altitudes[0],
                                num = (wx_times.index(gps_times[0])+1)) )      #initialize list with values from 0-first altitude
    print(gps_altitudes[-1],' ', gps_altitudes[-2])
    alts_down = []
    gps_index = 1 
    wx_index = wx_times.index(gps_times[0])
    cur_time = gps_times[1] #current elapsed time in gps list
    numseparate = 0 #number of missing entries between each elapsed time in gps list
    while wx_index < len(wx_times):
        if(wx_times[wx_index] >= cur_time and gps_altitudes[gps_index] > gps_altitudes[gps_index - 1]):
            alts_up.extend(np.linspace(gps_altitudes[gps_index - 1],    #add list of altitudes where start = gps altitude[gps_index-1], end = gps altitude[gps_index]
                                        gps_altitudes[gps_index],       #number of entries to add = number of missing entries compared to wx
                                         num = numseparate))
            numseparate = 0 #reset the number of missing entries            
            gps_index += 1 
            cur_time = gps_times[gps_index]
        elif wx_times[wx_index] >= cur_time: 
            alts_down.extend(np.linspace(gps_altitudes[gps_index - 1],    #add list of altitudes where start = gps altitude[gps_index-1], end = gps altitude[gps_index]
                                        gps_altitudes[gps_index],       #number of entries to add = number of missing entries compared to wx
                                         num = numseparate))
            numseparate = 0 #reset the number of missing entries
            gps_index += 1
            cur_time = gps_times[gps_index] 
        else:
            numseparate += 1 #increase number of missing entries
            wx_index += 1
    alts_down.extend(list(np.linspace(gps_altitudes[-1], gps_altitudes[-2], num= 15)))
    harbor_data["interpolated_altitude_up"] = alts_up   #add lists of altitudes and interpolated alts from gps_altitudes to harbor_data dictionary, 
    harbor_data["interpolated_altitude_down"] = alts_down   #descending altitude
    harbor_data["temps_up"] = (harbor_data["wx_temperatures"])[0:len(harbor_data["interpolated_altitude_up"])]
    harbor_data["temps_down"] = (harbor_data["wx_temperatures"])[len(harbor_data["interpolated_altitude_up"]):len(harbor_data["wx_times"])]



def plot_figs(harbor_data):
    """
    Plot 2 figures with 2 subplots each.
    :param harbor_data: A dictionary to collect data.
    :return: nothing
    """
    # Create canvas with two subplots
    plt.figure()
    plt.subplot(2, 1, 1)                # select first subplot
    plt.title("Harbor Flight Data")
    plt.plot(harbor_data["wx_times"], harbor_data["wx_temperatures"])   #plot wx_times v wx_temperatures
    plt.ylabel("Temperature, F")

    plt.subplot(2, 1, 2)                # select second subplot
    plt.ylabel("Altitude, ft")
    plt.xlabel("Time Elapsed (s)")
    plt.plot(harbor_data["gps_times"], harbor_data["gps_altitude"]) #plot gps_times v gps_altitude
    plt.show()      # display plot

    plt.figure()
    plt.subplot(1, 2, 1)
    plt.title("Harbor Ascent Flight Data")
    plt.ylabel("Altitude, Feet")
    plt.xlabel("Temperature, F")
    plt.plot(harbor_data["temps_up"], harbor_data["interpolated_altitude_up"])

    plt.subplot(1, 2, 2)
    plt.title("Harbor Descent Flight Data")
    plt.ylabel("Altitude, Feet")
    plt.xlabel("Temperature, F")
    #pp.pprint((harbor_data["interpolated_altitude_down"])[-10: -1])
    #print((harbor_data["temps_down"])[-10: -1])
    plt.plot(harbor_data["temps_down"], harbor_data["interpolated_altitude_down"])
    plt.show()


def wx_time_elapsed(start_time, times, harbor_data, end_time):
    """
    Turn HH:MM:SS wx times into list of elapsed time, start at 0 = first time
    Keep only times and temps within start time of wx file -> end time of gps file
    :param start_time: first time in wx times
    :param times: list of times in HH:MM:SS format
    :param harbor_data: dictionary to collect data
    :return: nothing
    """
    elapsed_times = []  #list of times as seconds since start of flight
    temps = []  #list of temps within the range of flight time
    for time in times:
        split_time = time.split(':')    #separate time entries by the colon 
        hours = int(split_time[0]) * 3600   #hour value -> seconds
        minutes = int(split_time[1]) * 60   #min value -> seconds
        seconds = int(split_time[2])
        if (hours + minutes + seconds) - start_time <= end_time:    #check if time elapsed is within the range of flight time
            elapsed_times.append((hours + minutes + seconds) - start_time) #add time to elapsed time list
        else:   #end loop, out of flight time
            break
    harbor_data["wx_times"] = elapsed_times #set list of wxtime = the times elapsed

    index = 0
    while index < len(harbor_data["wx_times"]): #get list of temps that were recorded during flight time
        temps.append((harbor_data["wx_temperatures"])[index])
        index+=1
    harbor_data["wx_temperatures"] = temps  #set list of temps = valid temps during flight

def gps_time_elapsed(start_time, times, harbor_data):
    """
    Turn HH:MM:SS gps times into list of elapsed times, 
        starting at 0 = first value in wx times
    :param start_time: first time in wx times (6 hours ahead of gps times)
    :param times: list of times from gps data
    :param harbor_data: dictionary to collect data
    :return: nothing
    """
    elapsed_times = []  #list of times as seconds since start of flight
    for time in times:
        split_time = time.split(':')    #separate time entries by the colon 
        hours = (int(split_time[0])-6) * 3600   #hours -> seconds (subtract six hours to match wx file)
        minutes = int(split_time[1]) * 60       # minutes -> seconds
        seconds = int(split_time[2])
        elapsed_times.append((hours + minutes + seconds) - start_time) #add time to elapsed time list
    harbor_data["gps_times"] = elapsed_times #set list of gps times = elapsed_times list
  



def main():
    """
    Main function
    :return: Nothing
    """
    harbor_data = {}
    wx_file = sys.argv[1]                   # first program input param
    gps_file = sys.argv[2]                  # second program input param

    read_wx_data(wx_file, harbor_data)      # collect weather data
    
    #find beginning of flight using wx_times list
    start_time = (harbor_data["wx_times"])[0]   
    start_time = int((int(start_time[0:2]) * 3600) + (int(start_time[3:5]) * 60) + int(start_time[6:8]))

    read_gps_data(gps_file, harbor_data)    # collect gps data
    gps_time_elapsed(start_time, harbor_data["gps_times"], harbor_data) #get elapsed times as seconds from start

    end_time = (harbor_data["gps_times"])[len(harbor_data["gps_times"]) - 1]        #find when flight ends according to gps file
    wx_time_elapsed(start_time, harbor_data["wx_times"], harbor_data, end_time)     #get elapsed wx times as seconds from start of flight
    #pp.pprint((harbor_data["gps_times"]))
    interpolate_wx_from_gps(harbor_data)    # calculate interpolated data
    plot_figs(harbor_data)                  # display figures


if __name__ == '__main__':
    main()
    exit(0)

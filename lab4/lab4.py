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
    wx_times= []
    wx_temperatures = []

    with open(wx_file, mode='r') as file:        #open file
        file.readline()
        for line in file:
            line_words = line.split(',')       #separate entries by space
            wx_times.append(line_words[1])    #add times to wx_times list
            wx_temperatures.append(line_words[3]) #add temperature to wx_temperatures list
    
    harbor_data["wx_times"] = wx_times
    harbor_data["wx_temperatures"] = wx_temperatures
            



def read_gps_data(gps_file, harbor_data):
    """
    Read gps and altitude data from file.
    Populates the harbor_data dictionary with two lists: gps_times and gps_altitude
    :param gps_file: File object with gps data
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """
    gps_times = []
    gps_altitude = []

    with open(gps_file, mode='r') as file:        #open file
        file.readline()     #skip two lines
        file.readline()
        for line in file:
            line_words = line.split()       #separate entries by space
            gps_times.append("{0}:{1}:{2}".format(line_words[0], line_words[1], line_words[2]))    #add times to gps_times list
            gps_altitude.append(line_words[6])  #add altitude to gps_altitude list
    harbor_data["gps_times"] = gps_times
    harbor_data["gps_altitude"] = gps_altitude
    
    


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
    pass


def plot_figs(harbor_data):
    """
    Plot 2 figures with 2 subplots each.
    :param harbor_data: A dictionary to collect data.
    :return: nothing
    """
    pass


def main():
    """
    Main function
    :return: Nothing
    """
    harbor_data = {}
    wx_file = sys.argv[1]                   # first program input param
    gps_file = sys.argv[2]                  # second program input param

    read_wx_data(wx_file, harbor_data)      # collect weather data
    read_gps_data(gps_file, harbor_data)    # collect gps data
        
    pp.pprint(harbor_data["gps_times"])
    interpolate_wx_from_gps(harbor_data)    # calculate interpolated data
    plot_figs(harbor_data)                  # display figures


if __name__ == '__main__':
    main()
    exit(0)

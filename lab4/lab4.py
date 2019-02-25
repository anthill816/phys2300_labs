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
            wx_times.append(line_words[1])    #add date to wdates list
            wx_temperatures.append(line_words[3]) #add temperature to wtemperatures list
    
    index = 0
    for time in wx_times:
        if(time in harbor_data):
            harbor_data[time] += wx_temperatures[index]
        else:
            harbor_data[time] = wx_temperatures[index]
        index += 1
            



def read_gps_data(gps_file, harbor_data):
    """
    Read gps and altitude data from file.
    Populates the harbor_data dictionary with two lists: gps_times and gps_altitude
    :param gps_file: File object with gps data
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """
    pass


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
    pp.pprint(harbor_data)
    read_gps_data(gps_file, harbor_data)    # collect gps data
    interpolate_wx_from_gps(harbor_data)    # calculate interpolated data
    plot_figs(harbor_data)                  # display figures


if __name__ == '__main__':
    main()
    exit(0)

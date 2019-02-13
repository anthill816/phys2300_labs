'''
--------------------------------------------------------------------------------
G e n e r a l I n f o r m a t i o n
--------------------------------------------------------------------------------
Name: weather.py

Usage: python datafile

Description: Code to analyze weather data

Inputs: name of data file containing weather data

Outputs: plots and analysis

Auxiliary Files: None

Special Instructions: None

--------------------------------------------------------------------------------
'''
import sys
import matplotlib.pylab as plt
import numpy as np

# Pseudocode:
# 1) get the name of the data file from the user on the command line
# 2) open the data file
# 3) read the first line of data and throw it away (it is the header info the computer doesn't need)
#       from all the remaining lines:
#       read in the date (index 2) and temperature (index 3)
#       parse the date string into year, month, day
#       convert year, month, day into decimal years for plotting (this would make a great function!)
#       (need to pay attention to leap years here!)
# 4) make two lists for the time series - the decimal year list and the temperature list
# 5) sort the data by month so we can average it and take the standard deviation later
# 6) Plot the results


def parse_data(infile):
    """
    Function to parse weather data
    :param infile: weather data input file
    :return: two lists. One list with the information from the third column (date)
                        One list with the information from the fourth column (temperature)
    """
    wdates = []             # list of dates data
    wtemperatures = []      # list of temperature data
    wlows = []
    whighs = []
    with open(infile, mode='r') as file:        #open file
        file.readline()
        for line in file:
            line_words = line.split()       #separate entries by space
            wdates.append(line_words[2])    #add date to wdates list
            wtemperatures.append(line_words[3]) #add temperature to wtemperatures list
            whighs.append(float(line_words[17]))
            wlows.append(float(line_words[18]))

    return wdates, wtemperatures, wlows, whighs


def calc_mean_std_dev(wdates, wtemp):
    """
    Calculate the mean temperature per month
    Calculate the standard deviation per month's mean
    :param wdates: dictionary with dates fields
    :param wtemp: temperature per month
    :return: means, std_dev: months_mean and std_dev lists
    """
    monthsandtemps = {"01": [], "02": [], "03": [], "04": [],
                     "05": [], "06": [], "07": [], "08": [],
                     "09": [], "10": [], "11": [], "12": []}         #dictionary with month keys and temp values
    index = 0

    for date in wdates:         #create a dictionary with the month as key as temps as values
        if(date[4:6] in monthsandtemps):        #add temperature value if the month is already a key
            monthsandtemps[(date[4:6])] += [float(wtemp[index])]
        else:    #add month as key and first temperature value of that month to dictionary
            monthsandtemps[(date[4:6])] = [float(wtemp[index])]
        index += 1

    means = []      #list of means per month
    std_dev = []    #list of std_dev per month
   
    for month in monthsandtemps:        #find mean per month
       total = sum(monthsandtemps[month])       #sum of all values in a month
       size = len(monthsandtemps[month])        #number of temps in a month
       means += [total / size]                  #add mean 

    for month in monthsandtemps:            #find standard deviation per month
        std_dev += [np.std(monthsandtemps[month])]

    return means, std_dev



def plot_data_task1(wyear, wtemp, month_mean, month_std):
    """
    Create plot for Task 1.
    :param: wyear: list with year (in decimal)
    :param: wtemp: temperature per
    :param: month_mean: list with month's mean values
    :param: month_std: list with month's mean standard dev values
    """
    # Create canvas with two subplots
    plt.figure()
    plt.subplot(2, 1, 1)                # select first subplot
    plt.title("Temperatures at Ogden")
    plt.plot(wyear, wtemp, "bo")
    plt.ylabel("Temperature, F")
    plt.xlabel("Decimal Year")

    plt.subplot(2, 1, 2)                # select second subplot
    plt.ylabel("Temperature, F")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthNumber = list(range(1, 13, 1))
    plt.xlim([0.7, 13])
    plt.ylim([0, 90])
    width = 0.8
    plt.bar(monthNumber, month_mean, yerr=month_std, width=width,
            color="lightgreen", ecolor="black", linewidth=1.5)
    plt.xticks(monthNumber, months)
    plt.show()      # display plot


def plot_data_task2(wyear, whigh, wlow):
    """
    Create plot for Task 2. Describe in here what you are plotting
    Also modify the function to take the params you think you will need
    to plot the requirements.
    :param: xxx??
    """
    plt.title("High and Low Temperatures at Ogden")
    plt.plot(wyear, whigh, "bo", label="Maximum Temp")
    plt.plot(wyear, wlow, "ro", label="Minimum Temp")
    plt.ylabel("Temperature, F")
    plt.xlabel("Decimal Year")
    plt.legend()
    plt.show()

def get_year_and_temp(wdates, wtemps):  
    """
    Gather years and list of temps in each year
    param: wdates = list of dates as strings
    param: wtemps = list of temps as strings

    return: wyear = list of years as floats
    return: wtemp = list of temps as floats
    """
    wyear = []      #list of years
    wtemp = []      #list of temps

    for date in wdates:     #collect all years as floats
        year = date[0:4]
        wyear += [float(year)]                 #add year to wyear list


    for temp in wtemps:     #collect all temps as floats
        wtemp += [float(temp)]

    return wyear, wtemp

def find_hi_lo(wdates, whighs, wlows):
    """
    Find highest and lowest temerature per year

    Param: wdates = list of dates
    Param: whighs = list of highs
    Param: wlows = list of lows

    Return: years = list of years
    Return: hiyear = list of valid highs per year
    Return: loyear = list of valid lows per year
    """
    hitempsperyear = {}     #dictionary of high temps per year
    lotempsperyear = {}     #dictionary of low temps per year
    index = 0

    hiyear = []
    loyear = []
    years = []

    #get rid of any values equal to '9999.9'
    for date in wdates:
        year = date[0:4]
        if year in hitempsperyear:
            if(whighs[index] != 9999.9):
                hitempsperyear[year] += [float(whighs[index])]
            if(wlows[index] != 9999.9):
                lotempsperyear[year] += [float(wlows[index])]
        else:
            if(whighs[index] != 9999.9):
                hitempsperyear[year] = [float(whighs[index])]
            if(wlows[index] != 9999.9):
                 lotempsperyear[year] = [float(wlows[index])]
        index += 1

    for year in hitempsperyear:
        years += [float(year)]
        hiyear.append(max(hitempsperyear[year]))      #store max value in each year
    for year in lotempsperyear:
        loyear.append(min(lotempsperyear[year]))    #store min value for each year

    return years, hiyear, loyear

def main(infile):
    weather_data = infile    # take data file as input parameter to file
    wdates, wtemperatures, wlows, whighs = parse_data(weather_data)
    # Calculate mean and standard dev per month
    month_mean, month_std = calc_mean_std_dev(wdates, wtemperatures)
    # TODO: Make sure you have a list of:
    #       1) years, 2) temperature, 3) month_mean, 4) month_std
    wyear, wtemp = get_year_and_temp(wdates, wtemperatures)
    plot_data_task1(wyear, wtemp, month_mean, month_std)
    # TODO: Create the data you need for this

    years, highs, lows = find_hi_lo(wdates, whighs, wlows)
    plot_data_task2(years, highs, lows)



if __name__ == "__main__":
    # infile = 'data/CDO6674605799016.txt'  # for testing
    # Note: the 0th argument is the program itself.
    infile = sys.argv[1]
    main(infile)
    exit(0)

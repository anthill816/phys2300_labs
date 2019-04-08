from math import sqrt
import numpy as numpy
from vpython import *
import argparse

rearth = 1.5e11 #radius in x direction, in meters
rsun = 0
vearth = 3e4 #velocity in y direction in m/s
vsun = 0 #velocity in both directions, m/2
mearth = 5.97e24 #mass of earth in kg
msun = 1.99e30 #mass of sun in kg
deltat = 6.3e4 #change in time in seconds
Ttotal = 3.15e7 #total period in seconds
G = 6.674e-11 #Newton's constant

def visualize(objects, dt):
    """
    visualize the system
    param: objects = list holding spheres
    param: dt = time step
    """
    for i in objects:
        i.acceleration = vector(0, 0, 0)
        for j in objects:
            if i!=j:
                dist = j.pos - i.pos
                i.acceleration = i.acceleration + G * j.mass * dist / mag(dist)**3
        for i in objects:
            i.velocity = i.velocity + i.acceleration * dt
            i.pos = i.pos + i.velocity * dt

def gatherinfo(num_bodies):
    """
    Get initial information from user
    Return: array of masses
          : array of x_positions
          : array of y_positions
          : array of x_velocities
          : array of y_velocities
          : float time step
          : float total time
    param: num_bodies = number of bodies in the system
    """
    masses = []
    x_positions = []
    y_positions = []
    z_positions = []
    x_velocities = []
    y_velocities = []
    z_velocities = []

    index = 0
    while(index < num_bodies):
        #gather information of each body
        masses.append(float(input("Please enter the mass of body {} (in kg): ".format(index + 1))))
        x_positions.append(float(input("Please enter the initial x position of body {} (in meters): ".format(index + 1))))
        y_positions.append(float(input("Please enter the initial y position of body {} (in meters): ".format(index + 1))))
        z_positions.append(float(input("Please enter the initial z position of body {} (in meters): ".format(index + 1))))
        x_velocities.append(float(input("Please enter the velocity in the x direction of body {} (in m/s): ".format(index + 1))))
        y_velocities.append(float(input("Please enter the velocity in the y direction of body {} (in m/s): ".format(index + 1))))
        z_velocities.append(float(input("Please enter the intial z velocity of body {} (in m/s): ".format(index + 1))))
        index += 1


    #get time information
    t_step = float(input("Please enter the time step: "))
    total_time = float(input("Please enter the total time the simulation should run: "))
    return masses, x_positions, y_positions, z_positions, x_velocities, y_velocities, z_velocities, t_step, total_time

def read_file(filename):
    """
    gather body information from a file
    param: filename = name of file to get info from
    Return: array of masses
          : array of x_positions
          : array of y_positions
          : array of x_velocities
          : array of y_velocities
          : float time step
          : float total time
    """
    #NO MASSES INCLUDED IN FILE
    masses = []
    x_positions = []
    y_positions = []
    z_positions = []
    x_velocities = []
    y_velocities = []
    z_velocities = []

    with open(filename, mode='r') as file:        #open file
        file.readline() #skip first line
        file.readline() #skip second line
        for line in file:
            line_words = line.split(',')       #separate entries by comma
            #add positions to lists, converted to meters
            x_positions.append(float(line_words[1])*1.496e+11)
            y_positions.append(float(line_words[2])*1.496e+11)
            z_positions.append(float(line_words[3])*1.496e+11)
            #add velocities to lists
            x_velocities.append(float(line_words[4])*1.496e+11)
            y_velocities.append(float(line_words[5])*1.496e+11)
            z_velocities.append(float(line_words[6])*1.496e+11)
    t_step = float(input("Please enter the time step: "))
    total_time = float(input("Please enter the total time the simulation should run: "))
    return masses, x_positions, y_positions, z_positions, x_velocities, y_velocities, z_velocities, t_step, total_time

def main():
    """
    Main method
    """
    # 1) Parse the arguments
    parser = argparse.ArgumentParser(description="N-Body Simulation")
    parser.add_argument("--file", "-f", action="store", help="file input", dest="input_file", default="empty")
    args = parser.parse_args()
    num_bodies = 0 #number of bodies reacting in the system

    if(args.input_file != "empty"):
        read_file(args.input_file)
    else:
        #make sure that the number of bodies is 2 or greater
        while(num_bodies < 2):
            num_bodies = float(input("How many bodies are in your system?: "))
        #gather all information from user
        masses, x_positions, y_positions, z_positions, x_velocities, y_velocities, z_velocities, t_step, total_time = gatherinfo(num_bodies)
        #create spheres to be used 
    
    index = 0
    objects = [] #list to hold spheres
    positions = []
    while(index < num_bodies):
        objects.append(sphere(pos=vector(x_positions[index], y_positions[index], z_positions[index]), radius=6371000000))
        positions.append([]) #add an empty list to hold values for each body
        index += 1

    
    

    t = 0 #initial time
    index1 = 0 
    index2 = 0
    acceleration = vector(0, 0, 0)  
    while t < total_time:
        while index1 < len(masses):  #for i in objects
            acceleration *= 0 #reset acceleration
            while index2 < len(masses): # for j in objects
                if(index1 != index2): # if i != j
                    #dist = j.pos - i.pos
                    r12 = vector((x_positions[index2] - x_positions[index1]), (y_positions[index2]-y_positions[index1]), (z_positions[index2]-z_positions[index1]))
                    abs_r12 = sqrt((x_positions[index2] - x_positions[index1])**2 + (y_positions[index2]-y_positions[index1])**2 + (z_positions[index2]-z_positions[index1])**2)
                    acceleration += G * masses[index2] *r12 / (abs_r12**3)
                index2 += 1 #increment index for inner loop
            index2 = 0 #reset index for inner loop
            #acceleration * dt
            delta_v = acceleration * t_step #find change in velocity
            acceleration *=0
            #update velocities
            x_velocities[index1] += delta_v.x
            y_velocities[index1] += delta_v.y
            z_velocities[index1] += delta_v.z
            #update positions
            x_positions[index1] += x_velocities[index1] * t_step
            y_positions[index1] += y_velocities[index1] * t_step
            z_positions[index1] += z_velocities[index1] * t_step
            # objects[index1].pos = vector(x_positions[index1], y_positions[index1], z_positions[index1])
            #add position to list for animation later
            positions[index1].append(vector(x_positions[index1], y_positions[index1], z_positions[index1]))
            index1+=1
        index1 = 0
        t+=t_step

    index = 0
    for posit in positions[0]:
        rate(10)
        obj_index = 0
        for obj in objects:
            obj.pos = (positions[obj_index])[index]
            obj_index += 1
        index+=1


if __name__ == "__main__":
    main()
    exit(0)
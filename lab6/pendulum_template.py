import numpy as np
from matplotlib import pyplot as plt
from vpython import *

g = 9.81    # m/s**2, gravity
l = 1    # meters, length of arm
l_2 = 1.5 #meters, length of second arm
W = 0.01   # arm radius
R = 0.07    # ball radius
framerate = 100
steps_per_frame = 10

def set_scene():
    """
    Set Vpython Scene
    """
    scene.title = "Assignment 6: Not so simple pendulum"
    scene.width = 800
    scene.heigth = 600
    scene.caption = """Right button drag or Ctrl-drag to rotate "camera" to view scene.
    To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
    On a two-button mouse, middle is left + right.
    Touch screen: pinch/extend to zoom, swipe or two-finger rotate."""
    scene.forward = vector(0, -.3, -1)
    scene.x = -1

def f(angles):
    """
    First Pendulum
    param: angles = array with index 0 = theta, index 1 = omega
    """
    theta = angles[0]
    omega = angles[1]
    ftheta = omega
    fomega = -(g/l)*np.sin(theta) - 2 * omega
    return np.array([ftheta, fomega], float)

def f_2nd(angles):
    """
    Second pendulum
    param: angles = array with index 0 = theta, index 1 = omega
    """
    theta = angles[0]
    omega = angles[1]
    ftheta = omega
    fomega = -(g/l_2)*np.sin(theta) - 2 * omega
    return np.array([ftheta, fomega], float)


def plot_theta(angles, times):
    """
    Create of plot of theta v time
    Param: angles = list of thetas
    Param: times = list of times
    """
    plt.plot(times, angles)
    plt.xlabel("Time in Seconds")
    plt.ylabel("Angle in Radians")
    plt.title("Movement of a Pendulum")
    plt.show()


def main():
    """
    Main method
    """
    #set vpython scene
    set_scene()

    angles = []
    times = []

    # Set up initial values
    h = 1.0/(framerate * steps_per_frame)
    #angles for first pendulum
    r = np.array([np.pi*179/180, 0], float)
    #angles for second pendulum
    r_2 = np.array([np.pi*179/180, 0], float)
    # Initial x and y
    x = l*np.sin(r[0])
    y = -l*np.cos(r[0])

    #display starting point of pendulum rod
    pivotball = sphere(pos=vector(x, y, 0), radius=.05)
    rod1 = cylinder(pos=vector(x, y, 0), axis=vector(cos(r[0]), -sin(r[0]), 0), radius=.01)
    rod2 = cylinder(pos=vector(x, y, 0), axis=vector(cos(r[0]), -sin(r[0]), 0), radius=.01, color=color.blue)
    bob1 = sphere(pos=vector(x, y, 0), radius=0.07)
    bob2 = sphere(pos=vector(x, y, 0), radius=0.07, color=color.blue)
    # Loop over some time interval
    dt = 0.01
    t = 0
        # Use the 4'th order Runga-Kutta approximation
    for i in range(framerate):
        rate(5)
        #get values for first pendulum
        k1 = f(r)
        k2 = h * f(r + 0.5 * k1)
        k3 = h * f(r + 0.5 * k2)
        k4 = h * f(r + k3)
        r += (k1 + 2 * k2 + 2 * k3 + k4)/6
        #get values for second pendulum
        k1_2 = f_2nd(r_2)
        k2_2 = h * f_2nd(r_2 + 0.5 * k1_2)
        k3_2 = h * f_2nd(r_2 + 0.5 * k2_2)
        k4_2 = h * f_2nd(r_2 + k3_2)
        r_2 += (k1_2 + 2 * k2_2 + 2 * k3_2 + k4_2)/6

        #gather angle and time values to use for graphing
        angles.append(r[0])
        # angles.append(r_2[0])
        times.append(t)
        t += dt
        # Update positions
        x = np.cos(r[0] - np.pi/2)
        y = -abs(np.sin(r[0] - np.pi/2)) 
        
        x_2 = np.cos(r_2[0] - np.pi/2)
        y_2 = -abs(np.sin(r_2[0] - np.pi/2)) 
        # Update the cylinder axis
        rod1.axis = vector(x, y, 0)
        rod2.axis = vector(x_2 * l_2, y_2 * l_2, 0)
        # Update the pendulum's bob
        bob1.pos=vector(x + .025, y + 1, 0)
        bob2.pos = vector(x_2 + .025, y_2 + .5, 0)

    plot_theta(angles, times)

if __name__ == "__main__":
    main()
    exit(0)

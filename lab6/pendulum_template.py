import numpy as np
from matplotlib import pyplot as plt
from vpython import *

g = 9.81    # m/s**2
l = 1    # meters
W = 0.002   # arm radius
R = 0.01     # ball radius
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
    # Set background: floor, table, etc

def f(angles):
    """
    Pendulum
    """
    theta = angles[0]
    omega = angles[1]
    ftheta = omega
    fomega = -(g/l)*np.sin(theta) -  2 * omega
    return np.array([ftheta, fomega], float)

def plot_theta(angles, times):
    """
    Create of plot of theta v time
    Param: angles = list of thetas
    Param: times = list of times
    """
    plt.plot(times, angles)
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
    r = np.array([np.pi*179/180, 0], float)
    # Initial x and y
    x = l*np.sin(r[0])
    y = -l*np.cos(r[0])

    #display starting point of pendulum rod
    pivotball = sphere(pos=vector(x, y, 0), radius=.05)
    rod = cylinder(pos=vector(x, y, 0), axis=vector(cos(r[0]), -sin(r[0]), 0), radius=.01)
    # Loop over some time interval
    dt = 0.01
    t = 0
        # Use the 4'th order Runga-Kutta approximation
    for i in range(framerate):
        # k1 = h * f([r, t])
        rate(5)
        k1 = f(r)
        k2 = h * f(r + 0.5 * k1)
        k3 = h * f(r + 0.5 * k2)
        k4 = h * f(r + k3)
        r += (k1 + 2 * k2 + 2 * k3 + k4)/6
        # r += h*f(r)
        angles.append(r[0])
        times.append(t)
        t += dt
        # Update positions
        x = np.cos(r[0] - np.pi/2)
        y = -abs(np.sin(r[0] - np.pi/2)) 
        
        # Update the cylinder axis
        rod.axis = vector(x, y, 0)
        # Update the pendulum's bob
    plot_theta(angles, times)

if __name__ == "__main__":
    main()
    exit(0)

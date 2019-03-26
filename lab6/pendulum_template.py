import numpy as np
from matplotlib import pyplot as plt
from vpython import *

g = 9.81    # m/s**2
l = 0.1     # meters
W = 0.002   # arm radius
R = 0.01     # ball radius
framerate = 100
steps_per_frame = 10

def set_scene():
    """
    Set Vpython Scene
    """
    scene.title = "Assignment 5: Projectile motion"
    scene.width = 800
    scene.heigth = 600
    scene.caption = """Right button drag or Ctrl-drag to rotate "camera" to view scene.
    To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
    On a two-button mouse, middle is left + right.
    Touch screen: pinch/extend to zoom, swipe or two-finger rotate."""
    scene.forward = vector(0, -.3, -1)
    scene.x = -1
    # Set background: floor, table, etc

def f(r):
    """
    Pendulum
    """
    theta = r[0]
    omega = r[1]
    ftheta = omega
    fomega = -(g/l)*np.sin(theta)
    return np.array([ftheta, fomega], float)


def main():
    """
    """
    set_scene()
    print("hi")
    # Set up initial values
    h = 1.0/(framerate * steps_per_frame)
    r = np.array([np.pi*179/180, 0], float)
    # Initial x and y
    x = l*np.sin(r[0])
    y = -l*np.cos(r[0])

    #display starting point of pendulum rod
    pivotball = sphere()
    rod = cylinder(pos=vector(x, y, 0), axis=vector(1, 0, 0), radius=.01)
    # Loop over some time interval
    dt = 0.01
    t = 0
        # Use the 4'th order Runga-Kutta approximation
    for i in range(steps_per_frame):
        k1 = h * f([angles, t])
        k2 = h * f([angles + 0.5 * k1, t])
        k3 = h * f([angles + 0.5 * k2, t])
        k4 = h * f([angles + k3, t])
        angles += (k1 + 2 * k2, 2 * k3, k4)/6
        r += h*f(r)
        t += dt
        # Update positions
        x = l*np.sin(r[0])
        y = -l*np.cos(r[0])
        # Update the cylinder axis
        # Update the pendulum's bob

if __name__ == "__main__":
    main()
    exit(0)

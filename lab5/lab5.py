from vpython import *
from math import sin, cos, radians
import argparse
import numpy as np
import pprint as pp



def set_scene(data):
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


def motion_no_drag(data):
    """
    Create animation for projectile motion with no dragging force
    """
    ball_nd = sphere(pos=vector(0, data['init_height'], 0),
                        radius=1, color=color.cyan, make_trail=True)
    
    # # Follow the movement of the ball
    scene.camera.follow(ball_nd)
    # Create lists of x and y values of motion

    index = 1
    y_values = [data['init_height']]
    y_velocities = [data['init_y_vel']]
    x_values = [0]
    while y_values[index-1] > 0 or index == 1:
        new_x = x_values[index - 1] + data['init_x_vel'] * data['deltat'] # find next x position
        x_values.append(new_x) #add generated x position to list
        
        new_y_vel = y_velocities[index - 1] + data['gravity'] * data['deltat'] # find new y velocity
        y_velocities.append(new_y_vel)
        new_y = y_values[index - 1] + new_y_vel * data['deltat']
        y_values.append(new_y)
        index += 1

    #create scenery elements (ground and mountains)
    ground = box(pos=vector(x_values[-1]/2,-1,-x_values[-1]/4 + 10), color=color.green, size=vector(x_values[-1] + 20, 1, x_values[-1]/2))
    mount1 = cone(pos=vector(3 * x_values[-1] / 8 - 20,-1,-3 * x_values[-1] / 8), axis=vector(0, max(y_values), 0), radius=(3 * x_values[-1] / 8), color=color.white)
    mount2 = cone(pos=vector(x_values[-1] * .825 - 20,-1,-3 * x_values[-1] / 8), axis=vector(0, max(y_values) * 2, 0), radius=(3 * x_values[-1] / 8), color=color.white)
    #Animate
    pos_index = 0
    while pos_index < len(y_values):
        rate(100)
        position = vector(x_values[pos_index], y_values[pos_index], 0)
        ball_nd.pos = position
        pos_index += 1



def motion_drag(data):
    """
    Create animation for projectile motion with dragging force
    """
    index = 1
    y_values = [data['init_height']]
    y_velocities = [data['init_y_vel']]
    x_values = [0]
    while y_values[index-1] > 0 or index == 1:
        new_x = x_values[index - 1] + data['init_x_vel'] * data['deltat'] # find next x position
        x_values.append(new_x) #add generated x position to list
        
        new_y_vel = y_velocities[index - 1] + data['gravity'] * data['deltat'] # find new y velocity
        y_velocities.append(new_y_vel)
        new_y = y_values[index - 1] + new_y_vel * data['deltat']
        y_values.append(new_y)
        index += 1
     
        

    


def main():
    """
    """
    # 1) Parse the arguments
    parser = argparse.ArgumentParser(description="Demo")
    parser.add_argument("--velocity", "-v", action="store", help="velocity in m/s", dest="velocity", type=float, required="true")
    parser.add_argument("--angle", "-a", action="store", help="angle in degrees", dest="angle", type=float, required="true")
    parser.add_argument("--height",  action="store", help="height in meters", dest="height", type=float, default=1.2)

    args = parser.parse_args()
    # Set Variables
    data = {}       # empty dictionary for all data and variables
    data['init_height'] = args.height   # y-axis  
    data['init_velocity'] = args.velocity  # m/s
    data['theta'] = args.angle       # degrees

    rad_angle = radians(args.angle) # angle in radians
    data['init_x_vel'] = cos(rad_angle) * args.velocity # velocity in the x-direction
    data['init_y_vel'] = sin(rad_angle) * args.velocity # velocity in the y-direction

    # Constants
    data['rho'] = 1.225  # kg/m^3
    data['Cd'] = 0.5    # coefficient friction
    data['deltat'] = 0.005
    data['gravity'] = -9.8  # m/s^2

    data['ball_mass'] = 0.145  # kg
    data['ball_radius'] = 0.075  # meters
    data['ball_area'] = pi * data['ball_radius']**2
    data['alpha'] = data['rho'] * data['Cd'] * data['ball_area'] / 2.0
    data['beta'] = data['alpha'] / data['ball_mass']
    # Set Scene
    set_scene(data)
    # 2) No Drag Animation
    motion_no_drag(data)
    # 3) Drag Animation
#     motion_drag(data)
    # 4) Plot Information: extra credit
#     plot_data(data)


if __name__ == "__main__":
    main()
    exit(0)

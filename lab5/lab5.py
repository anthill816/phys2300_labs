from vpython import *
from math import sin, cos, radians
import argparse
import numpy as np
import pprint as pp
import matplotlib.pyplot as plt




def set_scene(data):
    """
    Set Vpython Scene
    param: data = dictionary with all data
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
    param: dictionary with all data
    """
    ball_nd = sphere(pos=vector(0, data['init_height'], 0),
                        radius=1, color=color.cyan, make_trail=True)
    
    # # Follow the movement of the ball
    scene.camera.follow(ball_nd)

    # Create lists of x and y values of motion
    index = 1 
    y_values = [data['init_height']] #list of all y positions
    y_velocities = [data['init_y_vel']] # list of y velocities
    x_values = [0] #list of all x positions
    while y_values[index-1] > 0 or index == 1:
        new_x = x_values[index - 1] + data['init_x_vel'] * data['deltat'] # find next x position
        x_values.append(new_x) #add generated x position to list
        
        new_y_vel = y_velocities[index - 1] + data['gravity'] * data['deltat'] # find new y velocity
        y_velocities.append(new_y_vel)
        new_y = y_values[index - 1] + new_y_vel * data['deltat'] #fine new y position
        y_values.append(new_y) #add new position to the list
        index += 1

    #create scenery elements (ground and mountains)
    ground = box(pos=vector(x_values[-1]/2,-1,-x_values[-1]/4 + 10), color=color.green, size=vector(x_values[-1] + 20, 1, x_values[-1]/2))
    mount1 = cone(pos=vector(3 * x_values[-1] / 8 - 20,-1,-3 * x_values[-1] / 8), axis=vector(0, max(y_values), 0), radius=(3 * x_values[-1] / 8), color=color.white)
    mount2 = cone(pos=vector(x_values[-1] * .825 - 20,-1,-3 * x_values[-1] / 8), axis=vector(0, max(y_values) * 2, 0), radius=(3 * x_values[-1] / 8), color=color.white)
    #Animate

    #loop through lists to change the position of the ball
    pos_index = 0
    while pos_index < len(y_values):
        rate(500)
        position = vector(x_values[pos_index], y_values[pos_index], 0)
        ball_nd.pos = position
        pos_index += 1
    
    #add positions to the data dictionary to be graphed
    data['x_no_drag'] = x_values
    data['y_no_drag'] = y_values



def motion_drag(data):
    """
    Create animation for projectile motion with dragging force
    param: data = dictionary with all data
    """
    ball_nd = sphere(pos=vector(0, data['init_height'], 0),
                        radius=1, color=color.magenta, make_trail=True)
    
    # # Follow the movement of the ball
    scene.camera.follow(ball_nd)
    # Create lists of x and y values of motion
    index = 1
    x_vel = data['init_x_vel']
    y_values = [data['init_height']]
    y_vel = data['init_y_vel']
    x_values = [0]
    while y_values[index-1] > 0 or index == 1:
        # new_x = x_values[index - 1] + data['init_x_vel'] * data['deltat'] # find next x position
        x_vel = x_vel + data['x_drag_accel'] * data['deltat']
        # data['x_drag_accel'] = data['x_drag_accel'] - x_vel * data['beta']   #update acceleration based on new velocity
        new_x = x_values[index - 1] + x_vel * data['deltat']
        x_values.append(new_x) #add generated x position to list
        
        y_vel = y_vel + data['y_drag_accel'] * data['deltat'] # find new y velocity
        new_y = y_values[index - 1] + y_vel * data['deltat']
        y_values.append(new_y)

        index += 1
     #Animate
    pos_index = 0
    while pos_index < len(y_values):
        rate(500)
        position = vector(x_values[pos_index], y_values[pos_index], 0)
        ball_nd.pos = position
        pos_index += 1
    
    #add lists of positions to the data dictionary to be graphed
    data['x_drag'] = x_values
    data['y_drag'] = y_values
     
        
def plot_data(data):
    """
    Use lists of positions with and without drag
    to create a graph
    param: data = dictionary with all data
    """
     # Create canvas with two plots on one graph
    plt.figure()
    plt.title("Position with and without drag force")
    plt.plot(data["x_no_drag"], data["y_no_drag"], "g-", label="Position without Drag")   #plot x vs y position without drag
    plt.ylabel("Y Position (m)")
    plt.xlabel("X Position (m)")

    plt.plot(data["x_drag"], data["y_drag"], "b-", label="Position with Drag") #plot x vs y position with drag
    plt.legend()
    plt.show()      # display plot
    


def main():
    """
    Main method
    """
    # 1) Parse the arguments
    parser = argparse.ArgumentParser(description="Projectile Motion")
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
    data['rho'] = 1.225  # kg/m^3, density
    data['Cd'] = 0.5    # coefficient friction
    data['deltat'] = 0.005
    data['gravity'] = -9.8  # m/s^2

    data['ball_mass'] = 0.145  # kg
    data['ball_radius'] = 0.075  # meters
    data['ball_area'] = pi * data['ball_radius']**2
    data['alpha'] = data['rho'] * data['Cd'] * data['ball_area'] / 2.0
    data['beta'] = data['alpha'] / data['ball_mass']

    #acceleration when the ball experiences drag
    data['x_drag_accel'] = - data['beta'] * data['init_x_vel']
    data['y_drag_accel'] = data['gravity'] - data['beta'] * data['init_y_vel'] 
    # Set Scene
    set_scene(data)
    # 2) No Drag Animation
    motion_no_drag(data)
    # 3) Drag Animation
    motion_drag(data)
    # 4) Plot Information: extra credit
    plot_data(data)


if __name__ == "__main__":
    main()
    exit(0)

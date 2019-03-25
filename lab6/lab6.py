import numpy as np


def f_theta_omega(angles, times):
    """
    Calculate the angle theta of displacement for
        several periods of the pendulum when it's released
        from standstillat theta = 179 degrees
    param: angles = array with omega and theta
    param: times = array with periods of time
    Graph theta as a function of time
    """
    # gravity = 9.81
    # arm_length = 0.1 

    # omega = angles[0]
    # theta = angles[1]
    # ftheta = omega
    # fomega = -(gravity/arm_length) * np.sin(theta)
    pass

def theta_v_time():
    """
    create a plot of theta as a function of time
    """
    pass

def animate_pendulum():
    """
    Animate the movement of the pendulum using info gathered
        with f_theta_omega
    """
    # frame_rate = 100
    # steps_per_frame = 10
    # h = 1.0/(frame_rate*steps_per_frame) # size of single step
    # for i in range(steps_per_frame):
    #     k1 = h * f_theta_omega(angles, t)
    #     k2 = h * f_theta_omega(angles + 0.5 * k1, t)
    #     k3 = h * f_theta_omega(angles + 0.5 * k2, t)
    #     k4 = h * f_theta_omega(angles + k3, t)
    #     angles += (k1 + 2 * k2, 2 * k3, k4)/6
    pass

def main():
    """
    Main method
    """


if __name__ == "__main__":
    main()
    exit(0)
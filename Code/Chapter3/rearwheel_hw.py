""" Kinematic Bicycle Model
    Written by: Kristina Miller
    For detailed reference for models see: 
    A Survey of Motion Planning and Control Techniques for Self-Driving Urban Vehicles
    Publisher: IEEE
    Url: https://ieeexplore.ieee.org/document/7490340/
    Author(s): Brian Paden ; Michal Cap ; Sze Zheng Yong ; Dmitry Yershov ; Emilio Frazzoli
"""

import numpy as np
from numpy.linalg import norm
from scipy.misc import derivative
''' needing to do this because of a matplotlib bug'''
import matplotlib as mpl
mpl.use('tkagg')
import matplotlib.pyplot as plt
from scipy.integrate import odeint

'''Vehicle parameters: 
    length and steering angle limits'''
vhcl_mdl = {'l' : 10,
			'delta_lim' : np.pi/4}

def rearwheel_model(z, t, u, l):
    '''
    Bicycle model of vehicle. z[0], z[1] Position of rear wheel in stationary coordinates.
    z[2] theta: Heading. 
    DO NOT Change this function
    u: input steering angle and velocity
    l: length of vehicle
    '''
    xr = z[0]
    yr = z[1]
    theta = z[2]

    delta = u[0]
    vr = u[1]

    dxrdt = vr*np.cos(theta)
    dyrdt = vr*np.sin(theta)
    dthetadt = (vr/l)*np.tan(delta)
    dzdt = [dxrdt, dyrdt, dthetadt]
    return dzdt


def orient(z, u, k, path, vhcl_mdl, gamma = 0.025, S = 1001):
    '''Inputs:
	   z: Current plant state
	   k: vector of control gains that can be tuned
	   path: 
	   gamma, S: parameters used by some controller, but you can ignore
	   Output to be computed: 	
	   delta: steering angle
    ''' 
    x_r = z[0] 
    y_r = z[1]
    theta = z[2]

    v_r = u[1]

    delta_max = vhcl_mdl['delta_lim']
    l = vhcl_mdl['l']
    s = np.linspace(0, 1, S)


    # Write code to calculate and output delta
    # 
    path_dir_vec = (path(s[-1]) - path(s[0]))/(norm(path(s[-1]) - path(s[0])))
    path_dir_angle = np.arctan(path_dir_vec[1]/path_dir_vec[0])
    angle_error = path_dir_angle - theta
    delta = 0.01*k*angle_error
    return delta

def another_controller(z, u, k, path, vhcl_mdl, gamma = 0.025, S = 1001):
	x_r = z[0] 
	y_r = z[1] 
	theta = z[2]

	v_r = u[1]

	# write
	return delta

 
'''Map of controller names'''
controllers = {'orient': orient,
               'another controller' : another_controller}


def path_control(z0, u0, t, cntrl, k, path, vhcl_mdl, gamma = 0.25, S = 100):	
    '''
        z0,u0: initial state, velocity
        t: time sequence for simulation
        cntr: controller to be used
    '''
    N = len(t)
    l = vhcl_mdl['l']

    '''Generate the path'''
    s = np.linspace(0, 1, S)
    x_path, y_path = path(s)

	
    '''These vectors will store the state variables of the vehicle'''     
    x = np.array([])
    y = np.array([])
    xf = np.array([])
    yf = np.array([])
    theta = np.array([])
    ''' Initialization of x, y, theta, xf, yf'''
    x = np.append(x, z0[0])
    y = np.append(y, z0[1])
    theta = np.append(theta, z0[2])
    xf = np.append(xf, x[-1] + l*np.cos(theta[-1]))
    yf = np.append(yf, y[-1] + l*np.sin(theta[-1]))

    v_r = u0[1]

    controller = controllers[cntrl]

    """ setting up the figure """
    plt.figure()

    """This loop solves the ODE for each pair of time points
    with fixed controller input"""
    for i in range(1, N):
        # The next time interval to compute the solution over
        tspan = [t[i - 1], t[i]]
        # solve ODE for next time interval with input u0 from new initial set z0
        z = odeint(rearwheel_model, z0, tspan, args=(u0, 1))
        # store solution (x,y,\theta) for plotting
        x = np.append(x, z[1][0])
        y = np.append(y, z[1][1])
        theta = np.append(theta, z[1][2])
        xf = np.append(xf, x[-1] + l*np.cos(theta[-1]))
        yf = np.append(yf, y[-1] + l*np.sin(theta[-1]))

        # next initial conditions
        z0 = z[1]
        # next controller input
        delta = controller(z0, u0, k, path, vhcl_mdl, gamma, S)
        if delta == None:
            print("Can't continue loop")
            break
        else:
            u0 = [delta, v_r]

    '''Rest of the function plots and you dont have to change anything ''' 
    plt.plot(xf, yf, '--', label = 'Front-wheel path', color='0.25',linewidth=2)
    plt.plot(x, y, '--', label = 'Rear-wheel path', color='0.5',linewidth=2)
 
    ''' plotting veicle. Line joining front and rear wheel'''
    for i in range(1, len(x), 25):
        plt.plot([x[i],xf[i]],[y[i],yf[i]], linewidth=3, color='0.8')
        #sanity check
        #vlength = np.sqrt((xf[i]-x[i])**2 + (yf[i]-y[i])**2)
        #print(vlength)

    ''' plot the starting and end points of the path'''
    plt.scatter(x[0], y[0], s = 100)
    plt.scatter(x[-1], y[-1], s = 100)

    '''plot path'''
    plt.plot(x_path, y_path, color='0', label = 'Path',linewidth=2)
    plt.legend(loc='lower right', fontsize='x-large')
    plt.tick_params(axis='both', labelsize=20)
    plt.title(cntrl)
    plt.grid()
    plt.show()

def path(s):
    ''' This function generates a 2d path as a sequence of (x,y) points
    the input s is a parameter. You can try to use other functions for 
	x and y
    '''
    x = 80*s
    y = 4*np.tanh((120*s-40)/4) + 4 
    return np.array([x, y])



''' Setup for runnint the simulation
    Thorizon: Time horizon for simulation
    Nsample: number of sample points that will be use to split [0, Thorizon]
    t will be the array of time points
'''
Nsample = 500
Thorizon = 80
t = np.linspace(0, Thorizon, Nsample)
# initial state and input
z0 = [0, -2, 0.1]
u0 = [0, 1]

# Control gains
k1 = 6   # Pure Pursuit
k2 = [0.75, 0.25] # Rearwheel Feedback
k3 = 0.5 # Frontwheel Feedback
#path_control(z0, u0, t, 'pure pursuit', k1, path, vhcl_mdl)
path_control(z0, u0, t, 'orient', k1, path, vhcl_mdl)
#path_control(z0, u0, t, 'rearwheel feedback', k2, path, vhcl_mdl)
#path_control(z0, u0, t, 'frontwheel feedback', k3, path, vhcl_mdl)


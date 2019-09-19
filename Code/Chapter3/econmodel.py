# The MIT License (MIT)

# Copyright (c) 2015 Sayan Mitra

# Permission is hereby granted, free of charge, to any person obtaining a copy of 
# this software and associated documentation files (the "Software"), to deal in the Software without restriction, 
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
# sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the 
# following conditions:

# The above copyright notice and this permission notice shall be included in all copies or 
# substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT 
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR 
# THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from scipy.integrate import odeint
import numpy as np
import pylab as pl
import scipy as sp
import grid as hr 

class ODE:
    """A simple class defining the simple economy model
    """
    
    def __init__(self,alphaval,betaval,kval,g0val,min,max):
        ''' Initializes the model parameters
        min: 2 vector defining lower bound of x and y
        max: 2 vector defning upper bound of x and y
        '''
        self.dimension = 2
        self.alpha = alphaval
        self.beta = betaval
        self.k = kval
        self.g0 = g0val
        ''' bounds for simulation and plotting'''
        self.range = hr.Hyperrect(min,max)
    
    def f(self,x,t):
        ''' Linear dynamical system model dx/dt = f(x) of a simple economy.
        This is the right hand side of the differential equation
        that is, the function f(x)
        Input:  x[0] is the national income (x)
                x[1] is the expenditure
                t is time
        Output: xd = [f(x)[0], f(x)[1]]
        '''
        xd = [[0],[0]]
        x1 = x[0]
        x2 = x[1]  
        
        ## Dynamics shifted to equilibrium for phase plot
        xd[0] = 1*x1 - self.alpha *x2
        xd[1] = self.beta*(1-k)*x1 - self.beta*x2  
        return xd   

    def vectorfield(self, gridsize):
        '''generate and plot vector field in 2d for the given dimensions
        gridsize: granularity of vectorfield
        '''
        x, y = np.meshgrid(np.linspace(self.range.ll[0],self.range.tr[0] , gridsize),
                np.linspace(self.range.ll[1], self.range.tr[1], gridsize))
        u, v = self.f([x,y],0)
        pl.quiver(x, y, u, v, color='0.75',linewidth=2)
        return

class ODESolver:
    def __init__(self,model):
        '''
        Takes and ODE object as argument
        '''
        self.dimension = model.dimension
        self.f = model.f

    def simulate(self,  InitialState,TimeSeq):
        '''
        simulates the ode for a given sequence of time points
        TimeSeq from InitialState
        '''
        StateSeq = odeint(self.f, InitialState, TimeSeq)
        return StateSeq
    
    def plotPhase(self,TimeSeq,StateSeq, dim1, dim2,LegendSeq=[]):
        '''plot phase portrait of dim1 vs dim2'''
        pl.plot(StateSeq[:,dim1],StateSeq[:,dim2],color='.2',linewidth='2')
        pl.legend(LegendSeq, loc='upper right', fontsize='x-large')

    
    def plotTraj(self,TimeSeq,StateSeq, LegendSeq=[]):
        '''plot trajectory vs time
            Input: Vector of time sequence
            and Vector of state sequence
            Vector of strings used as legend; defaults to empty
        '''
        pl.plot(TimeSeq, StateSeq,linewidth='2')
        pl.legend(LegendSeq, loc='upper right', fontsize='x-large')



## Define model parameters
alpha = 3
beta = 1.5
k = 0.1
g0 = 3
min = [-5,-5]
max = [5,5]

# Create model
model = ODE(alpha,beta,k,g0,min,max)

# Create solver for model
solver = ODESolver(model)

# Create time sequence
tseq = np.arange(0.0, 40, 0.1)

# Find solution for time sequence
sseq = solver.simulate([2,1],tseq)

# Time plot
solver.plotTraj(tseq,sseq,('income ($x$)', 'spending ($y$)', 'Lyapunov function ($V$)'))

# Uncomment the lines below for Phase plot
#solver.plotPhase(tseq,sseq,0,1,('income ($x$) vs spending ($y$)',))
#model.vectorfield(20)

pl.show()
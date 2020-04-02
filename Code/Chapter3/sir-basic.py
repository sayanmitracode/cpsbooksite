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
    """A simple class defining the basic SIR model from O. Kermack and Anderson Gray McKendrick 
        https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology
    """
    
    def __init__(self,betaval,gammaval,Nval,g0val,min,max):
        ''' Initializes the model parameters
        betaval: infection rate
        gammaval: recovery rate
        R0: basic reproductive rate
        '''
        self.dimension = 3
        self.beta = betaval
        self.gamma = gammaval
        self.N = Nval
        self.g0 = g0val
        self.R0 = self.beta/self.gamma
        ''' bounds for simulation and plotting'''
        self.range = hr.Hyperrect(min,max)
    
    def f(self,x,t):
        ''' 
        Input:  x[0] is S: stock of susceptible population (S)
                x[1] is stock of infected (I)
                x[2] is stock of recovered population (R)
                t is time
        Output: xd = [f(x)[0], f(x)[1]]
        '''
        xd = [[0],[0],[0]]
        S = x[0]
        I = x[1]
        R = x[2]  
        
        ## Dynamics shifted to equilibrium for phase plot
        xd[0] = -(self.beta * I * S )/self.N
        xd[1] = (self.beta * I * S )/self.N - self.gamma * I
        xd[2] = self.gamma * I
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
beta = 0.33
gamma = 0.17
''' values from https://towardsdatascience.com/infection-modeling-part-1-87e74645568a'''
N = 100 
I0 = 0.1
g0 = 3
min = [-5,-5]
max = [5,5]

# Create model
model = ODE(beta,gamma,N,g0,min,max)

# Create solver for model
solver = ODESolver(model)

# Create time sequence
tseq = np.arange(0.0, 100, 0.01)

# Find solution for time sequence
sseq = solver.simulate([(1-I0)*N,I0*N,0],tseq)

# Time plot
solver.plotTraj(tseq,sseq,('Susceptible ($S$)', 'Infected ($I$)', 'Recovered ($R$)'))

# Uncomment the lines below for Phase plot
#solver.plotPhase(tseq,sseq,0,1,('income ($x$) vs spending ($y$)',))
#model.vectorfield(20)

pl.show()
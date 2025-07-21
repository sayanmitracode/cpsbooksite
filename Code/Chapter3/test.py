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
import matplotlib.pyplot as pl
import scipy as sp
import grid as hr 

## Define model parameters
alpha = 3
beta = 1
k = 0
g0 = 1
min = [-5,-5]
max = [5,5]



# # Create model
# model = ODE(alpha,beta,k,g0,min,max)

# # Create solver for model
# solver = ODESolver(model)

# Create time sequence
tseq = np.arange(0.0, 40, 0.1)
pl.plot(10,10)

# Find solution for time sequence
#sseq = solver.simulate([2,1],tseq)

# Time plot
# solver.plotTraj(tseq,sseq,('income ($x$)', 'spending ($y$)', 'Lyapunov function ($V$)'))

# Uncomment the lines below for Phase plot
# solver.plotPhase(tseq,sseq,0,1,('income ($x$) vs spending ($y$)',))
# model.vectorfield(20)

# print("Eighenvalues are:")
# a = np.array([[1, 1],[-3, -1]])
# print(np.linalg.eigvalsh(a))
# print(matplotlib.__version__)
pl.show()

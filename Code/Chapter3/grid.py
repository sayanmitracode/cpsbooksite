# The MIT License (MIT)

# Copyright (c) 2019 Sayan Mitra

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

from math import ceil, floor
import itertools
import pylab as pl
from matplotlib.patches import Rectangle
import matplotlib.lines as mlines
import numpy as np


    
class Hyperrect:
    '''Class for a hyperrectangles
    Input:
    ll: n vector defining lower left corner
    tr: n vector defininf upper right corner
    constructs a hyperrectagle if the dimensions are right
    '''
    
    def __init__(self,ll,tr):
        """
        ll:lowerleft vector
        tr:topright vector
        """
        # checking if dimensions match
        if len(ll) != len(tr):
            raise ValueError('LowerLeft and TopRight vector size mismatch')
        
        # checking if ll values are leq tr values
        for j in range(0,len(ll)):
            if ll[j] > tr[j]:
                raise ValueError('LowerLeft not \leq TopRight at ' + str(j))
        
        self.ll = ll
        self.tr = tr
        self.dim = len(ll)
        self.gridsize = None
        self.gridlist = None
    
    @classmethod
           
        
    def MakeBall(cls, center, radius):
        '''Creates a hyperrectangle
        Input: 
            n vector defining center
            1 float defining radius
        Ouput: lower left and top right vectors of a hyperrectangle 
        Maybe we should make it like MakeBig
        '''
        ll = [x-radius for x in center]
        tr = [x+radius for x in center]
        return [ll, tr]
    
    def MakeBig(self,M):
        '''Change self to a hyperrectangle from [0,0,...] to [M,M,...]
        ''' 
        self.ll = [0 for x in self.ll]
        self.tr = [M for x in self.tr]
        return

    def print_function(self):
        ''' Prints the corners of the hyperrectangle and the gridding'''
        print('Hyperrectangle \n')
        print(str(self.ll) +'->'+ str(self.tr)+'\n')
        print('Gridded as \n')
        print(self.gridlist)
        
    def contains(self,x):
        "returns 1 if x \in self else returns 0"
        if len(x) != self.dim:
            raise ValueError('x and hyperrectangle dim')
        for i in range(0,self.dim):
            if x[i] > self.tr[i] or x[i] < self.ll[i]:
                return 0
        return 1
            
        
    def grid_1d(self,k,delta):
        llk = self.ll[k]
        dimrange0 = float(self.tr[k] - llk)
        A = []
        for j in range(0, int(ceil(dimrange0/delta))):
            # Sept. There was a 1 + int() in calculating the range.
            # could add 1 in the end point of the range
            A.append(llk+(delta/2) + j*delta)
        return A
    
    def grid_all(self,delta):
        "initializes the hyperrectangle with a grid"
        L = [self.grid_1d(0, delta)]
        for i in range(1,self.dim):
            L.append( self.grid_1d(i, delta))
        self.gridlist = L
        self.gridsize = delta
        return L
     
    def grid(self,delta):
        "May make sense to use grid_all instead of this function"
        L = self.grid_all(delta)
        # print(L)
        G=[]
        for element in itertools.product(*L):
            G.append( element)
        return G
    
    def quantize(self,x):
        """Call this after calling grid_all on hyperrectangle
            returns quantized version of x
        """
        if len(x) != self.dim:
            raise ValueError('x and hyperrectangle dim')
        if self.gridlist == None:
            raise ValueError('hyperrectangle not gridded')
        if not self.contains(x):
            raise ValueError('hyperrectangle does not contain x')
        L = self.gridlist
        q = np.zeros((self.dim))
        for j in range(0,self.dim):
            # Previously quantization used the lowest value in the interval as the quantization point
            # pick point from quantized list
            for xj in range(0,len(L[j])):
                if ((L[j][xj] - self.gridsize/2 <= x[j]) & (x[j] < L[j][xj] + self.gridsize/2)):
                    q[j] = L[j][xj]
                    break;
                ## q.append(L[j][xj])
##            xj = int(floor((x[j]-self.ll[j])/self.gridsize)) # ceil should also work
            # Now we will use the mid point
            #for kk in range(1,len(L[j])):
             #   if (L[j][kk] >= x[j]):
             #       qxj = (L[j][kk] + L[j][kk-1] )/2
              #      print(qxj)
 ##           if (L[j][xj]==x[j]):
 ##               q.append(L[j][xj])
 ##           else:
 ##               q.append((L[j][xj]+L[j][xj+1])/2)
        return q  
    
    def grid_plot(self):
        """plots a rectangle its grid, the input point x, and the quantized point q
        only works for two dimensional things"""
        if (self.dim != 2):
            print("Cannot plot grids for dimensions != 2")
            return
        currentAxis = pl.gca()
        # draw the whole hyperrectangle
        currentAxis.add_patch(Rectangle((self.ll),self.tr[0]-self.ll[0],self.tr[1]-self.ll[1],fill=False))
        # draw the grid
        for xi in range(0,len(self.gridlist[0])-1):
                for yj in range(0,len(self.gridlist[1])-1):
                    #pl.plot([self.gridlist[0][xi]],[self.gridlist[1][yj]],'o',color='0.75',ms=3,markeredgewidth=None)
                    currentAxis.add_patch(Rectangle((self.gridlist[0][xi]-self.gridsize/2,self.gridlist[1][yj]-self.gridsize/2),self.gridsize,self.gridsize,fill=False,linestyle='dotted'))
                    #
                    # print(str([self.gridlist[0][xi],self.gridlist[1][yj]]))
     
        

# some code for testing the above functions
#  
# R = Hyperrect([3,1],[9,4])
# R.print_function()
# R.grid_all(.5)
# R.print_function()
# #c = [5,5]
# #B = Hyperrect.MakeBall(c, 10)
# #print(B)
# x = [3,2.9]
# q = R.quantize(x)
# # print ("point = " + str(x))
# # print ("quantized point = " + str(q))
# # pl.axis([2,10,0,5])
# #R.grid_plot()
# #pl.plot([x[0]],[x[1]],'ro')
# #pl.plot([q[0]],[q[1]],'go')
# #pl.show()

# #####################

# #print (Hyperrect.MakeBall(q,.1))
# #A0 =  R.grid_1d(0,0.5)
# #A1 =  R.grid_1d(1,0.5)
# #L = R.grid_all(1)
# #print(L)
# #L = R.grid(.1)
# #print(L)

# #for element in itertools.product(*L):
# #    print (element)

## 
R = Hyperrect([3,1],[4,2])
R.print_function()
R.MakeBig(1000)
R.print_function()
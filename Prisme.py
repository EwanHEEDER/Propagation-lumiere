#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 09:53:59 2021

@author: ewanheeder
"""

import numpy as np

import matplotlib.pyplot as plt

def f(x1, x2, y3):
    
    x3 = (x1 + x2)/2
    
    a1 = (2 * y3)/(x2 - x1)
    
    b1 =-2 * x1 * y3/(x2 - x1) #par tan
    
    a2 = (2 * y3)/(x1 - x2)
    
    b2 = 2 * y3 * x2/(x2 - x1)  #Thalês le 100


    x = np.linspace(x1,x2)
    
    fig=plt.figure()
    
    ax = fig.add_subplot(111)
    
    plt.plot(x, a1 * x + b1, 'b')
    plt.plot(x, a2 * x + b2, 'r')
    plt.hlines(0,x1, x2)
    
    plt.xlim(0,10)
    plt.ylim(0,10)
    ax.set_aspect('equal')
    
    
f(1,3,5)
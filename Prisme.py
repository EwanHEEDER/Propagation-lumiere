import numpy as np

import matplotlib.pyplot as plt

def prisme(dictionnaire):
    
    x1 = dictionnaire["Prisme"][0]
    x2 = dictionnaire["Prisme"][1]
    y3 = dictionnaire["Prisme"][2]
    
    """Prisme isocèle"""
    
    a1 = (2 * y3)/(x2 - x1)
    
    b1 =-2 * x1 * y3/(x2 - x1) #par tan
    
    a2 = (2 * y3)/(x1 - x2)
    
    b2 = 2 * y3 * x2/(x2 - x1)  #Thalês le 100


    x = np.linspace(x1,x2)
    
    #fig=plt.figure()
    
    #ax = fig.add_subplot(111)
   
    eq1 = a1 * x + b1
    eq2 = a2 * x + b2
    
    def f1(x):
        return a1 * x + b1
   
    def f2(x):
        return a2 * x + b2
    
    
#   plt.plot(x[eq1<=y3], eq1[eq1<=y3], 'b')
#   plt.plot(x[eq2<=y3], eq2[eq2<=y3], 'r')
#   plt.hlines(0,x1, x2)
    
#   plt.xlim(0,10)
#   plt.ylim(0,10)
#   ax.set_aspect('equal')
    
    return f1, f2

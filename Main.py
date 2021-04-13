#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 15:04:09 2021

@author: ewanheeder
"""

"""Indexation:
    
    v[a,b,c]: a:[0, tot_trajec]; Point considéré
              b:{0,1}; vecteur position ou dérivée du vecteur position
              c: {0,1}; Coordonnée du vecteur considéré"""



import numpy as np
import matplotlib.pyplot as plt





from Indice import n_grad, n_interface
from Résolution_equation_mouvement import dérivée, RK4

ds = 1 #km

tot_trajec = 200



theta = np.pi/10

# Interface eau/air


v_ini = np.array([[0,0],[np.cos(theta),np.sin(theta)]])

s, v = RK4(tot_trajec, ds,v_ini,dérivée, n_grad,ds)

plt.plot(v[:,0,0],v[:,0,1])
plt.xlabel("X")
plt.ylabel("Y")
#plt.axvline(150, color = 'black')
print(s)
print(v[:,0,0])


###Problème entre abscisse et abscisse curviligne: on atteint des abscisses et ordonnées normalement impossibles
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 09:17:24 2021

@author: ewanheeder
"""
import numpy as np

ds = 1 #km


def dérivée(u_prec, u, s, n):
    
    # u est un tuple (r, dr/ds). /!\ r et dr/dt sont des vecteurs
    
    du = np.empty(np.shape(u))
    
    dn = n(u[0]) - n(u_prec[0]) #Problème
    
    dx = u[0,0] - u_prec[0,0] #Problème aussi
    
    dy = u[0,1] - u_prec[0,1]
    
    grad_n = (dn/dx) * np.array([1,0]) + (dn/dy) * np.array([0,1])
    
    #print("grad_n =", grad_n)
    
    du[0] = u[1]
    du[1] = grad_n - dn/ds * u[1]
    
    return du # une liste , (dr/ds, d^2(r) / ds^2)

def RK4(tot_trajec, step, v_ini, derive, n):

    # Création du tableau d'abscisse curviligne
    
    num_points = int(tot_trajec / step) + 1     # nombre d'éléments
    s = np.linspace(0, tot_trajec, num_points)    # tableau d'abscisse curviligne, on commence obligatoirement à 0

    # initialisation du tableau v, à 3 dimensions: Pour chaque pas --> deux vecteurs de dimension 2
    v = np.empty((num_points,2,2))
    


    # condition initiale
    v[0] = v_ini 
    v[1] = v_ini[0] + ds * v_ini[1]

    # boucle for
    
    for i in range(2,num_points):
        print("i = ", i)
        
        print("x[i-2] = ", v[i-2,0,0])
        
        print("x[i-1] = ", v[i-1,0,0])
        
        print("dx = ",v[i-1,0,0] - v[i-2, 0, 0])
        
        
        
        
        #On change la fonction utilisée pour le calcul de dérivée
        
        d1 = np.array(derive(v[i-2],v[i-1], s[i-2], n))
        
        d2 = np.array(derive(v[i-2],v[i-1] + d1 * step/2, s[i-1] + step/2, n))
        
        d3 = np.array(derive(v[i-2],v[i-1] + d2 * step/2, s[i-1] + step/2, n))
        
        d4 = np.array(derive(v[i-2],v[i-1] + d3 * step, s[i-1] + step, n))
        
        v[i] = v[i-1] + (d1 + 2 * d2 + 2 * d3 + d4) * step / 6
        
        
   
    # argument de sortie
    return s , v

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 09:20:23 2021

@author: ewanheeder
"""

def n_grad(position, n1 = 1.000157, n2 = 1.0, hauteur = 1000):
    
    if position[1] <= hauteur:
        
        delta_n =n2 - n1
    
        return (delta_n / hauteur) * position[1] + n1
    
    else:
        
        return n2



def n_interface(position, dioptre = 150, n1 = 1., n2 = 2):
    
    if position[0]< 150:
        n=n1
    else:
        n=n2
    return n


def n_prisme(position, Lambda, n1, nD = 1.72, VD = 29.3): #Possible changer verre. Par défaut --> Crown C

    """ Input: position = Vecteur position (x,y)
               Lambda = longueur donde du rayon (nm)
               n1 = Indice du milieu dans lequel se trouve le prisme
               nd, vd = paramètres du verre; indice pour la raie de référence D & nombre d'Abbe du verre"""
    if position>=2:
        
        lC=656.3
        lD=589.3
        lF=486.1
        
        B = (nD-1)/(VD*(1/(lF*lF)-1/(lC*lC)))
        A=nD - B/(lD*lD)
        
        n = A + B/(Lambda**2)
        
        return n
        
    else:
        
        return n1
        
        
print(n_prisme(3,420,1.0))
    
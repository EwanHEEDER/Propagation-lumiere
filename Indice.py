#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 09:20:23 2021

@author: ewanheeder
"""


def n_grad(position, n1 = 1.000157, n2 = 1.0, largeur = 1000):
    
    if position[0] <= largeur:
        
        delta_n =n2 - n1
    
        return (delta_n / largeur) * position[0] + n1
    
    else:
        
        return n2



def n_interface(position, dioptre = 150, n1 = 1., n2 = 2):
    
    if position[0]< 150:
        n=n1
    else:
        n=n2
    return n
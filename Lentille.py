#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 14:22:14 2021

@author: ewanheeder
"""

#Ce programme sert à calculer un grand nombre de trajectoires pour observer la 
#lentille gravitationnelle. Les données sont rassemblées dans 'lentille.csv' pour
#épargner le temps de calcul. Il n'a donc pas besoin d'être exécuté


import numpy as np
import tqdm
import matplotlib.pyplot as plt

from numpy import asarray
from numpy import savetxt


from Indice import n_amas
from Resolution_equation_mouvement import dérivée_3D, RK4_3D
from Modeles import propagation_grav
from Main import opti_grav

nombre_angles = 10000
angles = np.linspace(0,2*np.pi, nombre_angles)    #théta

plt.figure()

lentille = np.empty((nombre_angles, 2))

for i in tqdm.tqdm(range(nombre_angles)):
    
    opti_grav["Angle initial en 3D"][0] = angles[i]
    
    s,v,indices = RK4_3D(opti_grav)
    
    indice = np.argmin(np.abs(v[:, 0, 2]))

    lentille[i, 0] = v[indice,0,0]
    lentille[i, 1] = v[indice,0,1]

    
savetxt('lentille.csv', lentille, delimiter = ',')

plt.scatter(lentille[:,0], lentille[:,1])

    
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 13:54:53 2021

@author: ewanheeder
"""
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cmx
import tqdm

from Resolution_equation_mouvement import dérivée, RK4, dérivée_3D, RK4_3D
from Indice import n_grad, n_interface, n_prisme
from Prisme import prisme

def propagation_grad(dictionnaire):
    
    #Sécurité
    dictionnaire["Calcul d'indice"] = n_grad
    
    
    v_ini = np.array([dictionnaire["Position initiale"],
                      [np.cos(dictionnaire["Angle initial"]),np.sin(dictionnaire["Angle initial"])]])
    
    s, v = RK4(dictionnaire)
    
    masque = v[:,0,1] >= 0
    x = v[:,0,0][masque]
    y = v[:,0,1][masque]
    
    
#    fig = plt.figure(figsize = (10,10), dpi = 1200)
    fig = plt.figure(figsize = (10,10))
    
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')

    plt.plot(x,y)
    
    #Pour mettre en évidence le mirage
    
    v = v[masque]
    
    plt.plot(x,(1/v[-1,1,0]) * (v[-1,1,1] *  x - v[-1,0,0] * v[-1,1,1] + v[-1,0,1] * v[-1,1,0]))
    
    plt.xlim(0,x[-1] +5)
    plt.ylim(0,x[-1] +5)
    
    plt.xlabel("X (en m)")
    plt.ylabel("Y (en m)")
    plt.title("Trajet d'un rayon lumineux émis d'une hauteur h = " + str(v_ini[0,1]) + " m,"+ "\n" +
          "avec un angle de " + "{0:.2e}".format(dictionnaire["Angle initial"]) + " rad")
    
    plt.text(x[-1]/2, 1, "n1 = " + str(dictionnaire["Indice 1 gradient"]),fontsize = 'large')
    plt.text(x[-1]/2, x[-1] , "À h = " + str(dictionnaire["Hauteur du gradient"])+
             "m, n2 = " + str(dictionnaire["Indice 1 gradient"]),fontsize = 'large')
    
    return v

def propagation_interface(dictionnaire):
    
    #Sécurité
    dictionnaire["Calcul d'indice"] = n_interface
    
    
    dioptre = dictionnaire["Position dioptre"]
    n1 = dictionnaire["Indice 1 interface"]
    n2 = dictionnaire["Indice 2 interface"]
    
    v_ini = np.array([dictionnaire["Position initiale"],
                      [np.cos(dictionnaire["Angle initial"]),np.sin(dictionnaire["Angle initial"])]])
    
    s, v = RK4(dictionnaire)
    
    masque = v[:,0,1] >= 0
    x = v[:,0,0][masque]
    y = v[:,0,1][masque]
    
 #   fig = plt.figure(figsize = (10,10), dpi = 1200)
    fig = plt.figure(figsize = (10,10))

    
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    
    plt.plot(x,y)
    
    plt.xlim(0,10)
    plt.ylim(0,10)
    
    plt.axvline(dioptre, color = 'black')
    
    plt.xlabel("X (en m)")
    plt.ylabel("Y (en m)")
    plt.title("Trajet d'un rayon lumineux à l'interface entre un milieu d'indice n1 = " + str(n1) + "\n"+ 
              "et un milieu d'indice n2 = " +str(n2) + "\n" + "avec un angle initiale de "+
               str("%.3f"%dictionnaire["Angle initial"]) + " rad")
    
    normale = dioptre * np.tan(dictionnaire["Angle initial"])
    
    vecteur = v[-1,1,:]
    
    plt.axhline(normale,linestyle = '--', color = 'orange')
    plt.text(1, 9, "n1 sin(i1) = " + str("%.3f"%(n1 * v_ini[1,1])) + "\n" + "n2 sin(i2) = " + 
             str("%.3f"%(n2 * (vecteur[1]/np.linalg.norm(vecteur)))), fontsize = 'xx-large')
    
    return v
    
def propagation_prisme(dictionnaire):
    
    #Sécurité
    dictionnaire["Calcul d'indice"] = n_prisme
    
    f1, f2 = prisme(dictionnaire)
    contours = np.linspace(dictionnaire["Prisme"][0],dictionnaire["Prisme"][1])
    
    fig=plt.figure(figsize = (10,10), dpi = 1200)
    
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    
    eq1 = f1(contours)
    eq2 = f2(contours)
    
    plt.plot(contours[eq1<=dictionnaire["Prisme"][2]], eq1[eq1<=dictionnaire["Prisme"][2]], 'black')
    plt.plot(contours[eq2<=dictionnaire["Prisme"][2]], eq2[eq2<=dictionnaire["Prisme"][2]], 'black')
    
    plt.hlines(0,dictionnaire["Prisme"][0], dictionnaire["Prisme"][1], color = 'black')
    
    
    s, v = RK4(dictionnaire)
    
    masque = v[:,0,1] >= 0
    x = v[:,0,0][masque]
    y = v[:,0,1][masque]
    
    
    plt.plot(x,y,color = 'MediumSpringGreen', 
             label = "lambda = " +str(dictionnaire["Lambda"])+ " nm")
    plt.legend()
    plt.title("Trajectoire d'un rayon lumineux à travers un prisme" + "\n"+
              "(nD = " + str(dictionnaire["Verre"][0]) + ", VD = " + str(dictionnaire["Verre"][1]) +")" )
    
    plt.xlabel("X (en m)")
    plt.ylabel("Y (en m)")
    

def faisceau_prisme(dictionnaire):
    
     #Sécurité
    dictionnaire["Calcul d'indice"] = n_prisme
    
    wavelength = np.linspace(380,780, dictionnaire["Nombre lambda"])

    colors = [cmx.rainbow(i) for i in np.linspace(0, 1, len(wavelength))]
    
    f1, f2 = prisme(dictionnaire)
    contours = np.linspace(dictionnaire["Prisme"][0],dictionnaire["Prisme"][1])
    
    fig = plt.figure(figsize = (7,7))
    
    ax = fig.add_subplot(111)
    
    eq1 = f1(contours)
    eq2 = f2(contours)
    
    plt.plot(contours[eq1<=dictionnaire["Prisme"][2]], eq1[eq1<=dictionnaire["Prisme"][2]], 'white')
    plt.plot(contours[eq2<=dictionnaire["Prisme"][2]], eq2[eq2<=dictionnaire["Prisme"][2]], 'white')
    plt.plot((dictionnaire["Prisme"][0]+dictionnaire["Prisme"][1])/2, dictionnaire["Prisme"][2], 'white')
    
    plt.hlines(0,dictionnaire["Prisme"][0], dictionnaire["Prisme"][1], color = 'white')
    
    ax.set_aspect('equal')
    ax.set_facecolor('black')
    
    for i in tqdm.tqdm(range(wavelength.size)):
        
        dictionnaire["Lambda"] = wavelength[i]
    
        s, v = RK4(dictionnaire)

        masque = v[:,0,1] >= 0

        x = v[:,0,0][masque]

        y = v[:,0,1][masque]


        plt.plot(x,y,'.', markersize = 2.5, color = colors[i])
    
 #       print("i = ", i , "sur ", wavelength.size - 1) --> tqdm plus pratique
        
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.title("Dispersion d'un faisceau lumineux de " 
              + str(dictionnaire["Nombre lambda"]) + " longueurs d'ondes à travers un prisme"+
              "\n"+ "(nD = " + str(dictionnaire["Verre"][0]) + ", VD = " + str(dictionnaire["Verre"][1]) +")")
    
    plt.xlim(0,15)
    plt.ylim(0,15)

def propagation_grav(dictionnaire):
    
    s,v, indices = RK4_3D(dictionnaire)

    masque_v = v[:,0,2] < 0
    masque_indice = indices < 1000
    
    
    indices = indices[masque_v & masque_indice]
    v = v[masque_v & masque_indice]
    
    plt.figure(figsize = (5,5))
    ax = plt.axes(projection='3d')
    
    ax.plot3D(v[:,0,0], v[:,0,1], v[:,0,2], 'gray')
    
    xdata, ydata, zdata = dictionnaire["Position centre galaxie"]
    ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='summer')
    
    x,y,z = dictionnaire["Position centre amas"]
    
    
    ax.scatter3D(x, y, z, c=z, cmap='gnuplot')
    
    ax.scatter3D(0,0,0, s = 80)
    
    
    
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    
    
    
    ax.set_xlim(-1e17, 1e17)
    ax.set_ylim(-1e17, 1e17)
    ax.set_zlim(-1e22, 1e21)
    
    
    
    plt.figure()
    
    plt.scatter(np.linalg.norm(v[:,0] - [0, 0, -1e22/2], axis = 1), indices)
    

def multi_propagation_grav(dictionnaire):
    
    nombre_angles = dictionnaire["Nombre d'angles"]
    angles = np.linspace(0,2*np.pi, nombre_angles)    #théta
    ds = dictionnaire["Pas d'intégration"]
    
    plt.figure(1)
        
    ax = plt.axes(projection='3d')
    
    for i in tqdm.tqdm(range(nombre_angles)):
        
        dictionnaire["Angle initial en 3D"][0] = angles[i]
        
        s,v,indices = RK4_3D(dictionnaire)
        
        masque = v[:,0,2] <= ds/2 
        
        v = v[masque]
        
    
        
        ax.plot3D(v[:,0,0], v[:,0,1], v[:,0,2], 'gray')
        
        xdata, ydata, zdata = dictionnaire["Position centre galaxie"]
        ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='summer')
        
        x,y,z = dictionnaire["Position centre amas"]
        
        
        ax.scatter3D(x, y, z, c=z, cmap='gnuplot')
        
        ax.scatter3D(0,0,0, s = 80)
        
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        
        
        
    ax.set_xlim(-5e16, 5e16)
    ax.set_ylim(-5e16, 5e16)
    ax.set_zlim(-1e22, 1e21)
        
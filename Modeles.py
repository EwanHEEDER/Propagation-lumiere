#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 13:54:53 2021

@author: ewanheeder
"""
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cmx

from Resolution_equation_mouvement import dérivée, RK4
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
    
    
    fig = plt.figure(figsize = (10,10), dpi = 1200)
    
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
    
    fig = plt.figure(figsize = (10,10), dpi = 1200)
    
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
    
    fig = plt.figure(figsize = (10,10), dpi = 1200)
    
    ax = fig.add_subplot(111)
    
    eq1 = f1(contours)
    eq2 = f2(contours)
    
    plt.plot(contours[eq1<=dictionnaire["Prisme"][2]], eq1[eq1<=dictionnaire["Prisme"][2]], 'white')
    plt.plot(contours[eq2<=dictionnaire["Prisme"][2]], eq2[eq2<=dictionnaire["Prisme"][2]], 'white')
    
    plt.hlines(0,dictionnaire["Prisme"][0], dictionnaire["Prisme"][1], color = 'white')
    
    ax.set_aspect('equal')
    ax.set_facecolor('black')
    
    for i in range(wavelength.size):
        
        dictionnaire["Lambda"] = wavelength[i]
    
        s, v = RK4(dictionnaire)

        masque = v[:,0,1] >= 0

        x = v[:,0,0][masque]

        y = v[:,0,1][masque]


        plt.plot(x,y,'.', markersize = 2.5, color = colors[i])
    
        print("i = ", i , "sur ", wavelength.size - 1)
        
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.title("Dispersion d'un faisceau lumineux de " 
              + str(dictionnaire["Nombre lambda"]) + " longueurs d'ondes à travers un prisme"+
              "\n"+ "(nD = " + str(dictionnaire["Verre"][0]) + ", VD = " + str(dictionnaire["Verre"][1]) +")")
    
    plt.xlim(0,15)
    plt.ylim(0,15)

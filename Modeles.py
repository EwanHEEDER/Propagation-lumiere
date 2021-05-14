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
from scipy.optimize import curve_fit

from Resolution_equation_mouvement import dérivée, RK4, dérivée_3D, RK4_3D
from Indice import n_grad, n_interface, n_prisme
from Prisme import prisme


def propagation_grad(dictionnaire):
    
    #calcul des trajectoires
    
   
    
    s, v = RK4(dictionnaire)
    
    masque = v[:,0,1] >= 0
    x = v[:,0,0][masque]
    y = v[:,0,1][masque]
    
    #Figure
    
    fig = plt.figure(figsize = (10,10))
    
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')

    plt.plot(x,y)
    
    #Pour mettre en évidence le mirage, on trace la trajectoire apparente
    
    v = v[masque]
    
    v_ini = np.array([dictionnaire["Position initiale"],
                      [np.cos(dictionnaire["Angle initial"]),np.sin(dictionnaire["Angle initial"])]])
    
    plt.plot(x,(1/v[-1,1,0]) * (v[-1,1,1] *  x - v[-1,0,0] * v[-1,1,1] + v[-1,0,1] * v[-1,1,0]),
             label = 'Trajectoire apparente')
    
    plt.xlim(0,x[-1] +5)
    plt.ylim(0,x[-1] +5)
    
    plt.xlabel("X (en m)")
    plt.ylabel("Y (en m)")
    plt.title("Trajet d'un rayon lumineux émis d'une hauteur h = " + str(v_ini[0,1]) + " m,"+ "\n" +
          "avec un angle de " + "{0:.2e}".format(dictionnaire["Angle initial"]) + " rad")
    
    plt.legend(loc = 'upper left')
    
    plt.text(x[-1]/2, 1, "n1 = " + str(dictionnaire["Indice 1 gradient"]),fontsize = 'large')
    plt.text(x[-1]/2, x[-1] , "À h = " + str(dictionnaire["Hauteur du gradient"])+
             "m, n2 = " + str(dictionnaire["Indice 1 gradient"]),fontsize = 'large')
    
    return v

def propagation_interface(dictionnaire):
    
    
    dioptre = dictionnaire["Position dioptre"]
    n1 = dictionnaire["Indice 1 interface"]
    n2 = dictionnaire["Indice 2 interface"]
    
    
    s, v = RK4(dictionnaire)
    
    masque = v[:,0,1] >= 0
    x = v[:,0,0][masque]
    y = v[:,0,1][masque]
    
    
    #Plot trajectoire
    
    fig = plt.figure(figsize = (10,10))
    
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    
    plt.plot(x,y)
    
    plt.xlim(0,10)
    plt.ylim(0,10)
    
    plt.axvline(dioptre, color = 'black')
    
    #Trajectoire sans déviation
    
    masque_th = v[:,0,0] <= dioptre
    v_th = v[masque_th]
    
    x_th = v[:,0,0][~masque_th]
    
    plt.plot(x_th,(1/v_th[0,1,0]) * (v_th[0,1,1] *  x_th - v_th[0,0,0] * v_th[0,1,1] + v_th[0,0,1] * v_th[0,1,0]),
             '.', markersize = 0.5, color = 'red', label = 'Trajectoire en absence de déviation')
    
    
    plt.xlabel("X (en cm)")
    plt.ylabel("Y (en cm)")
    plt.title("Trajet d'un rayon lumineux à l'interface entre un milieu d'indice n1 = " + str(n1) + "\n"+ 
              "et un milieu d'indice n2 = " +str(n2) + "\n" + "avec un angle initiale de "+
               str("%.3f"%dictionnaire["Angle initial"]) + " rad")
    plt.legend()
    
    
    
    #Loi de Snell-Descartes
    
    normale = dioptre * np.tan(dictionnaire["Angle initial"])
    
    vecteur = v[-1,1,:]
    
    plt.axhline(normale,linestyle = '--', color = 'orange')
    
    v_ini = np.array([dictionnaire["Position initiale"],
                      [np.cos(dictionnaire["Angle initial"]),np.sin(dictionnaire["Angle initial"])]])
    plt.text(6, 1, "n1 sin(i1) = " + str("%.3f"%(n1 * v_ini[1,1])) + "\n" + "n2 sin(i2) = " + 
             str("%.3f"%(n2 * (vecteur[1]/np.linalg.norm(vecteur)))), fontsize = 'large')
    
    return v
    
def propagation_prisme(dictionnaire):
    
    #Parois du prisme
    
    f1, f2 = prisme(dictionnaire)
    contours = np.linspace(dictionnaire["Prisme"][0],dictionnaire["Prisme"][1]) 
    
    fig=plt.figure(figsize = (10,10))
    
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    
    eq1 = f1(contours)
    eq2 = f2(contours)
    
    plt.plot(contours[eq1<=dictionnaire["Prisme"][2]], eq1[eq1<=dictionnaire["Prisme"][2]], 'black')
    plt.plot(contours[eq2<=dictionnaire["Prisme"][2]], eq2[eq2<=dictionnaire["Prisme"][2]], 'black')
    
    plt.hlines(0,dictionnaire["Prisme"][0], dictionnaire["Prisme"][1], color = 'black')
    
    #Trajectoires
    
    s, v = RK4(dictionnaire)
    
    masque = v[:,0,1] >= 0
    x = v[:,0,0][masque]
    y = v[:,0,1][masque]
    
    #Plot
    
    plt.plot(x,y,color = 'MediumSpringGreen', 
             label = "lambda = " +str(dictionnaire["Lambda"])+ " nm")
    plt.legend()
    plt.title("Trajectoire d'un rayon lumineux à travers un prisme" + "\n"+
              "(nD = " + str(dictionnaire["Verre"][0]) + ", VD = " + str(dictionnaire["Verre"][1]) +")" )
    
    plt.xlabel("X (en cm)")
    plt.ylabel("Y (en cm)")
    

def faisceau_prisme(dictionnaire):
    
    #tableau de longueurs d'onde
    wavelength = np.linspace(380,780, dictionnaire["Nombre lambda"])

    #Liste des couleurs associées aux lambda
    colors = [cmx.rainbow(i) for i in np.linspace(0, 1, len(wavelength))]
    
    #Parois du prisme
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
    
    #calcul de trajectoire pour chaque lambda
    
    for i in tqdm.tqdm(range(wavelength.size)):
        
        dictionnaire["Lambda"] = wavelength[i]
    
        s, v = RK4(dictionnaire)

        masque = v[:,0,1] >= 0

        x = v[:,0,0][masque]

        y = v[:,0,1][masque]


        plt.plot(x,y,'.', markersize = 2.5, color = colors[i])
    
        
    #Plot (pink floyd)
    plt.xlabel("X (cm)")
    plt.ylabel("Y (cm)")
    plt.title("Dispersion d'un faisceau lumineux de " 
              + str(dictionnaire["Nombre lambda"]) + " longueurs d'ondes à travers un prisme"+
              "\n"+ "(nD = " + str(dictionnaire["Verre"][0]) + ", VD = " + 
              str(dictionnaire["Verre"][1]) +")")
    
    plt.xlim(0,15)
    plt.ylim(0,15)

def propagation_grav(dictionnaire):
    
    #Calcul de la trajectoire
    
    s,v, indices = RK4_3D(dictionnaire)
    
    #Retrait des rayons qui dépassent la Terre et des indices optiques aberrant

    masque_v = v[:,0,2] < 0
    masque_indice = indices < 1000
    
    
    indices = indices[masque_v & masque_indice]
    v = v[masque_v & masque_indice]
    
    #Plot de la trajectoire en 3D
    
    plt.figure(figsize = (5,5))
    ax = plt.axes(projection='3d')
    
    ax.plot3D(v[:,0,0], v[:,0,1], v[:,0,2], 'gray')
    
    
    
    xdata, ydata, zdata = dictionnaire["Position centre galaxie"]
    ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='summer', label = 'Galaxie')
    
    x,y,z = dictionnaire["Position trou noir"]
    ax.scatter3D(x, y, z, c=z, cmap='gnuplot', label = 'Trou noir')
    
    ax.scatter3D(0,0,0, label = "Terre")
    
    
    ax.set_xlabel('X axis (m)')
    ax.set_ylabel('Y axis (m)')
    ax.set_zlabel('Z axis (m)')
    
    plt.title("Trajet d'un rayon lumineux depuis une galaxie située à " + 
              str("{:.1e}".format(np.linalg.norm([xdata, ydata, zdata]))) + " m de la Terre")
    plt.legend()
    
    
    
    ax.set_xlim(-1e17, 1e17)
    ax.set_ylim(-1e17, 1e17)
    ax.set_zlim(-1e22, 1e21)
    
      
    # Plot de n(r)
    
    plt.figure()
    
    plt.scatter(np.linalg.norm(v[:,0] - [0, 0, -1e22/2], axis = 1), indices)
    
    plt.xlabel("r (m)")
    plt.ylabel("n")
    
    plt.title("Évolution de l'indice optique en fonction de la distance au centre du trou noir")
    


def multi_propagation_grav(dictionnaire):
    
    
    #Nombre de rayons partant de la galaxie 
    nombre_angles = dictionnaire["Nombre d'angles"]   
    
    #tableau de valeurs de théta
    angles = np.linspace(0,2*np.pi, nombre_angles) 
    
    
    ds = dictionnaire["Pas d'intégration"]
    
    #Plot
    
    plt.figure()    
    ax = plt.axes(projection='3d')
    
    #Ajout de la Terre, du trou noir et de la galaxie d'origine
        
    xdata, ydata, zdata = dictionnaire["Position centre galaxie"]    
    ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='summer', label = 'Galaxie')
        
    x,y,z = dictionnaire["Position trou noir"]    
    ax.scatter3D(x, y, z, c=z, cmap='gnuplot', label = 'Trou noir')
        
    ax.scatter3D(0,0,0, label = "Terre") 
    
    #Calcul de trajectoire pour chaque angle initial
    
    for i in tqdm.tqdm(range(nombre_angles)):
        
        #Changement de l'angle initial dans le dictionnaire utilisé
        
        dictionnaire["Angle initial en 3D"][0] = angles[i]      
        
        s,v,indices = RK4_3D(dictionnaire)                      
        masque = v[:,0,2] <= ds/2         
        
        v = v[masque]                            
        
        ax.plot3D(v[:,0,0], v[:,0,1], v[:,0,2], 'gray')
    
    
    ax.set_xlabel('X axis (m)')        
    ax.set_ylabel('Y axis (m)')       
    ax.set_zlabel('Z axis (m)')
    
    plt.title("Trajet de " + str(nombre_angles) +" rayons lumineux depuis une galaxie située à " + 
              str("{:.1e}".format(np.linalg.norm([xdata, ydata, zdata]))) + " m de la Terre")
   
    plt.legend()
        
        
        
        
    ax.set_xlim(-5e16, 5e16)
    ax.set_ylim(-5e16, 5e16)
    ax.set_zlim(-1e22, 1e21)
    
    
        
def lentille_grav():
    
    m_S = 1.988e30 #kg
    
    #Récupération des données
    lentille = np.genfromtxt('lentille.csv', delimiter = ',')
    
    #Plot

    fig=plt.figure(figsize = (10,10))
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    ax.set_facecolor('black')
    
    plt.plot(lentille[:,0], lentille[:,1], 'white')
    
    plt.xlabel('X axis (m)')
    plt.ylabel('Y axis (m)')
    plt.title("Effet de lentille gravitationnelle provoqué par un trou noir de masse m = " + 
              str("{:.2e}".format(4e16*m_S))+ " kg " + "\n"+ " et de rayon R = " + 
              str("{:.2e}".format(1e15)))
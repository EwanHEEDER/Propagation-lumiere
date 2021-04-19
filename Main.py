"""Indexation:
    
    v[a,b,c]: a:[0, tot_trajec]; Point considéré
              b:{0,1}; vecteur position ou dérivée du vecteur position
              c: {0,1}; Coordonnée du vecteur considéré"""



import numpy as np
import matplotlib.pyplot as plt



from Indice import n_grad, n_interface, n_prisme
from Résolution_equation_mouvement import dérivée, RK4
from Prisme import prisme
from Mvt_prisme import dérivée_prisme, RK4_prisme


paramètres = {"Pas d'intégration": 1,               #en km
              "Longueur du trajet": 400,            #abscisse curviligne, en km
              "Angle initial": np.pi/100000,        #angle avec l'horizontale, en rad
              "Fonction dérivée": dérivée_prisme,          #fonction utilisée pour le calcul de dérivée
              "Pas de calcul du gradient": 0.5,
              "Indice en dehors prisme": 1.0,
              "lambda": 477,                         #nm
              "Calcul d'indice": n_prisme}



v_ini = np.array([[0,1.50e-3],[np.cos(paramètres["Angle initial"]),np.sin(paramètres["Angle initial"])]])

s, v = RK4_prisme(paramètres["Longueur du trajet"], paramètres["Pas d'intégration"],v_ini,
           paramètres["Fonction dérivée"], paramètres["Calcul d'indice"],
           paramètres["Pas de calcul du gradient"], paramètres["lambda"], 
           paramètres["Indice en dehors prisme"])


masque = v[:,0,1] >= 0

x = v[:,0,0][masque]

y = v[:,0,1][masque]

plt.figure(dpi = 600)
plt.plot(x,y)
plt.xlabel("X (en km)")
plt.ylabel("Y (en km)")
plt.title("Trajet d'un rayon lumineux émis d'une hauteur h = " + str(v_ini[0,1]) +
          "m , avec un angle de " + "{0:.2e}".format(paramètres["Angle initial"]) + " rad")
#plt.xlim(0,40100)
#plt.ylim(0, 100)
#plt.hlines(0, color = 'brown')
#plt.axvline(150, color = 'black')
print(v[-1,0,1])
plt.plot(x, v[-1,1,1] * v[-1,1,0] * x - v[-1,0,0] * v[-1,1,1] + v[-1,0,1] * v[-1,1,0])
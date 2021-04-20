"""Indexation:
    
    v[a,b,c]: a:[0, tot_trajec]; Point considéré
              b:{0,1}; vecteur position ou dérivée du vecteur position
              c: {0,1}; Coordonnée du vecteur considéré"""



import numpy as np
import matplotlib.pyplot as plt



from Indice import n_grad, n_interface, n_prisme
from Résolution_equation_mouvement import dérivée, RK4
from Prisme import prisme
from Modèles import propagation_grad, propagation_interface, propagation_prisme, faisceau_prisme
import matplotlib.cm as cmx

paramètres = {"Pas d'intégration": 0.01,               #en km
              "Longueur du trajet": 20,               #abscisse curviligne, en km
              "Position initiale": [0,0.5],              #coordonnées du point de départ du rayon
              "Angle initial": np.pi/15,              #angle avec l'horizontale, en rad
              "Fonction dérivée": dérivée,             #fonction utilisée pour le calcul de dérivée
              "Calcul d'indice": n_prisme,               #fonction utilisée pour le calcul de l'indice
              "Pas de calcul du gradient": 0.1,
              "Indice 1 gradient": 2,
              "Indice 2 gradient": 1,
              "Hauteur du gradient": 100,
              "Indice 1 interface": 1,
              "Indice 2 interface": 2,
              "Position dioptre": 150,
              "Indice en dehors du prisme": 1.5,
              "Lambda": 634,
              "Nombre lambda": 20,          #nm
              "Prisme": (2,8,6),   #Géométrie du prisme (x1, x2, y3), prisme de base x1x2 au sol, de hauteur y3
              "Verre": (1.72, 29.3)}        #propriétés du verre; tuple : (nD, Nombre d'Abbe)   


opti_interface = {"Pas d'intégration": 0.01,          #en m     
              "Longueur du trajet": 30,               #abscisse curviligne, en m
              "Position initiale": [0,0],             
              "Angle initial": np.pi/5,               
              "Fonction dérivée": dérivée,             
              "Calcul d'indice": n_interface,               
              "Pas de calcul du gradient": 0.01,
              "Indice 1 interface": 1,
              "Indice 2 interface": 1.33,
              "Position dioptre": 5}  

#propagation_interface(opti_interface)  

opti_gradient = {"Pas d'intégration": 1,               #en m
              "Longueur du trajet": 120,               #abscisse curviligne, en m
              "Position initiale": [0,0],              
              "Angle initial": np.pi/8,                
              "Fonction dérivée": dérivée,             
              "Calcul d'indice": n_grad,               
              "Pas de calcul du gradient": 0.1,
              "Indice 1 gradient": 2,
              "Indice 2 gradient": 1,
              "Hauteur du gradient": 100}

#propagation_grad(opti_gradient)       
  

opti_prisme = {"Pas d'intégration": 0.01,               #en m
              "Longueur du trajet": 15,                #abscisse curviligne, en m
              "Position initiale": [0,0],              
              "Angle initial": np.pi/9,              
              "Fonction dérivée": dérivée,             
              "Calcul d'indice": n_prisme,               
              "Pas de calcul du gradient": 0.1,
              "Indice en dehors du prisme": 1.33,
              "Lambda": 537,                           
              "Prisme": (3,9,6),   
              "Verre": (1.72, 29.3)}

propagation_prisme(opti_prisme)


opti_faisceau = {"Pas d'intégration": 0.01,               
              "Longueur du trajet": 20,               
              "Position initiale": [0,0.5],              
              "Angle initial": np.pi/15,              
              "Fonction dérivée": dérivée,             
              "Calcul d'indice": n_prisme,               
              "Pas de calcul du gradient": 0.1,
              "Indice en dehors du prisme": 1.5,
              "Nombre lambda": 35,                         
              "Prisme": (2,8,6),           
              "Verre": (1.72, 29.3)}       

#faisceau_prisme(opti_faisceau)


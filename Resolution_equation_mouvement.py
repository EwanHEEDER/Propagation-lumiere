import numpy as np

import tqdm


def dérivée(u_prec, u, s, dictionnaire):
    
    n = dictionnaire["Calcul d'indice"]
    ds = dictionnaire["Pas d'intégration"]
    dl = dictionnaire["Pas de calcul du gradient"]
    
    
    """ u_prec : coordonnées au pas précédent
        u : coordonnées au pas actuel
        s : abscisse curviligne au pas actuel
        ds : voir step
    """
    # u est un tuple (r, dr/ds). /!\ r et dr/dt sont des vecteurs
    #du est un tableau , (dr/ds, d^2(r) / ds^2)
    
    du = np.empty(np.shape(u))
    
    dn = n(u[0], dictionnaire) - n(u_prec[0], dictionnaire)
    
    #Calcul du gradient d'indice
    
    dn_x = n(u[0], dictionnaire) - n(u[0] - dl * np.array([1,0]), dictionnaire) 
    
    dn_y = n(u[0], dictionnaire) - n(u[0] - dl * np.array([0,1]), dictionnaire)
        
    grad_n = (dn_x/dl) * np.array([1,0]) + (dn_y/dl) * np.array([0,1])
    
    
    du[0] = u[1]
    
    #Normalisation du vecteur
    
    du[0] /= np.linalg.norm(du[0])
    
    du[1] = (grad_n - dn/ds * u[1]) / n(u[0], dictionnaire)
    
    return du 



def RK4(dictionnaire):
    
    tot_trajec = dictionnaire["Longueur du trajet"]
    step = dictionnaire["Pas d'intégration"]
    v_ini = np.array([dictionnaire["Position initiale"],
                      [np.cos(dictionnaire["Angle initial"]),np.sin(dictionnaire["Angle initial"])]])
    derive = dictionnaire["Fonction dérivée"]
    
    
    """ tot_trajec : longueur totale parcourue en abscisse curviligne (float)
        step : pas d'intégration (float)
        v_ini : paramètres initiaux (array 2x2)
        derive : fonction qui traduit l'équa diff
    """
    
    # Création du tableau d'abscisse curviligne
    
    num_points = int(tot_trajec / step) + 1     # nombre d'éléments
    s = np.linspace(0, tot_trajec, num_points)  #tableau d'abscisse curviligne, on commence obligatoirement à 0

    # initialisation du tableau v, à 3 dimensions: Pour chaque pas --> deux vecteurs de dimension 2
    v = np.empty((num_points,2,2))
    


    # condition initiale
    v[0] = v_ini 
    v[1] = np.array([v_ini[0] + step * v_ini[1], v_ini[1]])

    #Calcul du point suivant
    
    for i in range(2,num_points):
        
        d1 = derive(v[i-2],v[i-1], s[i-1], dictionnaire)
        
        d2 = derive(v[i-2]+ d1 * step/2 , v[i-1] + d1 * step/2, s[i-1] + step/2, dictionnaire)
        
        d3 = derive(v[i-2]+ d2 * step/2 , v[i-1] + d2 * step/2, s[i-1] + step/2, dictionnaire)
        
        d4 = derive(v[i-2] + d3 * step , v[i-1] + d3 * step, s[i-1] + step, dictionnaire)
        
        v[i] = v[i-1] + (d1 + 2 * d2 + 2 * d3 + d4) * step / 6
         
    return s , v


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ TROU NOIR ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



def dérivée_3D(u_prec, u, s, dictionnaire):
    
    """ u_prec : coordonnées au pas précédent
        u : coordonnées au pas actuel
        s : abscisse curviligne au pas actuel
    """
    
    n = dictionnaire["Calcul d'indice"]
    ds = dictionnaire["Pas d'intégration"]
    dl = dictionnaire["Pas de calcul du gradient"]
    
    G = dictionnaire["Constante G"]
    M = dictionnaire["Masse trou noir"]
    c = dictionnaire["Vitesse lumière"]
    centre = dictionnaire["Position trou noir"]
    C = dictionnaire["Concentration"]
    R = dictionnaire["R"]
    g  = 1/(np.log(1+C)-C/(1+C))
    
    #calcul de la distance au centre du trou noir
    r = np.linalg.norm(u[0] - centre)
    
    alpha = r/R
    
    
    # u est un tuple (r, dr/ds). /!\ r et dr/ds sont des vecteurs
    #du est un tableau , (dr/ds, d^2(r) / ds^2)
    
    du = np.empty(np.shape(u))
    
    dn = n(u[0], dictionnaire) - n(u_prec[0], dictionnaire)
    
    #Calcul du gradient 
    
    if r<=R:
        
        dn_x = -2*G*M/c**2*u[0,0]/r**3*g * (-2*C*alpha/(1+C*alpha)+np.log(1+C*alpha) + C*alpha/(1+C*alpha)**2)
        
        dn_y = -2*G*M/c**2*u[0,1]/r**3*g * (-2*C*alpha/(1+C*alpha)+np.log(1+C*alpha) + C*alpha/(1+C*alpha)**2)

        dn_z = -2*G*M/c**2*u[0,2]/r**3*g * (-2*C*alpha/(1+C*alpha)+np.log(1+C*alpha) + C*alpha/(1+C*alpha)**2)
        
        
    #Dans le cas où le rayon passe à l'intérieur de l'objet (jamais le cas pour nous)
    else:

        dn_x = - (2*G*M/c**2) * u[0,0]/r**3
        
        dn_y = - (2*G*M/c**2) * u[0,1]/r**3
        
        dn_z = - (2*G*M/c**2) * u[0,2]/r**3
        
        grad_n = dn_x * np.array([1,0,0]) + dn_y * np.array([0,1,0]) + dn_z * np.array([0,0,1])
    
    
    du[0] = u[1]
    
    du[0] /= np.linalg.norm(du[0])
    
    du[1] = (grad_n - dn/ds * u[1]) / n(u[0], dictionnaire)
    
    return du 



def RK4_3D(dictionnaire):
    
    
    
    tot_trajec = dictionnaire["Longueur du trajet"]
    step = dictionnaire["Pas d'intégration"]
    derive = dictionnaire["Fonction dérivée"]
    theta = dictionnaire["Angle initial en 3D"][0]
    beta = dictionnaire["Angle initial en 3D"][1]
    v_ini = np.array([dictionnaire["Position centre galaxie"],
                      [np.sin(beta)*np.cos(theta), np.sin(beta)*np.sin(theta), np.cos(beta)]])
    
  
    
    # Création du tableau d'abscisse curviligne
    
    num_points = int(tot_trajec / step) + 1     # nombre d'éléments
    s = np.linspace(0, tot_trajec, num_points)  #tableau d'abscisse curviligne, on commence obligatoirement à 0

    # initialisation du tableau v, à 3 dimensions: Pour chaque pas --> deux vecteurs de dimension 3
    v = np.empty((num_points,2,3))
    
    
    #On va conserver l'indice  optique calculé à chaque pas
    indices = np.ones(num_points)
    


    # condition initiale
    v[0] = v_ini 
    v[1] = np.array([v_ini[0] + step * v_ini[1], v_ini[1]])

    
    for i in range(2,num_points):
        
        
        d1 = derive(v[i-2],v[i-1], s[i-1], dictionnaire)
        
        d2 = derive(v[i-2]+ d1 * step/2 , v[i-1] + d1 * step/2, s[i-1] + step/2, dictionnaire)
        
        d3 = derive(v[i-2]+ d2 * step/2 , v[i-1] + d2 * step/2, s[i-1] + step/2, dictionnaire)
        
        d4 = derive(v[i-2] + d3 * step , v[i-1] + d3 * step, s[i-1] + step, dictionnaire)
        
        v[i] = v[i-1] + (d1 + 2 * d2 + 2 * d3 + d4) * step / 6
        
        
        indices[i] = dictionnaire["Calcul d'indice"](v[i,0], dictionnaire)
        
    return s , v, indices

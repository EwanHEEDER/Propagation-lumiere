import numpy as np


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
    
    du = np.empty(np.shape(u))
    
    dn = n(u[0], dictionnaire) - n(u_prec[0], dictionnaire)
    
    dn_x = n(u[0], dictionnaire) - n(u[0] - dl * np.array([1,0]), dictionnaire) #Problème
    
    dn_y = n(u[0], dictionnaire) - n(u[0] - dl * np.array([0,1]), dictionnaire)
        
    grad_n = (dn_x/dl) * np.array([1,0]) + (dn_y/dl) * np.array([0,1])
    
    #print("grad_n =", grad_n)
    
    du[0] = u[1]
    du[1] = grad_n - dn/ds * u[1]
    
    return du # une liste , (dr/ds, d^2(r) / ds^2)

def RK4(dictionnaire):
    
    tot_trajec = dictionnaire["Longueur du trajet"]
    step = dictionnaire["Pas d'intégration"]
    v_ini = np.array([dictionnaire["Position initiale"],
                      [np.cos(dictionnaire["Angle initial "]),np.sin(dictionnaire["Angle initial"])]])
    derive = dictionnaire["Fonction dérivée"]
    
    
    """ tot_trajec : longueur totale parcourue en abscisse curviligne (float)
        step : pas d'intégration (float)
        v_ini : paramètres initiaux (array 2x2)
        derive : fonction qui traduit l'équa diff
    """
    # Création du tableau d'abscisse curviligne
    
    num_points = int(tot_trajec / step) + 1     # nombre d'éléments
    s = np.linspace(0, tot_trajec, num_points) #tableau d'abscisse curviligne, on commence obligatoirement à 0

    # initialisation du tableau v, à 3 dimensions: Pour chaque pas --> deux vecteurs de dimension 2
    v = np.empty((num_points,2,2))
    


    # condition initiale
    v[0] = v_ini 
    v[1] = np.array([v_ini[0] + step * v_ini[1], v_ini[1]])

    # boucle for
    
    for i in range(2,num_points):
        """print("i = ", i)
        
        print("x[i-2] = ", v[i-2,0,0])
        
        print("x[i-1] = ", v[i-1,0,0])
        
        print("dx = ",v[i-1,0,0] - v[i-2, 0, 0])
        """
        
        
        
        #On change la fonction utilisée pour le calcul de dérivée
        
        d1 = derive(v[i-2],v[i-1], s[i-1], dictionnaire)
        
        d2 = derive(v[i-2]+ d1 * step/2 , v[i-1] + d1 * step/2, s[i-1] + step/2, dictionnaire)
        
        d3 = derive(v[i-2]+ d2 * step/2 , v[i-1] + d2 * step/2, s[i-1] + step/2, dictionnaire)
        
        d4 = derive(v[i-2] + d3 * step , v[i-1] + d3 * step, s[i-1] + step, dictionnaire)
        
        v[i] = v[i-1] + (d1 + 2 * d2 + 2 * d3 + d4) * step / 6
        
        
   
    # argument de sortie
    return s , v


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ AMAS DE GALAXIES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def dérivée_3D(u_prec, u, s, dictionnaire):
    
    n = dictionnaire["Calcul d'indice"]
    ds = dictionnaire["Pas d'intégration"]
    dl = dictionnaire["Pas de calcul du gradient"]
    
    """ u_prec : coordonnées au pas précédent
        u : coordonnées au pas actuel
        s : abscisse curviligne au pas actuel
        ds : voir step
    """
    # u est un tuple (r, dr/ds). /!\ r et dr/dt sont des vecteurs
    
    du = np.empty(np.shape(u))
    
    dn = n(u[0], dictionnaire) - n(u_prec[0], dictionnaire)
    
    dn_x = n(u[0], dictionnaire) - n(u[0] - dl * np.array([1,0,0]), dictionnaire) #Problème
    
    dn_y = n(u[0], dictionnaire) - n(u[0] - dl * np.array([0,1,0]), dictionnaire)
    
    dn_z =  n(u[0], dictionnaire) - n(u[0] - dl * np.array([0,0,1]), dictionnaire)
        
    grad_n = (dn_x/dl) * np.array([1,0,0]) + (dn_y/dl) * np.array([0,1,0]) + (dn_z/dl) * np.array([0,0,1])
    
    #print("grad_n =", grad_n)
    
    du[0] = u[1]
    du[1] = grad_n - dn/ds * u[1]
    
    return du # une liste , (dr/ds, d^2(r) / ds^2)

def RK4_3D(dictionnaire):
    
    tot_trajec = dictionnaire["Longueur du trajet"]
    step = dictionnaire["Pas d'intégration"]
    derive = dictionnaire["Fonction dérivée"]
    theta = dictionnaire["Angle initial en 3D"][0]
    beta = dictionnaire["Angle initial en 3D"][1]
    v_ini = np.array([dictionnaire["Position centre galaxie"],
                      [np.sin(beta)*np.cos(theta), np.sin(beta)*np.sin(theta), np.cos(beta)]])
    
    """ tot_trajec : longueur totale parcourue en abscisse curviligne (float)
        step : pas d'intégration (float)
        v_ini : paramètres initiaux (array 2x2)
        derive : fonction qui traduit l'équa diff
    """
    # Création du tableau d'abscisse curviligne
    
    num_points = int(tot_trajec / step) + 1     # nombre d'éléments
    s = np.linspace(0, tot_trajec, num_points) #tableau d'abscisse curviligne, on commence obligatoirement à 0

    # initialisation du tableau v, à 3 dimensions: Pour chaque pas --> deux vecteurs de dimension 2
    v = np.empty((num_points,2,3))
    


    # condition initiale
    v[0] = v_ini 
    v[1] = np.array([v_ini[0] + step * v_ini[1], v_ini[1]])

    # boucle for
    
    for i in range(2,num_points):
        """print("i = ", i)
        
        print("x[i-2] = ", v[i-2,0,0])
        
        print("x[i-1] = ", v[i-1,0,0])
        
        print("dx = ",v[i-1,0,0] - v[i-2, 0, 0])
        """
        
        
        
        #On change la fonction utilisée pour le calcul de dérivée
        
        d1 = derive(v[i-2],v[i-1], s[i-1], dictionnaire)
        
        d2 = derive(v[i-2]+ d1 * step/2 , v[i-1] + d1 * step/2, s[i-1] + step/2, dictionnaire)
        
        d3 = derive(v[i-2]+ d2 * step/2 , v[i-1] + d2 * step/2, s[i-1] + step/2, dictionnaire)
        
        d4 = derive(v[i-2] + d3 * step , v[i-1] + d3 * step, s[i-1] + step, dictionnaire)
        
        v[i] = v[i-1] + (d1 + 2 * d2 + 2 * d3 + d4) * step / 6
        
        
   
    # argument de sortie
    return s , v

import numpy as np

from Prisme import prisme 

def n_grad(position, dictionnaire):
    
    n1, n2 = dictionnaire["Indice 1 gradient"], dictionnaire["Indice 2 gradient"]
    
    hauteur = dictionnaire["Hauteur du gradient"]
    
    
    if position[1] <= hauteur:
        
        delta_n =n2 - n1
    
        return (delta_n / hauteur) * position[1] + n1
    
    else:
        
        return n2

def n_interface(position, dictionnaire):
    
    dioptre = dictionnaire["Position dioptre"]
    n1 = dictionnaire["Indice 1 interface"]
    n2 = dictionnaire["Indice 2 interface"]
    
    if position[0]< dioptre:
        n=n1
    else:
        n=n2
    return n


def n_prisme(position, dictionnaire):       #Possible changer verre. Par défaut --> EDF
    
    Lambda = dictionnaire["Lambda"]
    n1 = dictionnaire["Indice en dehors du prisme"]
    nD, VD = dictionnaire["Verre"][0], dictionnaire["Verre"][1]


    """ Input: position = Vecteur position (x,y)
               Lambda = longueur donde du rayon (nm)
               prisme = prisme dans lequel on envoie le rayon défini par ses sommets
               n1 = Indice du milieu dans lequel se trouve le prisme
               nd, vd = paramètres du verre; indice pour la raie de référence D & nombre d'Abbe du verre"""
    
   
    f1, f2 = prisme(dictionnaire)      #fonction du côté gauche puis droit de notre prisme

    if (position[1] <= f1(position[0])) & (position[1] <= f2(position[0])): 
        
        lC=656.3
        lD=589.3
        lF=486.1
        
        B = (nD-1)/(VD*(1/(lF*lF)-1/(lC*lC)))
        A=nD - B/(lD*lD)
        
        n = A + B/(Lambda**2)
        
    else:
        
        n = n1
    
    return n
        
    

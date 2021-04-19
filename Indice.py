import numpy as np

from Prisme import prisme 

def n_grad(position, n1 = 1.000157, n2 = 1.0, hauteur = 1000):
    
    if position[1] <= hauteur:
        
        delta_n =n2 - n1
    
        return (delta_n / hauteur) * position[1] + n1
    
    else:
        
        return n2



def n_interface(position, dioptre = 150, n1 = 1., n2 = 2):
    
    if position[0]< 150:
        n=n1
    else:
        n=n2
    return n


def n_prisme(position, Lambda, n1, nD = 1.72, VD = 29.3): #Possible changer verre. Par défaut --> Crown C

    """ Input: position = Vecteur position (x,y)
               Lambda = longueur donde du rayon (nm)
               prisme = prisme dans lequel on envoie le rayon défini par ses sommets
               n1 = Indice du milieu dans lequel se trouve le prisme
               nd, vd = paramètres du verre; indice pour la raie de référence D & nombre d'Abbe du verre"""
    
   
    f1, f2 = prisme(2,8,7)      #fonction du côté gauche puis droit de notre prisme

        
    if (position[1] <= f1(position[0])) & (position[1] <= f2(position[0])): 
        
        lC=656.3
        lD=589.3
        lF=486.1
        
        B = (nD-1)/(VD*(1/(lF*lF)-1/(lC*lC)))
        A=nD - B/(lD*lD)
        
        n = A + B/(Lambda**2)
        
        return n
        
    else:
        
        return n1
        
position = np.array([2,0])
print(n_prisme(position,420,1.0))
    

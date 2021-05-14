import numpy as np

from Prisme import prisme



def n_grad(position, dictionnaire):
    
    n1, n2 = dictionnaire["Indice 1 gradient"], dictionnaire["Indice 2 gradient"]
    
    hauteur = dictionnaire["Hauteur du gradient"]
    
    
    if position[1] <= hauteur:
        
        delta_n =n2 - n1
    
        #A l'altitude 0, n = n1 donc on ajoute n1
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



def n_prisme(position, dictionnaire):       #Possible changer verre. Par défaut --> Dense Flint
    
    Lambda = dictionnaire["Lambda"]
    n1 = dictionnaire["Indice en dehors du prisme"]
    nD, VD = dictionnaire["Verre"][0], dictionnaire["Verre"][1]
    
   
    #parois du prisme
    f1, f2 = prisme(dictionnaire)      

    if (position[1] <= f1(position[0])) & (position[1] <= f2(position[0])): 
        
        lC=656.3
        lD=589.3
        lF=486.1
        
        B = (nD-1)/(VD*(1/(lF*lF)-1/(lC*lC)))
        A = nD - B/(lD*lD)
        
        n = A + B/(Lambda**2)
        
    else:
        
        n = n1
    
    return n

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ LENTILLE GRAVITATIONNELLE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#Si on est en dehors de l'objet
def phi_sup(r, dictionnaire):
    
    return - dictionnaire["Constante G"]*dictionnaire["Masse trou noir"]/r


#Si on se trouve dans l'objet (plus proche que son rayon)

def phi_inf(r, dictionnaire):
    
    G = dictionnaire["Constante G"]
    M = dictionnaire["Masse trou noir"]
    C = dictionnaire["Concentration"]
    R = dictionnaire["R"]
    
    g = 1/(np.log(1+C)-C/(1+C))
    
    alpha = r/R
    
    return -(G*M)/r*g*(np.log(1+C*alpha)-C*alpha/(1+C*alpha))


        
def n_grav(position, dictionnaire):
    
    c = dictionnaire["Vitesse lumière"]
    R = dictionnaire["R"]
    centre = dictionnaire["Position trou noir"]
    
    #Calcul de la distanec au centre du trou noir
    r = np.linalg.norm(position - centre)
    
    
    if r<=R:
        
        phi = phi_inf(r, dictionnaire)
        
    else : 
        
        phi = phi_sup(r, dictionnaire)
     
    
    return 1-2*phi/c**2

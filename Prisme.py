
def prisme(dictionnaire):
    
    x1 = dictionnaire["Prisme"][0]
    x2 = dictionnaire["Prisme"][1]
    y3 = dictionnaire["Prisme"][2]
    
    """Prisme isocèle"""
    
    a1 = (2 * y3)/(x2 - x1)
    
    b1 =-2 * x1 * y3/(x2 - x1) #par définition de la tangente
    
    a2 = (2 * y3)/(x1 - x2)
    
    b2 = 2 * y3 * x2/(x2 - x1)  #par théoreme de Thalès 
    
    def f1(x):
        
        return a1 * x + b1
   
    def f2(x):
        
        return a2 * x + b2

    #On return les fonctions correspondant aux parois du prisme
    
    return f1, f2

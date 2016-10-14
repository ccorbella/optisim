import numpy as np
import random

def numero_articles():
    """ Retorna el número d'articles que ha demanat el client, seguint
    la funció de probabilitat proporcionada a l'enunciat."""
    return np.random.choice([3,8,12,18,30],p=[0.1,0.2,0.25,0.15,0.3])

def temps_cobrar(articles):
    return 3*articles + random.uniform(120,360)

def supermercat(T,nl,N):
    caixes            = np.zeros(N)
    propera_entrada   = 0
    propera_sortida   = 1000
    properes_sortides = np.zeros(N)
    t                 = 0
    
    data = {k: [] for k in xrange(N)}
    
    while (t < T) or (caixes.sum() > 0):
        
        #Mirem quin és el proper esdeveniment. Si el primer que passa és que arriba un nou client,
        if  ((t == propera_entrada) or (caixes.sum() == 0)) and (t < T):
            #Mirem el número d'articles que tindra el client i li donem caixa.
            n                  = numero_articles()
            
            if n <= 10:
                idx_caixa      = np.argmin(caixes)
            else:
                idx_caixa      = np.argmin(caixes[:nl])
            
            caixes[idx_caixa] += 1
            data[idx_caixa].append((propera_entrada,n))
            
            #Cerquem propera entrada i sortida, en el supòsit que no hi 
            #hagués cap altre client davant del nou.
            propera_entrada   += random.expovariate(1/15.0)
            
            if caixes[idx_caixa] == 1:
                properes_sortides[idx_caixa] = propera_entrada + temps_cobrar(n)
                propera_sortida              = np.min(properes_sortides[caixes != 0])
        
        else:
            min_sortides                     = np.min(properes_sortides[caixes != 0])
            idx_caixa                        = np.where(properes_sortides == min_sortides)[0][0]
            element = data[idx_caixa].pop(0) #eliminem el primer element de la llista
            properes_sortides[idx_caixa]     = element[0] + temps_cobrar(element[1])
            caixes[idx_caixa]               -= 1
            
            if (caixes > caixes[idx_caixa]).sum() > 0:
                idx = np.where(caixes > caixes[idx_caixa])[0][0]
                data[idx_caixa].append(data[idx].pop())
                caixes[idx_caixa] += 1
                caixes[idx]       -= 1
                
        t = min(propera_entrada,propera_sortida)
        
print(supermercat(2000,17,20))
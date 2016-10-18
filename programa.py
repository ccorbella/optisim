# -*- coding: utf-8 -*-

import numpy as np
import random
import math

def numero_articles():
    """ Retorna el numero d'articles que ha demanat el client, seguint
    la funcio de probabilitat proporcionada a l'enunciat. """
    return np.random.choice([3,8,12,18,30],p=[0.1,0.2,0.25,0.15,0.3])

def temps_cobrar(articles):
    return 3*articles + random.uniform(120,360)

def supermercat(T,nl,N):
    caixes            = np.zeros(N)
    propera_entrada   = 0
    propera_sortida   = 1000
    properes_sortides = np.zeros(N)
    t                 = 0

    espera_clients    = np.empty(T)
    temps_espera      = np.empty(0)
    
    data = {k: [] for k in xrange(N)}
    
    while (t < T) or (caixes.sum() > 0):

        to = t
        
        #Mirem quin és el proper esdeveniment. Si el primer que passa és que arriba un nou client,
        if  ((t == propera_entrada)) and (t < T):
            #Mirem el número d'articles que tindra el client i li donem caixa.
            n                  = numero_articles()
            
            if n <= 10:
                idx_caixa      = np.argmin(caixes)
            else:
                idx_caixa      = np.argmin(caixes[:nl])
                        
            caixes[idx_caixa] += 1
            data[idx_caixa].append((propera_entrada,n))
            
            #Cerquem propera entrada 
            propera_entrada   += random.expovariate(1/15.0)
            
            #i sortida, en el supòsit que no hi hagués cap altre client davant del nou.
            if caixes[idx_caixa] == 1:
                properes_sortides[idx_caixa] = t + temps_cobrar(n) #hauria de ser t!
                #aqui vale perque coincideix que la caixa estava buida fins que no hem arribat nosaltres i paguem
                propera_sortida              = np.min(properes_sortides[caixes != 0])
        
        else:
            idx_caixa                        = np.argmin(properes_sortides[caixes != 0]) 
            element = data[idx_caixa].pop(0) #eliminem el primer element de la llista
            caixes[idx_caixa]               -= 1

            if caixes[idx_caixa] > 0: #si a la caixa que acaba de cobrar queda gent fent cua, cobrem al seguent
                properes_sortides[idx_caixa] = t + temps_cobrar(data[idx_caixa][0][1])
                propera_sortida              = np.min(properes_sortides[caixes != 0])

            temps_espera                     = np.append(temps_espera,t-element[0]) #estem comptant tambe el temps
                                                                                    #que s'esta cobrant!!
            
            if (caixes > (caixes[idx_caixa] +1) ).sum() > 0:  #alguna caixa amb mes gent que la nostra
                if idx_caixa >= nl: #caixa rapida! cas especial
                    for idx in np.where(caixes > (caixes[idx_caixa]+1)):
                        print idx
                        print data[idx]
                        if data[idx][-1][1] <= 10: #el num d'articles de l'ultima persona de la fila que es mes llarga
                                                   #que la meva es menor que 10 i pot anar xt a una caixa rapida
                            data[idx_caixa].append(data[idx].pop()) #faig el canvi de cua
                            caixes[idx]       -= 1
                            if caixes[idx_caixa] == 1:
                                properes_sortides[idx_caixa] = t + temps_cobrar(n)
                                propera_sortida              = np.min(properes_sortides[caixes != 0])
                            break

                                
                else:   #tothom pot canviar de fila! 
                    idx = np.where(caixes > (caixes[idx_caixa]+1))[0][0] #suposo que obtenim el primer (mes a l'esquerra)
                    data[idx_caixa].append(data[idx].pop()) #canviem l'ULTIM de la fila on son mes i el fiquem a l'actual
                    caixes[idx_caixa] += 1
                    caixes[idx]       -= 1
                    if caixes[idx_caixa] == 1:
                        properes_sortides[idx_caixa] = t + temps_cobrar(n)
                        propera_sortida              = np.min(properes_sortides[caixes != 0])

        if caixes.sum() > 0:
            propera_sortida = np.min(properes_sortides[caixes!=0])
        t = min(propera_entrada,propera_sortida)
        espera_clients[int(math.floor(to)):int(math.ceil(t))] = caixes.sum()
        #print t
        #print idx_caixa
        #print np.vstack((caixes, properes_sortides))

    return np.mean(espera_clients), np.mean(temps_espera)

""" 
super = np.empty(10)
for i in xrange(10):
    super[i] = supermercat(60*60*12,1,20)[1]
    
print(np.mean(super))
"""

print supermercat(20*60,1,5)

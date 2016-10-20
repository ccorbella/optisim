# -*- coding: utf-8 -*-
#@Autors: Corbella Bagot, Conrad; Guasch Morgades, Maria; Ripoll Oliveras, Albert; Taulé Flores, Pere
#Creat: 10/10/2016

#IMPORTS
import numpy as np
import random
import math

#FUNCIONS AUXILIARS
def numero_articles():
    """ Retorna el numero d'articles que ha demanat el client, seguint
    la funcio de probabilitat proporcionada a l'enunciat. """
    return np.random.choice([3,8,12,18,30],p=[0.1,0.2,0.25,0.15,0.3])

def temps_cobrar(articles):
    """ Retorna el temps necessari per cobrar: 3 segons per article
    mes un temps de 2-6 min (distr uniforme). """
    return 3*articles + random.uniform(120,360)

#FUNCIÓ PRINCIPAL
def supermercat(T,nl,N):
    """                            Programa principal de la simulació
    T: jornada laboral (en segons) // nl: numero de caixes lentes // N: nombre total de caixes"""

    caixes            = np.zeros(N)         #nombre de persones de la caixa i
    propera_entrada   = 0                   
    propera_sortida   = 1000                #ens inventem un valor que canviarà al primer loop perquè no peti
    properes_sortides = np.zeros(N)         #quan acabarà la primera persona a la caixa i
    t                 = 0                   #rellotge

    espera_clients    = np.zeros(int(1.1*T))         #num de clients esperant a cada instant t de temps
    espera_clients_v  = 0                            #acumulat del num de clients esperant a cada instant t de temps
    espera_temps      = np.zeros(int(1.1*T))         #temps d'espera 'instantani' a cada instant t (mitja dels ultims 10 valors)
    temps_espera      = np.empty(0)                  #temps d'espera de cada client
    llista_caixes     = np.arange(0,N,1)             #llista auxiliar
    
    data = {k: [] for k in xrange(N)}       #per cada caixa k disposem d'una llista de tuples (temps d'arribada, num articles)
    
    while (t < T) or (caixes.sum() > 0):    #Comencem el loop

        to = t                              #Var auxiliar per graficar coses                        
        
        #Mirem quin és el proper esdeveniment:
        
        #Arriba un nou client (i seguim dins de la jornada laboral T)
        if  ((t == propera_entrada)) and (t < T): 
            
            #Afegim el número d'articles i el temps de cobrar
            n                  = numero_articles()
            t_cobrar           = temps_cobrar(n)
            
            #Assignem la caixa amb la cua més curta al client 
            if n <= 10:                                     #Pot anar a qualsevol caixa
                idx_caixa      = np.argmin(caixes)
            else:                                           #Només caixa lenta (les nl primeres)
                idx_caixa      = np.argmin(caixes[:nl])
                        
            #Actualitzem les variables d'estat
            caixes[idx_caixa] += 1                          
            data[idx_caixa].append((propera_entrada,n,t_cobrar))
            
            #Cerquem propera entrada
            propera_entrada   += random.expovariate(1/15.0)
            
            #En el supòsit que no hi hagués cap altre client davant del nou podem definir ja la sortida:
            #es el temps actual (t) + el que tarda a cobrar
            if caixes[idx_caixa] == 1:
                properes_sortides[idx_caixa] = t + data[idx_caixa][0][2]              #afegim el temps de cobrar
                propera_sortida              = np.min(properes_sortides[caixes != 0])
               
            
            
        
        #Fi de compra/ sortida d'un client 
        else:
            #caixa d'on acaba un client
            
            idx_caixa                        = llista_caixes[caixes != 0][np.argmin(properes_sortides[caixes != 0])] 
            element = data[idx_caixa].pop(0) #eliminem el primer element de la llista corresponent a la caixa que toca (client ja atès)
            caixes[idx_caixa]               -= 1 #actualitzem també la llista de caixes
            
            
            
            #Calculem quan s'ha esperat la persona que acaba de ser atesa
            temps_espera                     = np.append(temps_espera,t-element[0] - element[2]) #restem el temps d'arribada [0]
                                                                                                 #i el de cobrar [2]
             
            
            #Si a la caixa que acaba de cobrar queda gent fent cua, comencem a cobrar al següent:
            if caixes[idx_caixa] > 0: 
                properes_sortides[idx_caixa] = t + data[idx_caixa][0][2]             #afegim el temps de cobrar
                propera_sortida              = np.min(properes_sortides[caixes != 0])
            
            
            
            #Canvi de fila
            if (caixes > (caixes[idx_caixa] +1) ).sum() > 0:  #alguna caixa amb mes gent que la nostra
                
                #Caixa ràpida: només poden venir clients ràpids
                if idx_caixa >= nl:
                    for idx in np.where(caixes > (caixes[idx_caixa]+1))[0]: #mirem per les cues més llargues que la nostra
                        
                        if data[idx][-1][1] <= 10: #si el num d'articles de l'ultima persona de la fila es menor que 10
                            
                            data[idx_caixa].append(data[idx].pop()) #pot fer el canvi de cua
                            caixes[idx_caixa] += 1
                            caixes[idx]       -= 1 

                            
                            if caixes[idx_caixa] == 1: #si ara el que s'ha canviat és el primer ja podem definir la seva sortida:
                                properes_sortides[idx_caixa] = t + data[idx_caixa][0][2]             #afegim el temps de cobrar
                                propera_sortida              = np.min(properes_sortides[caixes != 0])
                                break

                #Caixa normal: tothom pot venir                
                else:   
                    idx = np.where(caixes > (caixes[idx_caixa]+1))[0][0] #triem la primera cua que es mes llarga que la nostra
                    data[idx_caixa].append(data[idx].pop()) #canviem l'ultim de la fila on son mes i el fiquem a l'actual
                    caixes[idx_caixa] += 1
                    caixes[idx]       -= 1
                    if caixes[idx_caixa] == 1: #si ara el que s'ha canviat és el primer ja podem definir la seva sortida:
                        properes_sortides[idx_caixa] = t + data[idx_caixa][0][2]             #afegim el temps de cobrar
                        propera_sortida              = np.min(properes_sortides[caixes != 0])
                        
        if caixes.sum() > 0: #definim ara quina es la propera sortida
            propera_sortida = np.min(properes_sortides[caixes!=0])
        
        #Actualitzem el temps fins al proper esdeveniment
        if propera_entrada<T: #el proper esdeveniment serà el mínim
            t = min(propera_entrada,propera_sortida) 
        else: #hem tancat portes ja i només hem d'atendre la gent que queda dins
            t = propera_sortida
            
            
        espera_clients[int(math.floor(to)):int(math.ceil(t))] = caixes.sum() #Clients totals esperant entre els dos esdeveniments
        espera_clients_v += caixes.sum()*(t-to)
        if len(temps_espera) > 10:
            espera_temps[int(math.floor(to)):int(math.ceil(t))] = np.mean(temps_espera[-10:])

    """Es retorna:
        -np.mean(espera_clients_v): mitjana del nombre de clients esperant
        -np.mean(temps_espera)    : mitjana de temps esperat per cada client
        -espera_clients           : vector que conté els clients que s'estan esperant en cada instant de temps (discretitzant a segons)
        -espera_temps             : vector que conté el temps d'espera en cada instant de temps, calculat com la mitjana dels últims
                                    10 temps d'espera """
    
    
    return np.mean(espera_clients_v), np.mean(temps_espera), espera_clients, espera_temps 
    

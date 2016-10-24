# -*- coding: utf-8 -*-
from programa import supermercat

N = 1000         #Nombre de simulacions: 1000
T = 12*60*60     #Durada de simulació:   12h

mitja_espera_clients = np.empty(N);        mitja_temps_espera = np.empty(N);
espera_clients = np.empty((N,int(1.1*T))); espera_temps = np.empty((N,int(1.1*T)))

#El tamany dels vectors ha de ser més llarg que T perquè hi hagi temps a que s'acabin d'atendre els de la cua

for i in xrange(N):
    mitja_espera_clients[i], mitja_temps_espera[i], espera_clients[i,:], espera_temps[i,:] = supermercat(T, 17,20)
    

MITJA_TEMPS =np.mean(mitja_temps_espera)
print "Els clients s'esperen de mitjana %f segons (%f minuts)" %(MITJA_TEMPS, MITJA_TEMPS/60.0)

MITJA_CLIENTS =np.mean(mitja_espera_clients)
print "Hi ha %f clients de mitjana esperant-se" %MITJA_CLIENTS




#GRAFIQUES!
import matplotlib.pyplot as plt
%matplotlib inline
t = np.arange(0,int(1.1*T))/60.0

#Temps d'espera per a cada simulació (sobreposats). Permet observar la gran variància en els resultats.
plt.figure(figsize=(21, 7));
for i in xrange(N):
    plt.plot(t,espera_temps[i,:])
plt.ylabel("Temps d'espera", fontsize=18)
plt.xlabel('Temps', fontsize=18)
    
plt.savefig('Temps espera.png')


#Clients esperant per a cada simulació (sobreposats). Permet observar la gran variància en els resultats.
plt.figure(figsize=(21, 7));
for i in xrange(N):
    plt.plot(t, espera_clients[i,:])
    
plt.ylabel("Clients esperant", fontsize=18)
plt.xlabel('Temps', fontsize=18)
plt.savefig('Clients esperant.png')


#Mitja del temps d'espera respecte t
plt.figure(figsize=(21, 7));
mitja_espera = np.empty(int(1.1*T))
for i in xrange(int(1.1*T)):
    mitja_espera[i] = np.mean(espera_temps[:,i])
plt.plot(t, mitja_espera)
plt.ylabel("Temps d'espera", fontsize=18)
plt.xlabel('Temps', fontsize=18)
plt.savefig('Mitja temps espera.png')

#Mitja dels clients esperant respecte t
plt.figure(figsize=(21, 7));
mitja_clients = np.empty(int(1.1*T))
for i in xrange(int(1.1*T)):
    mitja_clients[i] = np.mean(espera_clients[:,i])
plt.plot(t, mitja_clients)
plt.ylabel("Clients esperant", fontsize=18)
plt.xlabel('Temps', fontsize=18)
plt.savefig('Mitja clients esperant.png')


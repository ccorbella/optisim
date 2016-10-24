# optisim
Simulació i Optimització Market Simulation Project 

Per a fer ús dels codis, feu-ne un "clone" (si sou usuaris de **Git**) o simplement "descarregueu-los" en una carpeta.

A la carpeta, trobareu:

* El programa **optimitzacio.py** intenta cercar quina combinació de caixes ràpides i lentes proporciona una millor atenció als usuaris (en el sentit que els clients són atesos més ràpidament i n'hi ha menys a les cues). Per a fer-ho, proporciona dues gràfiques amb la mitjana obtinguda amb cada combinació de caixes, una amb el temps d'espera i una altra amb el nombre de clients que es troben esperant.

* El programa **'calcul_transitori.py'** permet crear gràfiques dels comptadors estadístics (mitjana de clients esperant i temps d'espera mitjà) en funció de l'evolució del rellotge. En el primer parell de gràfiques es representen els resultats sobreposats de les 1000 simulacions realitzades, la qual cosa permet observar de forma molt visual la gran variabilitat de resultats que hi ha. Encara que, amb atenció, també s'hi pot observar directament el transitori, hem optat per representar a sota la mitjana per les 1000 simulacions d'aquests comptadors estadístics. En aquest segon parell de gràfiques queda clar quin és el transitori inicial (~3 hores) i el final (passades les 12h).
* El programa **'histograma.py'** proporciona els vectors que es van utilitzar en Minitab. De fet, en proporciona un en què les mostres estan agrupades de 10 en 10 i se'n calcula la mitjana i un altre amb les 10000 mostres senceres. Tant en un cas com en l'altre, es retira anteriorment el transitori dels resultats, eliminant les mostres que es creen abans que hagin passat 3 hores.

import math


def euclidean_distance(A,B):
    x_A= A[0]
    y_A= A[1]

    x_B= B[0]
    y_B= B[1]

    x= abs(x_A - x_B)
    y= abs(y_A - y_B)

    d= math.sqrt(x**2 + y**2)

    return d




# Conta il numero di città visitate
def calcola_citta_visitate(percorso,dizionario_citta):
    citta= list(dizionario_citta.keys())

    n_citta_visitate= 0

    for key in citta:
        if key in percorso:
            n_citta_visitate += 1

    return n_citta_visitate


# Conta il numero di nodi visitati    ( l'unica purtroppo differenza da 'calcola_citta_visitate' è che nodi è gia una lista di elementi e non un oggetto Cliente)
def calcola_nodi_visitati(nodi_visitati,nodi):
    n_nodi_visitati= 0

    for key in nodi:
        if key in nodi_visitati:
            n_nodi_visitati += 1

    return n_nodi_visitati



# ---------------------------------------- GREEDY ----------------------------------------
# Per NearestNeighbour
def find_next_node(percorso,current_node,dizionario_citta,dizionario_stazioni):
    min_dist= 10000000

    # Tiro fuori le coordinate del nodo corrente
    if current_node == 0:
        # In questo caso il nodo corrente è il deposito
        current_coordinate= [0,0]
    elif 'S' in str(current_node):
        # In questo caso il nodo corrente è una stazione
        current_station= current_node.replace('S','')

        current_coordinate= dizionario_stazioni.get(int(current_station))
    else:
        cliente= dizionario_citta.get(current_node) 
        current_coordinate= cliente.coordinate

    clients= list(dizionario_citta.keys())


    for client in clients:
        if client not in percorso:
            node= dizionario_citta.get(int(client))

            distance= euclidean_distance(node.coordinate,current_coordinate)

            if distance <= min_dist:
                min_dist= distance
                next_node= client
                
    return next_node, min_dist


# Tempo di ricarica è dato da 0.25 unita di tempo per unita metrica di autonomia ricaricata
def NearestNeighbour(dizionario_citta, dizionario_stazioni, deposito, k, N_CITIES):
    tempo_ricarica= 0  #Tempo speso a ricaricare
    distanza_percorsa= 0

    autonomia= k
    percorso= []

    current_node= deposito

    # Il nodo 0 è il deposito
    percorso.append(0)

    n_citta_visitate= calcola_citta_visitate(percorso,dizionario_citta)


    # Qua ci vuole un ciclo while
    while n_citta_visitate < N_CITIES - 1:

        # Se il nodo corrente non è il deposito, prendo l'oggetto cliente relativo
        if current_node != 0 and 'S' not in str(current_node):
            current_client= dizionario_citta.get(current_node)


        next_node, next_distance= find_next_node(percorso,current_node,dizionario_citta,dizionario_stazioni)

        future_autonomy= autonomia - next_distance

        next_client= dizionario_citta.get(int(next_node))

        # Se l'autonomia rimanente dovuta al prossimo spostamento che vorrei fare, non mi permetterebbe di andare a ricaricare partendo dal next_node
        # significa che non mi dovrò muovere verso il next_node ma dovrò prima andare a ricaricare l'auto 
        # NB: Questa condizione è veritiera solo nel caso in cui le stazioni di ricarica siano al centro di ogni quadrante
        if future_autonomy - next_client.distanza_stazione < 0:
            # Effettuo la ricarica
            # Aggiorno:
            #   - Percorso
            #   - Distanza Percorsa
            #   - Tempo Ricarica
            #   - Autonomia (Piena)       (N.B. Bisogna in futuro valutare quanto ricaricare)
            #   - Nodo Corrente (Stazione)

            node_station= str(current_client.get_quadrant()) + 'S'

            percorso.append(node_station)

            distanza_percorsa += current_client.distanza_stazione

            # delta_autonomia mi indica quanto devo ricaricare 

            delta_autonomia= k - (autonomia - current_client.distanza_stazione)

            tempo_ricarica += 0.25*delta_autonomia

            autonomia= k
            
            current_node= node_station

        else:
            # Sono nel caso in cui lo spostamento al prossimo nodo mi permette di muovermi nella stazione di ricarica

            distanza_percorsa += next_distance

            autonomia -= next_distance

            current_node= next_node

            percorso.append(next_node)
        
        # print("Percorso: " + str(percorso))
        # Aggiorno le città visitate
        n_citta_visitate= calcola_citta_visitate(percorso,dizionario_citta)
        # print("n_citta_visitate: " + str(n_citta_visitate))

    # Quando esco dal while significa che sono andato in tutte le città e non mi resta altro che tornare al deposito 
    # Quando esco dal ciclo sono PER FORZA in una citta

    current_client= dizionario_citta.get(current_node)

    # Controllo se ho l'autonomia sufficiente per tornare al deposito, se non ce l'ho mi fermo nella stazione del quadrante
    if autonomia - current_client.distanza_deposito < 0:
        # 1) Vado nella stazione di ricarica e aggiorno i valori di:
        #       - Percorso
        #       - Distanza Percorsa
        #       - Autonomia rimasta

        node_station= str(current_client.get_quadrant()) + 'S'
        percorso.append(node_station)

        distanza_percorsa += current_client.distanza_stazione

        # Aggiorno l'autonomia rimasta
        autonomia -= current_client.distanza_stazione

        # 2) Raggiunto la stazione devo ricaricare l'auto, la ricarico solo dell'autonomia necessaria per tornare al deposito dalla stazione
        #    in modo da evitare sprechi di tempo

        #    Per prima cosa recupero le coordinate della stazione in cui mi trovo
        node_station= node_station.replace('S','')
        coordinate_station= dizionario_stazioni.get(int(node_station))

        # Calcolo la distanza tra la STAZIONE CORRENTE e il deposito   (In questo punto non sono più nell'ultima citta visitata ma sono nella stazione di ricarica che devo partire per tornare al deposito)
        distanza_stazione_deposito= euclidean_distance(coordinate_station,[0,0])

        # Calcolo quanto devo ricaricare, ovvero io devo ricaricare pari a: distanza_deposito - autonomia rimasta 
        # dato che di
        delta_autonomia= distanza_stazione_deposito - autonomia

        tempo_ricarica += 0.25*delta_autonomia

        # 3) Torno al deposito, quindi aggiorno:
        #       - Percorso
        #       - Distanza Percorsa
        percorso.append(0)

        distanza_percorsa += distanza_stazione_deposito
    
    else:
    # Qui siamo nel caso in cui dall'ultima città si abbia autonomia sufficiente per tornare al deposito       
    # In questo caso devo solo aggiornare:
    #           - Percorso
    #           - Distanza Percorsa
        percorso.append(0)

        distanza_percorsa += current_client.distanza_deposito

    tempo_totale= distanza_percorsa + tempo_ricarica

    tempo_totale= round(tempo_totale,2)
    distanza_percorsa= round(distanza_percorsa,2)

    return percorso, distanza_percorsa, tempo_totale, tempo_ricarica


# ---------------------------------------- NON GREEDY ----------------------------------------

# Per MST
def calcola_dizionario_distanze(dizionario_citta):
    dizionario_distanze_citta= {}
    citta= list(dizionario_citta.keys())

    lista_distanze_deposito= [0]

    for n in citta:
        lista_distanze= []
        current_node= dizionario_citta.get(int(n))
        current_coordinate= current_node.coordinate
        
        distanza_deposito= current_node.distanza_deposito
        distanza_deposito= round(distanza_deposito,2)

        lista_distanze.append(distanza_deposito)
        lista_distanze_deposito.append(distanza_deposito)

        for i in citta:
            if i != n:
                next_node= dizionario_citta.get(int(i))
                next_coordinate= next_node.coordinate
                distance= euclidean_distance(current_coordinate,next_coordinate)
                distance= round(distance,2)
                lista_distanze.append(distance)
            else: 
                distance= 0
                lista_distanze.append(distance)

        dizionario_distanze_citta[n]= lista_distanze

    dizionario_distanze_citta[0]= lista_distanze_deposito
    return dizionario_distanze_citta




# L'ammissibilità dell' arco trovato qui viene determinata da MinimumSpanningTree
def ricerca_arco_minimo(dizionario_distanze_citta, dizionario_uso_archi):

    distanza_minima_arco= 100000000000
    nodo1= -1
    nodo2= -1

    nodi= list(dizionario_distanze_citta.keys())

    for key in nodi:
        lista_uso_archi_nodoKey= dizionario_uso_archi.get(key)   # lista_uso_archi è la lista contenente gli archi del nodo key
        i= 0   # indice nodo2, ovvero l'indice della lista degli archi
        for uso in lista_uso_archi_nodoKey:

            # Prendo in considerazione solo gli archi che non sono ancora stati usati e ovviamente non prendo in considerazione le distanze con se stessi ( che sono uguali a 0)
            if uso == 0 and i != key:
                lista_distanze= dizionario_distanze_citta.get(key)

                if lista_distanze[i] <= distanza_minima_arco: 
                    distanza_minima_arco= lista_distanze[i]
                    nodo1= key
                    nodo2= i
                    
            i += 1

    return distanza_minima_arco, nodo1, nodo2      

# Ritorna True se l'arco minimo selezionato NON crea un ciclo 

def verifica_ammissibilita(nodo1,nodo2,dizionario_sottoAlberi):

    if len(dizionario_sottoAlberi) == 0:
        sotto_set= [nodo1,nodo2]
        dizionario_sottoAlberi[1]= sotto_set
        return True
    else:

        lista_insiemi= list(dizionario_sottoAlberi.keys())

        # Vado a vedere a quali insiemi appartengono questi nodi, se non appartengono ad un insieme , prendono il valore di -1
        insiemeNodo1= -1
        insiemeNodo2= -1
        for n in lista_insiemi:
            nodi_insieme= dizionario_sottoAlberi.get(n)

            if nodo1 in nodi_insieme:
                insiemeNodo1= n
            if nodo2 in nodi_insieme:
                insiemeNodo2= n


        # Ci sono 4 possibilità: 
        # 1- Entrambi i nodi non fanno parte di nessun insieme, creo un nuovo insieme contentente entrambi questi nodi ( di fatto formano il primo albero del nuovo insieme)
        # 2- Almeno un nodo fa parte di un insieme e l'altro di nessuno allora aggiungo il secondo nodo all'insieme del primo
        # 3- I nodi fanno parte di due insiemi diversi, unisco i due insiemi 
        # 4- Entrambi i nodi fanno parte di uno stesso insieme, l'arco non è ammissibile
        
        
        if insiemeNodo1 == -1 and insiemeNodo2 == -1:
        # 1. Nodi non facenti parte di alcun insieme, creo nuovo insieme

            i= max(lista_insiemi) # i vale come l'ultimo insieme aggiunto

            dizionario_sottoAlberi[i+1]= [nodo1,nodo2]
            return True

        elif insiemeNodo1 != -1 and insiemeNodo2 == -1:
        # 2A. Caso in cui solo uno dei due nodi fa parte di un insieme    
            nodi_insieme= dizionario_sottoAlberi.pop(insiemeNodo1)
            nodi_insieme.append(nodo2)

            dizionario_sottoAlberi[insiemeNodo1]= nodi_insieme
            return True

        elif insiemeNodo1 == -1 and insiemeNodo2 != -1:
        # 2B. Caso in cui solo uno dei due nodi fa parte di un insieme (nodi invertiti rispetto a 2A)
            nodi_insieme= dizionario_sottoAlberi.pop(insiemeNodo2)
            nodi_insieme.append(nodo1)

            dizionario_sottoAlberi[insiemeNodo2]= nodi_insieme
            return True

        elif insiemeNodo1 != insiemeNodo2 and insiemeNodo1 != -1 and insiemeNodo2 != -1:
        # 3 Caso in cui i nodi fanno parte d'insiemi diversi
            nodi_insieme1= dizionario_sottoAlberi.pop(insiemeNodo1)
            nodi_insieme2= dizionario_sottoAlberi.pop(insiemeNodo2)

            newKey= min(insiemeNodo1,insiemeNodo2)


            dizionario_sottoAlberi[newKey]= nodi_insieme1 + nodi_insieme2
            return True
        
        elif insiemeNodo1 == insiemeNodo2:
            return False

def MinimumSpanningTree(dizionario_citta):
    # Distanza coperta dal'mst
    distanza_mst= 0

    # Lista degli archi usati
    archi_usati= []         # archi_usati[element1,element2,..], element= [nodoA,nodoB, peso arco]  

    
    # Creare un dizionario contenente tutte le distanze verso le altre città  di ogni nodo (citta e deposito)
    dizionario_distanze_citta= calcola_dizionario_distanze(dizionario_citta)

    # Creo lista d'appoggio per evitare di selezionare archi che creerebbero cicli, gli archi che andrò a selezionare non devono collegarsi ad un nodo gia utilizzato
    nodi= list(dizionario_citta.keys())
    nodi.append(0)

    # Lista dei nodi visitati
    nodi_visitati=[]

    
    # Dizionario degli insiemi dei sottoalberi
    dizionario_sottoAlberi= {}

    # Creo dizionario che mi va a tenere traccia degli archi gia utilizzati
    dizionario_uso_archi= {}

    for n in nodi:
        lista_archi=[]
        i = 0
        while i < len(nodi):
            lista_archi.append(0)
            i += 1
        
        dizionario_uso_archi[n]= lista_archi


    n_nodi_considerati= calcola_nodi_visitati(nodi_visitati,nodi)

    # Questo while in combo a calcola_nodi_visitati mi permette di andare a toccare tutti i nodi
    while n_nodi_considerati < len(nodi) or len(dizionario_sottoAlberi) != 1:

        peso_arco, nodo1, nodo2= ricerca_arco_minimo(dizionario_distanze_citta, dizionario_uso_archi)
        


        if verifica_ammissibilita(nodo1,nodo2,dizionario_sottoAlberi):

            lista_distanze_usateN1= dizionario_uso_archi.get(int(nodo1))
            lista_distanze_usateN2= dizionario_uso_archi.get(int(nodo2))

            # Simemtria nel dizionario degli usi
            lista_distanze_usateN1[int(nodo2)]= 1
            print("nodo1: " + str(nodo1))
            print("lista_distanze_usateN2: " + str(lista_distanze_usateN2))
            lista_distanze_usateN2[int(nodo1)]= 1

            if nodo1 not in nodi_visitati:
                nodi_visitati.append(nodo1)
            if nodo2 not in nodi_visitati:
                nodi_visitati.append(nodo2)

            # Aggiorno il numero dei nodi considerati
            n_nodi_considerati= calcola_nodi_visitati(nodi_visitati,nodi)

            archi_usati.append([nodo1,nodo2,peso_arco])

            distanza_mst += peso_arco
        
        else:
            # Caso in cui l'arco visitato creerebbe un ciclo, segno questo arco come non utilizzabile in modo da non ripescarlo
            lista_distanze_usateN1= dizionario_uso_archi.get(int(nodo1))
            lista_distanze_usateN2= dizionario_uso_archi.get(int(nodo2))

            lista_distanze_usateN1[int(nodo2)]= 2   # Valore 2 indica che non è utilizzabile in quanto creerebbe un ciclo, non importa in realtà il valore che gli metto, l'importante è non lasciarlo a 0 in quanto se rimane a 0 dopo viene riselezionato entrando in un loop infinito
            lista_distanze_usateN2[int(nodo1)]= 2

    return dizionario_distanze_citta, dizionario_uso_archi, distanza_mst, archi_usati



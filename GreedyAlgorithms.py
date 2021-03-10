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
        
        print("Percorso: " + str(percorso))
        # Aggiorno le città visitate
        n_citta_visitate= calcola_citta_visitate(percorso,dizionario_citta)
        print("n_citta_visitate: " + str(n_citta_visitate))

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

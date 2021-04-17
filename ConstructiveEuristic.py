import copy
import time
import os
import PlotGenerator as plt
from Cliente import Cliente, euclidean_distance, soluzione_accettabile, calcola_costo
from subprocess import PIPE, Popen

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

# ---------------------------------------- Nearest Neighbour ----------------------------------------

def find_next_node(percorso,current_node,dizionario_citta,dizionario_stazioni):
    min_dist= 10000000

    # Tiro fuori le coordinate del nodo corrente
    if current_node == 0:
        # In questo caso il nodo corrente è il deposito
        current_coordinate= [0,0]
    elif 'S' in str(current_node):
        # In questo caso il nodo corrente è una stazione
        current_station= current_node.replace('S','')
        try:
            current_coordinate= dizionario_stazioni.get(int(current_station))
        except:
            print("current_station: " + str(current_station))
            exit()
    else:
        cliente= dizionario_citta.get(current_node) 
        current_coordinate= cliente.coordinate

    clients= list(dizionario_citta.keys())

    for client in clients:

        if client not in percorso:
            node= dizionario_citta.get(int(client))
            
            # La distanza è approssimata ad intero  da euclidean_distance
            distance= euclidean_distance(node.coordinate,current_coordinate)

            if distance <= min_dist:
                min_dist= distance
                next_node= client
                
    return next_node, min_dist

def calcolo_ricarica(k, node_station, percorso, dizionario_citta, dizionario_stazioni, N_CITIES):
    # print("-----------Dentro calcolo ricarica-----------")
    n_citta_visitate= calcola_citta_visitate(percorso, dizionario_citta)

    autonomia= k
    # print("node_station: " + str(node_station))
    current_node= node_station
    # Fino alla penultima citta, quando arrivo alla penultima città esco dal while, è un caso particolare perchè devo farla arrivare al deposito
    while n_citta_visitate < N_CITIES - 1 :
        # print("current_node: " + str(current_node))
        # print("autonomia_calcolo_ricarica: " + str(autonomia))
        # Se il nodo corrente non è il deposito, prendo l'oggetto cliente relativo
        if current_node != 0 and 'S' not in str(current_node):
            current_client= dizionario_citta.get(current_node)

        next_node, next_distance= find_next_node(percorso,current_node,dizionario_citta,dizionario_stazioni)

        # print("next_node: " + str(next_node))
        # print("next_distance: " + str(next_distance))

        future_autonomy= autonomia - next_distance

        # print("future_autonomy: " + str(future_autonomy))

        next_client= dizionario_citta.get(int(next_node))

        # print("distanza_stazione_next_client: " + str(next_client.distanza_stazione))
        if future_autonomy - next_client.distanza_stazione < 0:
            #print("future_autonomy: " + str(future_autonomy))
            #print("next_client.distanza_stazione: " + str(next_client.distanza_stazione))
            #print("future_autonomy - next_client.distanza_stazione: " + str(future_autonomy - next_client.distanza_stazione))
            node_station= str(current_client.get_quadrant()) + 'S'
            #print("current_client:" + str(current_client.numero))
            percorso.append(node_station) 

            # Calcolo quanta autonomia mi rimane quando arrivo alla prossima stazione, questa autonomia rimanente va scalata dalla ricarica precedente, in modo da evitare sprechi 
            distanza_stazione= current_client.distanza_stazione
            #print("distanza_stazione_corrente: " + str(distanza_stazione))
            autonomia_residua= autonomia - distanza_stazione
            break
        else:

            autonomia -= next_distance

            current_node= next_node

            percorso.append(next_node)

        n_citta_visitate= calcola_citta_visitate(percorso,dizionario_citta)
    
    if n_citta_visitate == N_CITIES - 1:
        if 'S' in str(current_node):
            node_station= current_node.replace("S",""),
            stazioni_coordinate= dizionario_stazioni.get(int(node_station))
            distanza_deposito= euclidean_distance(stazioni_coordinate, [0,0])
            autonomia_residua= autonomia - distanza_deposito
            return autonomia_residua
        else:
            current_client= dizionario_citta.get(current_node)
            if autonomia - current_client.distanza_deposito < 0:

                node_station= str(current_client.get_quadrant()) + 'S'
                distanza_stazione = current_client.distanza_stazione

                autonomia_residua= autonomia - distanza_stazione
                return autonomia_residua

        autonomia_residua= autonomia - current_client.distanza_deposito
        return autonomia_residua

    else:
        return autonomia_residua
    
# Tempo di ricarica è dato da 0.25 unita di tempo per unita metrica di autonomia ricaricata
def NearestNeighbour(dizionario_citta, dizionario_stazioni, k, N_CITIES, Max_Axis):
    tempo_ricarica= 0  #Tempo speso a ricaricare
    distanza_percorsa= 0

    autonomia= k
    percorso= []

    current_node= 0  # 0 è il deposito

    # Il nodo 0 è il deposito
    percorso.append(0)

    n_citta_visitate= calcola_citta_visitate(percorso,dizionario_citta)


    # Fino a quando non ho visitato tutte le citta cerco il prossimo nodo da visitare
    # Sto nel ciclo fino a quando non mi manca di inserire nel percorso l'ultima città da visitare ( Es. N_CITIES= 10, le città sono in tutto 9 perchè 
    # nelle 10 città c'è anche 1 deposito, quindi sto nel ciclo fino a un n di città nel percorso < 9 cioè fino a 8 città, quando aggiungo la 9 e quindi l'ultima esco)
    while n_citta_visitate < N_CITIES - 1:

        # Se il nodo corrente non è il deposito, prendo l'oggetto cliente relativo
        if current_node != 0 and 'S' not in str(current_node):
            current_client= dizionario_citta.get(current_node)

        next_node, next_distance= find_next_node(percorso,current_node,dizionario_citta,dizionario_stazioni)

        future_autonomy= autonomia - next_distance  # Con future_autonomy tengo traccia dell'autonomia futura che avrò nel caso mi spostassi in next_node come prossimo passo 

        next_client= dizionario_citta.get(int(next_node))

        # ------- AMMISSIBILITA' DELLA MOSSA -------------

        # Se l'autonomia rimanente dovuta al prossimo spostamento che vorrei fare, non mi permetterebbe di andare a ricaricare partendo dal next_node
        # significa che non mi dovrò muovere verso il next_node ma dovrò prima andare a ricaricare l'auto 
        # Questa condizione include già anche il caso in cui partendo da una città non si ha autonomia per arrivare alla città più vicina successiva perchè
        # se non ho autonomia per arrivare alla città successiva più vicina  non ho l'autonomia neanche per arrivare alla stazione di ricarica della città successiva
        # E' anche vero però che potrei avere autonomia per arrivare alla città successiva e anche a quella successiva delle successiva ma non per arrivare alla stazione di ricarica a partire dalla successiva
        # Però secondo me come algoritmo costruttivo questo tipo di mossa può essere comunque valida, anche se non è perfettamente precisa

        #------------------------- NB: Forse l'ammissibilita potrei strutturarla  anche così: 
        # Forse avrei dovuto guardare avanti di 2 passi, 1) guardo se nel next_node ho autonomia a sufficienza per andare al next_next_node e in tale nodo ho ancora autonomia per andare a fare la ricarica
        # 2) se non ho autonomia a sufficienza guardo se nel next_node ho autonomia a sufficienza per andare a ricaricare partendo dal next_node
        # 3) se non ho autonomia sufficienza per ricaricare  a partire dal next_node, vado a ricaricare partendo dal current_node
        # ------------------------ Valutazione: Per me può anche andare bene come ho fatto perchè l'importante è che da un algoritmo costruttivo esca una soluzione di media bontà, non necessariamente ottima o molto buona in modo che poi si veda come lavori la LS e la meta euristica successiva
        # (Da Valutare la veridicità) NB: Questa condizione è veritiera solo nel caso in cui le stazioni di ricarica siano al centro di ogni quadrante

        if future_autonomy - next_client.distanza_stazione < 0:
            # In questo caso devo andare a ricaricare nella stazione partendo da current_node

            # Effettuo la ricarica
            # Aggiorno:
            #   - Percorso
            #   - Distanza Percorsa
            #   - Tempo Ricarica
            #   - Autonomia (Piena)       (N.B. Bisogna in futuro valutare quanto ricaricare)
            #   - Nodo Corrente (Stazione)

            node_station= str(current_client.get_quadrant()) + 'S'  # La stazione più vicina è quella del proprio quadrante in quanto è messa in mezzo al quadrante

            distanza_percorsa += current_client.distanza_stazione

            percorso.append(node_station)

            # delta_autonomia mi indica quanto devo ricaricare 

            autonomia -= current_client.distanza_stazione
            delta_ricarica=  k - autonomia

            autonomia= k    # Effettuo ricarica 

            tempo_ricarica += 0.25*delta_ricarica # Aggiorno il tempo impiegato per ricaricare


            current_node= node_station

        else:
            # Sono nel caso in cui lo spostamento al prossimo nodo mi permette di avere un autonomia tale per cui posso poi raggiungere eventualmente la stazione di ricarica a partire da next_node

            distanza_percorsa += next_distance

            autonomia -= next_distance
            current_node= next_node

            percorso.append(next_node)
        
        # print("Percorso: " + str(percorso))
        # Aggiorno le città visitate
        n_citta_visitate= calcola_citta_visitate(percorso,dizionario_citta)
        # print("n_citta_visitate: " + str(n_citta_visitate))

    # ------- FUORI WHILE ---------
    # Quando esco dal while significa che sono andato in tutte le città e non mi resta altro che tornare al deposito 
    # Quando esco dal ciclo sono PER FORZA in una citta e avendo fatto uno spostamento da una citta ad una citta ho autonomia per andare alla stazione di rifornimento di quella citta

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

        autonomia += delta_autonomia 

        tempo_ricarica += 0.25*delta_autonomia

        # 3) Torno al deposito, quindi aggiorno:
        #       - Percorso
        #       - Distanza Percorsa
        percorso.append(0)

        autonomia -= distanza_stazione_deposito

        distanza_percorsa += distanza_stazione_deposito
 
    else:
    # Qui siamo nel caso in cui dall'ultima città si abbia autonomia sufficiente per tornare al deposito       
    # In questo caso devo solo aggiornare:
    #           - Percorso
    #           - Distanza Percorsa
        percorso.append(0)

        distanza_percorsa += current_client.distanza_deposito

    tempo_totale= distanza_percorsa + tempo_ricarica

    plt.draw_map(percorso, dizionario_citta, dizionario_stazioni, Max_Axis, False)


    dizionario_Nearest_Neighbour= {}
    dizionario_Nearest_Neighbour['percorso']= percorso
    dizionario_Nearest_Neighbour['distanza']= distanza_percorsa
    dizionario_Nearest_Neighbour['tempo_tot']= tempo_totale
    dizionario_Nearest_Neighbour['tempo_ricarica']= tempo_ricarica


    return dizionario_Nearest_Neighbour


# ---------------------------------------- NON GREEDY ----------------------------------------
# ---------------------------------------- Christofides_Algorithm ----------------------------------------
# Per MST
def calcola_dizionario_distanze(dizionario_citta):
    dizionario_distanze_citta= {}
    citta= list(dizionario_citta.keys())
    
    lista_distanze_deposito= [0]

    for n in citta:
        current_node= dizionario_citta.get(int(n))
        distanza_deposito= current_node.distanza_deposito
        distanza_deposito= round(distanza_deposito,2)
        lista_distanze_deposito.append(distanza_deposito)

    dizionario_distanze_citta[0]= lista_distanze_deposito

    for n in citta:
        lista_distanze= []
        current_node= dizionario_citta.get(int(n))
        current_coordinate= current_node.coordinate
        
        # Siccome è la prima iterazione, aggiungo la distanza del nodo al deposito
        distanza_deposito= current_node.distanza_deposito
        distanza_deposito= round(distanza_deposito,2)

        lista_distanze.append(distanza_deposito)

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

    return dizionario_distanze_citta

def create_distance_dict(dizionario_citta):
    G= {}

    citta= list(dizionario_citta.keys())
    
    collegamenti={}
    for citt in citta:
        coord1= dizionario_citta.get(citt)
        coordinate1= coord1.coordinate

        collegamenti[citt]= euclidean_distance([0,0],coordinate1)
    
    G[0]= collegamenti

    for citt in citta:
        collegamenti={}
        if 0 not in citta:
            citta.insert(0,0)
        
        for citt2 in citta:
            if citt2 != citt:
                if citt2 == 0:
                    coordinate2= [0,0]
                else:
                    coord2= dizionario_citta.get(citt2)
                    coordinate2= coord2.coordinate

                coord1= dizionario_citta.get(citt)
                coordinate1= coord1.coordinate


                collegamenti[citt2]= euclidean_distance(coordinate1, coordinate2)
        
        G[citt]= collegamenti
    
    return G

# L'ammissibilità dell' arco trovato qui viene determinata da MinimumSpanningTree
def ricerca_arco_minimo_mst(dizionario_distanze_citta, dizionario_uso_archi):

    # print("Dizionario_distanze_citta: " + str(dizionario_distanze_citta))
    # print("Dizionario_uso_archi: "+ str(dizionario_uso_archi))
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

# Differisce dall'arco minimo mst in quanto il dizionario che gli passo è un dizionario di dizionari e non un dizionario di liste
# Anche qui l'ammissibilità viene verificata dalla funzione che contiene questa
def ricerca_arco_minimo_perfectMatching(subgraph, archi_usati):
    nodi= list(subgraph.keys())

    dist_min= 100000000000000

    nodo1= -1
    nodo2= -1

    for nodo in nodi:

        archi_usati_dizionarioNodo= archi_usati.get(int(nodo))

        altri_nodi= list(archi_usati_dizionarioNodo.keys())

        for key in altri_nodi:
            if int(archi_usati_dizionarioNodo.get(key)) == 0: # Se è uguale a 0 vuol dire che questo arco non l'ho ancora usato 
                
                dizionario_distanze_nodo= subgraph.get(int(nodo))

                peso_arco= int(dizionario_distanze_nodo.get(int(key)))

                if peso_arco <= dist_min:
                    dist_min= peso_arco
                    nodo1= int(nodo)
                    nodo2= int(key)

    return dist_min, nodo1, nodo2

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
        
        elif insiemeNodo1 == insiemeNodo2 and insiemeNodo1 != -1 and insiemeNodo2 != -1:
            return False

def find_odd_degree_verteces(nodi,archi_usati):

    dizionario_incidenze= {}

    odd_degree_verteces_list= []

    # Mi segno per ogni nodo quanti archi sono collegati ad esso
    for nodo in nodi:
        occ= 0

        for arco in archi_usati:
            if nodo == arco[0] or nodo == arco[1]:
                occ += 1

        dizionario_incidenze[nodo]= occ
    
    for nodo in nodi:
        if int(dizionario_incidenze.get(nodo)) % 2 != 0:   # Se dividendo il numero per due non ho un resto uguale a 0 allora è dispari
            odd_degree_verteces_list.append(nodo)
    

    return odd_degree_verteces_list

def find_greater_2_degree_verteces(dict_multi_graph_s, dizionario_citta):
    vertex_greater_2_degree= []
    # CERCARE I DOPPI ARCHI TRA 2 VERTICI
    nodes= list(dict_multi_graph_s.keys())

    for node in nodes: 

        vertex2_dict= dict_multi_graph_s.get(node)
        vertex2_keys= list(vertex2_dict.keys())

        # Le chiavi di vertex2_dict sono i vertici con cui node compone gli archi a cui è incidente, oltre a questi nodi bisogna andare a controllare la lunghezza della lista delle distanze
        # Generalmente tra due stessi vertici c'è solo un arco, può capitare però, dopo aver reso i vertici di grado dispari in grado pari, che tra due stessi vertici ci sia più di un arco che li collega,
        # perciò devo sommare a vertex_degree anche gli eventuali archi tra due stessi vertici
        vertex_degree= len(vertex2_keys)

        for key in vertex2_keys:
            vertex2_distance= vertex2_dict.get(key)
            if len(vertex2_distance) > 1:
                vertex_degree += len(vertex2_distance) - 1    # Se len(verte2_distance) == 2 significa che ci sono due stessi archi tra gli stessi due vertici, siccome un arco l'ho gia contato ( con vertex_degree= len(vertex2_keys) ), allora a vertex_degree dovrò sommare solo: len(vertex2_distance) - 1

        # Se vertex_degree è > 2 allora devo inserire node nella lista da restituire
        if vertex_degree > 2:
            vertex_greater_2_degree.append(node)

    return vertex_greater_2_degree

def MinimumSpanningTree(dizionario_citta):
    # Distanza coperta dal'mst
    distanza_mst= 0

    # Lista degli archi usati
    archi_usati= []         # archi_usati[element1,element2,..], element= [nodoA,nodoB, peso arco]  

    
    # Creare un dizionario contenente tutte le distanze verso le altre città  di ogni nodo (citta e deposito)
    dizionario_distanze_citta= calcola_dizionario_distanze(dizionario_citta)

    # Creo lista d'appoggio per evitare di selezionare archi che creerebbero cicli, gli archi che andrò a selezionare non devono collegarsi ad un nodo gia utilizzato
    nodi= list(dizionario_citta.keys())
    nodi.insert(0,0)    # !!! Modificato, prima era nodi.appen(0), così facendo però si aggiunge in coda lo 0

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

        peso_arco, nodo1, nodo2= ricerca_arco_minimo_mst(dizionario_distanze_citta, dizionario_uso_archi)
        

        if verifica_ammissibilita(nodo1,nodo2,dizionario_sottoAlberi):

            lista_distanze_usateN1= dizionario_uso_archi.get(int(nodo1))
            lista_distanze_usateN2= dizionario_uso_archi.get(int(nodo2))

            # Simemtria nel dizionario degli usi
            lista_distanze_usateN1[int(nodo2)]= 1
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

    # return dizionario_distanze_citta, dizionario_uso_archi, distanza_mst, archi_usati
    return archi_usati

def find_perfect_matching(subgraph):
    # Un perfect matching graph è un insieme di archi indipendenti( ovvero che questi archi  non devono condividere vertici in comune ) che vanno a considerare tutti i vertici
    # Il perfect matching graph che voglio trovare è quello di costo minimo

    perfect_matching= []
    distanza_perfect_matching= 0

    nodi= list(subgraph.keys())

    # Archi_usati tiene conto gli archi utilizzati
    archi_usati= {}
    
    # nodi_usati tiene traccia della copertura dei nodi
    nodi_usati= []

    # Inizializzo il dizionario che tiene dietro gli archi utilizzati, stessa procedura usata per creare l'MST
    for n in nodi:
        peso_archi= {}

        for i in nodi:
            if i != n:
                peso_archi[i]= 0

        archi_usati[n]= peso_archi

    n_nodi_visitati = calcola_nodi_visitati(nodi_usati, nodi)

    while n_nodi_visitati < len(nodi):

        peso_arco_minimo, nodo1, nodo2= ricerca_arco_minimo_perfectMatching(subgraph, archi_usati)

        # Verifico ammissibilità dell'arco minimo, ovvero l'arco deve comprendere due nodi che non sono stati ancora toccati
        if nodo1 not in nodi_usati and nodo2 not in nodi_usati:
            nodi_usati.append(nodo1)
            nodi_usati.append(nodo2)

            # Segno che tale arco è usato

            diz_archi_usati1= archi_usati.get(nodo1)
            diz_archi_usati1[nodo2]= 1  
            # Simmetria dell'uso degli archi
            diz_archi_usati2= archi_usati.get(nodo2)
            diz_archi_usati2[nodo1]= 1
        
            n_nodi_visitati = calcola_nodi_visitati(nodi_usati, nodi)

            perfect_matching.append([nodo1, nodo2, peso_arco_minimo])
            distanza_perfect_matching += peso_arco_minimo

        else:
            # Se sono qui significa che almeno uno dei due nodi era gia stato "toccato" da un'altro arco
            diz_archi_usati1= archi_usati.get(nodo1)
            diz_archi_usati1[nodo2]= 2  
            # Simmetria dell'uso degli archi
            diz_archi_usati2= archi_usati.get(nodo2)
            diz_archi_usati2[nodo1]= 2

    return perfect_matching

# CreateDictGraph mi crea un dizionario che tiene conto di tutti gli archi nati dall'unione 
def createDictGraph(perfect_matching_graph, mst_graph, dizionario_citta):
    
    dict_multi_graph_s= {}
    multi_graph_nodes= list(dizionario_citta.keys())
    multi_graph_nodes.append(0)

    # Inizializzo i nodi nel grafo
    for node in multi_graph_nodes: 
        dict_list= {}   
        dict_multi_graph_s[node]= dict_list

    # Ora devo assegnare i vari archi ai nodi
    # Archi del Perfect-Matching
    # associo un dizionario vuoto ad ogni arco del perfect matching
    for edge in perfect_matching_graph:
        # Per ogni arco
        dict_list= dict_multi_graph_s[edge[0]] # arco identificato dal primo nodo
        dict_list_nodes= list(dict_list.keys())

        # Se un arco tra i due nodi esiste gia, faccio l'append e aggiungo la distanza del secondo arco ( che dovrebbe avere distanza uguale ) 
        if edge[1] in dict_list_nodes:
            dict_list[edge[1]].append(int(edge[2]))
        else:
            # Se un arco tra i due nodi non esiste, creo una lista con la distanza di un arco soltanto
            distanza= [edge[2]]
            dict_list[edge[1]]= distanza

        # Devo fare il simmetrico
        dict_list2= dict_multi_graph_s[edge[1]]
        dict_list_nodes2= list(dict_list2.keys())

        if edge[0] in dict_list_nodes2:
            dict_list2[edge[0]].append(int(edge[2]))
        else:
            # Se un arco tra i due nodi non esiste, creo una lista con la distanza di un arco soltanto
            distanza= [edge[2]]
            dict_list2[edge[0]]= distanza

    # Archi del MST
    for edge in mst_graph:
        dict_list= dict_multi_graph_s[edge[0]]

        dict_list_nodes= list(dict_list.keys())

        # Se un arco tra i due nodi esiste gia, faccio l'append e aggiungo la distanza del secondo arco ( che dovrebbe avere distanza uguale ) 
        if edge[1] in dict_list_nodes:
            dict_list[edge[1]].append(int(edge[2]))
        else:
            # Se un arco tra i due nodi non esiste, creo una lista con la distanza di un arco soltanto
            distanza= [int(edge[2])]
            dict_list[edge[1]]= distanza

        # Devo fare il simmetrico
        dict_list2= dict_multi_graph_s[edge[1]]
        dict_list_nodes2= list(dict_list2.keys())

        if edge[0] in dict_list_nodes2:
            dict_list2[edge[0]].append(int(edge[2]))
        else:
            # Se un arco tra i due nodi non esiste, creo una lista con la distanza di un arco soltanto
            distanza= [int(edge[2])]
            dict_list2[edge[0]]= distanza

    return dict_multi_graph_s

# Controlla che se si tolgono gli archi (u,v),(v,w) e aggiungendo (u,w) il multigrafo rimane connesso
def check_connection_multigraph(u,w,v,archi_v,dict_multi_graph_s):
    node_v= copy.deepcopy(archi_v)

    new_dict= copy.deepcopy(dict_multi_graph_s)

    # Cancello arco (v,u)  NB!!! Se però ci sono due archi v,u in un colpo solo li tolgo tutti e due , ed è sbagliato perchè dopo avrò che il grafo potrebbe non essere connesso
    edge_v_u= node_v.pop(u)
    if len(edge_v_u) > 1:
        # print("edge_v_u dentro check: " + str(edge_v_u))
        edge_v_u= edge_v_u[0:-1] # cancello un arco
        node_v[u]= edge_v_u # reinserisco l'arco
    # Se la condizione non è verificata ho semplicemente effettuato la pop e quindi cancellato il singolo arco

    # cancello arco (v,w)
    edge_v_w= node_v.pop(w)
    if len(edge_v_w) > 1:
        edge_v_w= edge_v_w[0:-1]
        node_v[w]= edge_v_w
    
    # una volta aggiornato i collegamenti di v ( che sono le chiavi del dizionario che tiro fuori con new_dict.pop(v)) reinserisco il nodo v nel dizionario
    new_dict[v]= node_v

    # tolto gli archi (uv), (vw) e aggiungo (u,w)
    node_u= new_dict.pop(u)

    # devo togliere anche qui gli archi tolti da node_v
    if len(node_u[v]) > 1:
        edge_u_v= node_u.pop(v)
        edge_u_v= edge_u_v[0:-1]
        node_u[v]= node_u
    else:
        node_u.pop(v)
    # Al nodo u inserisco il collegamento con w ( e poi faro il viceversa), per aggiungere questo collegamento basta aggiungere la chiave w , l'importante è che ci sia la chiave, il valore corrispettivo a tale chiave non è importante
    # perchè qui devo solo guardare i nodi, non i valori degli archi
    node_u[w]= 1000
    new_dict[u]= node_u
    

    node_w= new_dict.pop(w)

    if len(node_w[v]) > 1:
        edge_w_v= node_w.pop(v)
        edge_w_v=  edge_w_v[0:-1]
        node_w[v]= edge_w_v
    else:
        node_w.pop(v)
    

    node_w[u]= 1000
    new_dict[w]= node_w

    # Ora che ho sistemato i collegamenti nel dizionario di prova, verifico che il grafo sia connesso
    # Creo uno stack, parto da un nodo (in questo caso da v)
    # Creo una lista, dove l'indice indica il nodo e il valore indica se tale nodo è stato visitato, se è stato visitato vale 1 altrimento 0
    nNodi= len(dict_multi_graph_s.keys()) + 1 # + 1 perchè prima di passare dict_multi_graph_s a questa funzione viene fatta una pop su di esso ( node_v )
    nodi_visitati=[]
    i= 0
    while i < nNodi:
        nodi_visitati.append(0)
        i += 1
    
    # print("nodi_visitati: " + str(nodi_visitati))
    # Vado a leggere il primo valore nello stack, inserisco nello stack tutti i nodi che non sono gia presenti nello stack  a cui v è collegato e che non sono gia stati visitati
    # Una volta inseriti i nodi non ancora visitati nello stack, faccio il pop del valore appena letto e lo segno come visitato
    stack= [int(v)]

    while len(stack) > 0:
        # print("stack: " + str(stack))
        # Tiro fuori il primo nodo nello stack
        node= stack.pop(0)
        # Lo segno come visitato
        nodi_visitati[node]= 1

        # Ora devo andare a mettere i nodi a cui node è collegato nello stack, in questo stack ci vanno i nodi che non sono stati ancora visitati e che ancora non sono nello stack
        linked_node_dict= new_dict.get(node)

        linked_node_list= list(linked_node_dict.keys())

        for el in linked_node_list:
            if nodi_visitati[el] == 0 and el not in stack:
                stack.append(int(el))
    
    # Quando non ho più nodi nello stack esco dal while, ora controllo la lista nodi_visitati, se sono tutti a 1 allora il grafo è collegato, se c'è un nodo a 0 significa che non è stato visitato e quindi il grafo non è collegato
    
    if 0 in nodi_visitati:
        # print("False")
        return False
    else:
        # print("True")
        return True

# def create_christofides_graph(perfect_matching_graph, mst_graph, dizionario_citta, Max_Axis):
def create_christofides_graph(mst_graph, G, dizionario_citta, Max_Axis):    

    # print("Grafo G: " + str(G))

    # Devo creare dict_multi_graph_s, un dizionario contenente gli archi del mst_graph
    dict_multi_graph_s= {}

    for edge in mst_graph:
        multi_graph_s_keys= list(dict_multi_graph_s.keys())
        # print("keys: " + str(multi_graph_s_keys))
        # print("edge: " + str(edge))
        if edge[0] not in multi_graph_s_keys:
            # Se l'arco non è nel dizionario lo inserisco
            arco= {}
            arco[edge[1]]= [edge[2]]
            dict_multi_graph_s[edge[0]]= arco
        else:
            # Se il primo nodo di un arco è nel dizionario, vado ad aggiornare gli archi che questo nodo compone
            dizionario_archi= dict_multi_graph_s.pop(edge[0])
            edge2_list= list(dizionario_archi.keys()) # edge2_list è la lista delle chiavi che identificano l'altro estremo degli archi che edge[0] compone

            if edge[1] in edge2_list:
                # Questo è il caso in cui esistano 2 archi che collegano gli stessi due vertici, situazione che può nascere quando precedentemente si è voluto rendere i vertici di grado dispari in vertici di grado pari.
                # Questo è il motivo per cui le distanze vengono salvate all'interno dei dizionari come liste, in modo che possa vedere se esistono degli archi doppi ( liste di lunghezza 2 ) 
                dizionario_archi[edge[1]].append(edge[2])
            else:
                dizionario_archi[edge[1]]= [edge[2]]

            # Una volta aggiornato dizionario_archi, lo reinserisco
            dict_multi_graph_s[edge[0]]= dizionario_archi


        # Siccome un arco è composto da 2 vertici e avendo lavorato su un solo vertice, ora devo fare il simmetrico

        if edge[1] not in multi_graph_s_keys:
            arco= {}
            arco[edge[0]]= [edge[2]]
            dict_multi_graph_s[edge[1]]= arco
        else:
            dizionario_archi= dict_multi_graph_s.pop(edge[1])
            edge2_list= list(dizionario_archi.keys())

            if edge[0] in edge2_list:
                dizionario_archi[edge[0]].append(edge[2])
            else:
                dizionario_archi[edge[0]]= [edge[2]]
            
            dict_multi_graph_s[edge[1]]= dizionario_archi
    
    # Fine Creazione dict_multi_graph_s , che è un dizionario di dizionari contente gli archi di mst_graph, in poche parole è il dizionario che rappresenta mst_graph

    plt.draw_multigraph(dict_multi_graph_s, dizionario_citta, Max_Axis)
    
    # 1)Per prima cosa devo trovare i nodi con grado > 2
    greater_2_verteces= find_greater_2_degree_verteces(dict_multi_graph_s, dizionario_citta)

    # n modo iterativo, 
	# ∀ nodo v di grado >2, 
	# - considera la coppia di archi (u,v) e (v,w) in S che massimizza cuv+cvw–cuw, con (u,w)∉S, mantenendo la connessione, 
	# - sostituisci gli archi (u,v) e (v,w) con l’arco (u,w), garantendo la connessione di S 



    # Per ogni vertice v di grado > 2 vado a prendere i due archi (u,v) e (v,w) che massimizzano C(u,v) + C(v,w) - C(u,w), con (u,w) non appartenente al multigrafo S

    for vertex in greater_2_verteces:

        max_cost= -10000000000000000000
        weight_edge_U_W= 0
        U= -1
        V= -1
        W= -1

        archi_v= dict_multi_graph_s.pop(int(vertex))
        nodi2_list= list(archi_v.keys())

        for u in nodi2_list:

            weight_u_v=  list(archi_v.get(int(u)))
            weight_edge_u_v= weight_u_v[0]
            for w in nodi2_list:
                # Verifico che (u,w) non faccia parte del multigrafo


                archi_u= dict_multi_graph_s.get(int(u))
                nodi2_u_list= list(archi_u.keys())

                if w not in nodi2_u_list:
                    # Qui devo verificare che se togliessi u,v e v,w aggiungendo u,w il grafo rimarrebbe connesso, se non rimane connesso la scelta va scartata
                    if w != u and check_connection_multigraph(u,w,vertex,archi_v,dict_multi_graph_s):
                        weight_v_w= list(archi_v.get(int(w)))
                        weight_edge_v_w= weight_v_w[0]
                        if u == 0:
                            coordinate_u= [0,0]
                        else:
                            coord_u= dizionario_citta.get(int(u))
                            coordinate_u= coord_u.coordinate
                        
                        if w == 0:
                            coordinate_w= [0,0]
                        else:
                            coord_w= dizionario_citta.get(int(w))
                            coordinate_w=coord_w.coordinate

                        weight_edge_u_w= euclidean_distance(coordinate_u,coordinate_w)  

                        cost= weight_edge_u_v + weight_edge_v_w - weight_edge_u_w
                        
                        if cost >= max_cost:
                            max_cost= cost
                            U= u
                            V= vertex
                            W= w
                            weight_edge_U_W= weight_edge_u_w

        # Finito il ciclo tra gli archi vado a cancellare gli archi che devo cancellare (u,v) e (v,w) e aggiungere l'arco che devo aggiungere (u,w)

        if U != -1 and W != -1:
            # Cancello (v,u)
            arco_v_u= archi_v.pop(U)

            # Se ci sono due stessi archi ne elimino solo 1 e l'altro lo lascio
            if len(arco_v_u) > 1:
                archi_v[U]= [arco_v_u[0]]

            # cancello il simmetrico(u,v) 

            archi_u= dict_multi_graph_s.pop(int(U))
            
            arco_u_v= archi_u.pop(V)

            if len(arco_u_v) > 1:
                archi_u[V]= [arco_u_v[0]]

            # Aggiungo l'arco (u,w)
            archi_u[W]= [weight_edge_U_W]
            dict_multi_graph_s[U]= archi_u

            # Cancello (v,w)
            arco_v_w= archi_v.pop(W)

            if len(arco_v_w) > 1:
                archi_v[W]= [arco_v_w[0]]
            
            # cancello il simmetrico(w,v)
            archi_w= dict_multi_graph_s.pop(int(W))
            arco_w_v= archi_w.pop(V)

            if len(arco_w_v) > 1:
                archi_w[V]= [arco_w_v[0]]
            
            # Aggiungo l'arco (w,u)
            archi_w[U]= [weight_edge_U_W]
            dict_multi_graph_s[W]= archi_w

            dict_multi_graph_s[V]= archi_v
        else:
            print("!!!1!1FALZOOOOOOOOOO!!!!")
            time.sleep(5)

    return dict_multi_graph_s

def create_green_graph1(christofides_graph_no_recharge, dizionario_stazioni, dizionario_citta, k):
    # Devo partire dal deposito, la direzione scelta  è quella del collegamento più corto 
    autonomia= k
    tempo_ricarica= 0
    distanza_percorsa= 0
    
    percorso = [0]

    current_node= 0

    # La scelta di andare nella stazione di ricarica è tale e quale a quella della nearest neighbour, se lo spostamento mi porterebbe in una citta e rimanessi con un'autonomia non sufficiente ad arrivare alla stazione di ricarica di quel quadrante
    # allora prima di andare in quella città vado in una stazione di rifornimento e mi ricarico. Qui posso vedere quanto ricaricare, tale scelta la posso fare nella seguente maniera:
    # Ipotizzo di fare una ricarica piena, proseguo nel mio tragitto e verifico quanta autonomia mi rimarrebbe nel momento in cui dovrò andare a fare una ricarica,
    # La ricarica che quindi farò sarà pari a: Autonomia piena - Autonomia rimanente di quando sarò nella stazione di ricarica futura

    # Devo scegliere come secondo nodo (per dare una direzione di percorrenza) il nodo più vicino
    min_dist= float("inf")   # qualsiasi numero è inferiore a floag("inf")  ( ma non superiore )
    dict_nodo_dep= christofides_graph_no_recharge.get(int(current_node))

    linked_nodes= list(dict_nodo_dep.keys())

    previous_node= current_node

    # Cerco il nodo più vicino al deposito
    for node in linked_nodes:
        dist_node= dict_nodo_dep.get(int(node))
        if dist_node[0] <= min_dist:
            min_dist = dist_node[0]
            current_node= node

    autonomia -= min_dist
    distanza_percorsa += min_dist

    # Ciclo fino a quando non ritorno al  nodo di partenza, ovvero il nodo 0 ( deposito )
    while current_node != 0:

        percorso.append(current_node)

        # print("current_node: " + str(current_node))
        # !!!!!!! probabilmente sbaglio a leggere le distanze qui !!!!!!!!!!!!!!!!!!!!!!! come fa ad esserci una stazione qui come nodo corrente?? e sopratutto non ci sono chiavi con 'S' dentro
        if 'S' not in str(current_node):
            dict_current_node= christofides_graph_no_recharge.get(int(current_node))
        else:
            dict_current_node= christofides_graph_no_recharge.get(current_node)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        linked_nodes= list(dict_current_node.keys())

        for node in linked_nodes:
            if node != previous_node:
                next_node= node

        # print("current_node: " + str(current_node))
        # print("dict_current_node: " +  str(dict_current_node))


        #     distanza_next_node= dict_current_node.get(int(next_node))
        # ValueError: invalid literal for int() with base 10: '2S'

        distanza_next_node= dict_current_node.get(int(next_node))
        future_autonomy= autonomia - distanza_next_node[0]

        # Se il prossimo nodo è il deposito ( termine Tour ) 
        if next_node == 0:
            if 'S' in str(current_node):    # Se al deposito ci arrivo da una stazione di ricarica
                current_node= current_node.replace("S","")
                coordinate_current_node= dizionario_stazioni.get(int(current_node))
            else:   # Se al deposito ci arrivo da una citta
                current_citta= dizionario_citta.get(current_node)
                coordinate_current_node= current_citta.coordinate

            distanza_stazione_next_node= euclidean_distance([0,0],coordinate_current_node)
        
        else: # Caso in cui il prossimo nodo non sia il deposito
            next_citta= dizionario_citta.get(next_node)
            distanza_stazione_next_node= next_citta.distanza_stazione
        
        # Nel caso sia l'ultimo nodo e devo andare verso il deposito, distanza_stazione_next_node è la distanza dall'ultimo nodo/ricarica al deposito

        # Vado alla stazione di ricarica se andando nel next_node avrò un autonomia che non mi permetterà di andare a ricaricare quando sarò al next node oppure se da current node non ho abbastanza autonomia per raggiungere next_node
        if future_autonomy < distanza_stazione_next_node or autonomia < distanza_next_node[0]:

            # Per inserire la stazione di ricarica nel percorso devo togliere next_node da dict_current_node e aggiungere la stazione di ricarica e viceversa,
            # ovvero, dal dizionario di next_node devo togliere current_node e aggiungerci la stazione di ricarica

            quadrante= dizionario_citta.get(current_node).get_quadrant()

            # Tolgo i collegamenti con il nodo futuro e viceversa
            dict_current_node.pop(next_node)

            dict_next_node= christofides_graph_no_recharge.get(int(next_node))
            dict_next_node.pop(int(current_node))

            # Aggiungo il collegamento con la stazione
            distanza_current_node_stazione= dizionario_citta.get(current_node).distanza_stazione
            next_key= str(quadrante) + 'S'
            dict_current_node[next_key]= [distanza_current_node_stazione]

            # Aggiungo il collegamento con la stazione anche nel nodo successivo
            dict_next_node[next_key]= [distanza_stazione_next_node]

            # Ora devo aggiungere la stazione nel dizionario
            distanze_stazione={}
            
            distanze_stazione[current_node]= [distanza_current_node_stazione]
            distanze_stazione[next_node]= [distanza_stazione_next_node]
            christofides_graph_no_recharge[next_key]= distanze_stazione

            # Calcolo il tempo di ricarica
            tempo_ricarica += (k - autonomia) * 0.25
            # Per ora ricarico completamente l'autonomia    
            autonomia= k
            distanza_percorsa += distanza_current_node_stazione
            previous_node= current_node
            current_node= next_key
        else:

            previous_node= current_node
            current_node= next_node
            autonomia = future_autonomy
            distanza_percorsa += distanza_next_node[0]

    percorso.append(0)
    tempo_totale= tempo_ricarica + distanza_percorsa
    return christofides_graph_no_recharge, distanza_percorsa, tempo_ricarica, percorso, tempo_totale



def crea_dizionario_percorso(percorso, dizionario_citta, dizionario_stazioni):

    dizionario_percorso={}

    dizionario_arco={}

    for i in range(0,len(percorso) - 1):
        dizionario_arco= {}
        node1= percorso[i]
        node2= percorso[i + 1]

        chiavi_dizionario_percorso= list(dizionario_percorso.keys())

        if 'S' not in str(node1) and 'S' not in str(node2):
            
            if node1 == 0:
                coordinate_nodo1= [0,0]
            else:
                citta1= dizionario_citta[int(node1)]
                coordinate_nodo1= citta1.coordinate
            

            if node2 == 0:
                coordinate_nodo2= [0,0]

            else: 
                citta2= dizionario_citta[int(node2)]
                coordinate_nodo2= citta2.coordinate
            
        
            distanza= euclidean_distance(coordinate_nodo1, coordinate_nodo2)


            if int(node1) not in chiavi_dizionario_percorso:
                dizionario_arco[int(node2)]= [distanza]
                dizionario_percorso[int(node1)]= dizionario_arco
            else: 
                dizionario_arco= dizionario_percorso.pop(int(node1))
                dizionario_arco[int(node2)]= [distanza]

                dizionario_percorso[int(node1)]= dizionario_arco

            dizionario_arco={}

            if int(node2) not in chiavi_dizionario_percorso:
                dizionario_arco[int(node1)]= [distanza]
                dizionario_percorso[int(node2)]= dizionario_arco
            else:
                dizionario_arco= dizionario_percorso.pop(int(node2))
                dizionario_arco[int(node1)]= [distanza]

                dizionario_percorso[int(node2)]= dizionario_arco

        elif 'S' in str(node1) and 'S' not in str(node2):
            
            stazione1= node1.replace('S','')
            coordinate_nodo1= dizionario_stazioni[int(stazione1)]
            
            if node2 == 0:
                coordinate_nodo2= [0,0]

            else: 
                citta2= dizionario_citta[int(node2)]
                coordinate_nodo2= citta2.coordinate


            distanza= euclidean_distance(coordinate_nodo1, coordinate_nodo2)


            if node1 not in chiavi_dizionario_percorso:
                dizionario_arco[int(node2)]= [distanza]
                dizionario_percorso[node1]= dizionario_arco
            else: 
                dizionario_arco= dizionario_percorso.pop(node1)
                dizionario_arco[int(node2)]= [distanza]

                dizionario_percorso[node1]= dizionario_arco

            dizionario_arco={}

            if int(node2) not in chiavi_dizionario_percorso:
                dizionario_arco[node1]= [distanza]
                dizionario_percorso[int(node2)]= dizionario_arco
            else:
                dizionario_arco= dizionario_percorso.pop(int(node2))
                dizionario_arco[node1]= [distanza]

                dizionario_percorso[int(node2)]= dizionario_arco

        elif 'S' not in str(node1) and 'S' in str(node2):

            if node1 == 0:
                coordinate_nodo1= [0,0]
            else:
                citta1= dizionario_citta[int(node1)]
                coordinate_nodo1= citta1.coordinate

            stazione2= node2.replace('S','')
            coordinate_nodo2= dizionario_stazioni[int(stazione2)]


            distanza= euclidean_distance(coordinate_nodo1, coordinate_nodo2)


            if int(node1) not in chiavi_dizionario_percorso:
                dizionario_arco[node2]= [distanza]
                dizionario_percorso[int(node1)]= dizionario_arco
            else: 
                dizionario_arco= dizionario_percorso.pop(int(node1))
                dizionario_arco[node2]= [distanza]

                dizionario_percorso[int(node1)]= dizionario_arco


            dizionario_arco={}

            if node2 not in chiavi_dizionario_percorso:
                dizionario_arco[int(node1)]= [distanza]
                dizionario_percorso[node2]= dizionario_arco
            else:
                dizionario_arco= dizionario_percorso.pop(node2)
                dizionario_arco[int(node1)]= [distanza]

                dizionario_percorso[node2]= dizionario_arco
    
    return dizionario_percorso


def create_green_graph(christofides_graph_no_recharge, dizionario_stazioni, dizionario_citta, k):

    percorso=[0]
    autonomia= k
    distanza_percorsa= 0
    tempo_ricarica= 0

    current_node= 0
    current_dict= christofides_graph_no_recharge[current_node]

    visited_station= 0
    last_node_flag= 0

    # Ora cerco il prossimo nodo
    # Per dare un verso al grafo scelgo l'arco più corto
    min_dist= float("inf")   # qualsiasi numero è inferiore a floag("inf")  ( ma non superiore )
    linked_nodes= list(current_dict.keys())

    # Cerco il nodo più vicino al deposito
    for node in linked_nodes:
        dist_node= current_dict.get(int(node))
        if dist_node[0] <= min_dist:
            min_dist = dist_node[0]
            current_node= node


    # avendo trovato il primo nodo, mi segno l'ultimo nodo del percorso
    for node in linked_nodes:
        if node != current_node:
            last_node= int(node)

    # posso aggiungere gia il nuovo nodo alla lista

    percorso.append(current_node)

    # aggiorno contatori    
    autonomia -= min_dist
    distanza_percorsa += min_dist

    while current_node != 0:

        #print("percorso: " + str(percorso))

        # Cerco il nodo futuro

        if last_node_flag == 1:
            
            current_dict= christofides_graph_no_recharge[current_node] #current_dict è anche l'ultimo nodo

            next_node= 0
            next_distance= current_dict[next_node]
            next_dist= next_distance[0]

        elif visited_station == 0 : # Se l'ultimo nodo visitato non è una stazione e non è l'ultimo nodo del percorso (e se siamo qui vuol dire che il nodo corrente non è l'ultimo)

            # current_node= int(percorso[-1])
            current_dict= christofides_graph_no_recharge[current_node]

            linked_nodes= list(current_dict)
            
            # In linked nodes ci sono solo 2 nodi, uno è il precedente ed uno è il successivo, il precedente è gia in percorso, io ho bisogno del successivo
            for node in linked_nodes: 
                if node not in percorso:
                    next_node= node
                    next_distance= current_dict[node]
                    next_dist= next_distance[0]

        elif visited_station == 1:   # Se l'ultimo nodo visitato è una stazione

            current_node= int(percorso[-2]) # nodo precedente alla stazione
            current_dict= christofides_graph_no_recharge[current_node]

            linked_nodes= list(current_dict)
                        
            for node in linked_nodes: 
                if node not in percorso:
                    next_node= node
                    
                    # Se l'ultimo nodo visitato è una stazione la prossima distanza sarà la distanza tra tale stazione e il next_node
                    last_station= str(percorso[-1])
                    stazione= int(last_station.replace('S',''))

                    coordinate_stazione= dizionario_stazioni[stazione]

                    next_city= dizionario_citta[int(next_node)]
                    coordinate_next_node= next_city.coordinate

                    next_dist= euclidean_distance(coordinate_stazione, coordinate_next_node)

                    break  # possiamo subito uscire dal for perchè tanto ce ne è solo uno di nodo non nel percorso

        # Devo separare due casi:
        #  1) caso finale che devo confrontare l'autonomia futura con la distanza del nodo corrente dal deposito
        #  2) caso in cui non si è alla fine dove devo confrontare l'autonomia futura che avrò nel next node se sarà sufficiente ad arrivare alla stazione del next_node dal next_node
        
        # Caso 1)
        if next_node == 0: 
            current_city= dizionario_citta[int(current_node)]
            distanza_deposito= current_city.distanza_deposito

            if distanza_deposito > autonomia: # in questo caso prima di andare al deposito devo fermarmi ad una stazione di ricarica e ricaricare solo dell'autonomia necessaria per arrivare al deposito
                distanza_stazione= current_city.distanza_stazione

                # cerco la stazione della città corrente
                quadrante= str(current_city.get_quadrant())
                stazione_current_city= quadrante + 'S'

                # aggiungo la stazione al percorso
                percorso.append(stazione_current_city)

                # aggiorno i contatori

                autonomia -= distanza_stazione
                distanza_percorsa += distanza_stazione
                
                # Ora devo trovare la distanza stazione-deposito

                coordinate_stazione= dizionario_stazioni[int(quadrante)]
                
                distanza_stazione_deposito= euclidean_distance(coordinate_stazione,[0,0])

                # distanza_stazione_deposito è anche quanto devo caricare

                # autonomia= distanza_stazione_deposito

                #print("\ntempo_ricarica prima della ricarica: " + str(tempo_ricarica))
                #print("tempo per questa ricarica: " + str((distanza_stazione_deposito - autonomia) * 0.25))
                
                tempo_ricarica += (distanza_stazione_deposito - autonomia) * 0.25

                #print("tempo_ricarica dopo la ricarica: " + str(tempo_ricarica) + "\n")

                distanza_percorsa += distanza_stazione_deposito

                # mi sposto sul deposito 
                percorso.append(next_node)

                # mettendo il current_node a 0 dovrei uscire dal while
                current_node= next_node
                
            else: # caso in cui ho autonomia a sufficienza per arrivare al deposito
                
                autonomia -= distanza_deposito
                distanza_percorsa += distanza_deposito

                percorso.append(next_node)
                current_node= next_node

        # Caso 2)
        else:
            next_city= dizionario_citta[int(next_node)]
            distanza_stazione_next_node= next_city.distanza_stazione

            autonomia_futura= autonomia - next_dist

            if distanza_stazione_next_node > autonomia_futura:
                # Da current_node devo andare in stazione_current_node e aggiungere la stazione al percorso

                current_city= dizionario_citta[current_node]
                distanza_stazione= current_city.distanza_stazione

                quadrante= str(current_city.get_quadrant())
                stazione_current_node= quadrante + 'S'

                # aggiungo la stazione al percorso
                percorso.append(stazione_current_node)

                # aggiorno contatori
                autonomia -= distanza_stazione
                distanza_percorsa += distanza_stazione

                # Devo ricaricare 
                # delta_ricarica mi dice quanto ricaricare
                delta_ricarica= k - autonomia

                autonomia= k

                #print("\ntempo_ricarica prima della ricarica: " + str(tempo_ricarica))
                #print("tempo per questa ricarica: " + str(delta_ricarica * 0.25))

                tempo_ricarica += 0.25 * delta_ricarica

                #print("tempo_ricarica dopo la ricarica: " + str(tempo_ricarica))

                # alzo il flag che mi indica che l'ultimo nodo visitato era una stazione
                visited_station= 1
            else:

                # Se invece ho abbastanza ricarica proseguo il tour
                percorso.append(next_node)

                # aggiorno i contatori

                autonomia -= next_dist
                distanza_percorsa += next_dist

                # se sono qui il current_node non può essere una stazione di ricarica
                current_node= next_node

                # qui devo fare il controllo se sono nell'ultimo nodo

                if int(current_node) == last_node:
                    # Se il nodo corrente è l'ultimo, al posto che fare il controllo per vedere se si riesce ad arrivare alla stazione del prossimo nodo , devo fare il controllo
                    # per vedere se riesco ad arrivare al deposito
                    last_node_flag= 1

                # se il flag di stazione visitata era alzato, ora l'abbasso in quanto l'ultimo nodo visitato era un cliente
                if visited_station == 1:
                    visited_station = 0


    tempo_totale= distanza_percorsa + tempo_ricarica

    christofides_graph= crea_dizionario_percorso(percorso,dizionario_citta,dizionario_stazioni)

    return christofides_graph, distanza_percorsa, tempo_ricarica, percorso, tempo_totale


def minimum_weight_matching(MST, G, odd_vert):  # MST è una lista di triple, (v1 v2 distanza),  G è un dizionario di dizionari, odd_vert è una lista di vertici
    import random
    random.shuffle(odd_vert)

    while odd_vert:
        v = odd_vert.pop()
        length = float("inf")
        u = 1
        closest = 0
        for u in odd_vert:
            if v != u and G[v][u] < length:
                length = G[v][u]
                closest = u

        MST.append([v, closest, length])
        odd_vert.remove(closest)

def Christofides_Algorithm(dizionario_citta, dizionario_stazioni, Max_Axis, k):
    G= create_distance_dict(dizionario_citta)
    # print("G: " + str(G))
    # 1) Trovare MST del grafo
    # dizionario_distanze_citta, dizionario_uso_archi, distanza_mst, mst_graph= MinimumSpanningTree(dizionario_citta)  # archi_usati[element1,element2,..], element= [nodoA,nodoB, peso arco] 
    mst_graph= MinimumSpanningTree(dizionario_citta)
    # print("mst_graph: ", str(mst_graph))
    # Creo il plot
    plt.draw_mst(dizionario_citta, Max_Axis, mst_graph)

    nodi= list(dizionario_citta.keys())
    nodi.append(0)

    # 2) Ottenere l'insieme dei vertici di grado dispari del mst
    odd_degree_verteces=  find_odd_degree_verteces(nodi,mst_graph)

    # print("odd_degree_vertex: " + str(odd_degree_verteces))
    # 3) Creare il sottografo indotto dati i vertici di grado dispari trovati prima, da questo grafo, trovare il Perfect Matching di peso minimo
    # add minimum weight matching edges to MST, ovvero, confronto tutti i nodi dispari e cerco di collegarli con i nodi dispari con distanza minore

    minimum_weight_matching(mst_graph,G,odd_degree_verteces)
    # print("mst_graph dopo: " + str(mst_graph))
    # Creo il plot


    # 4) n modo iterativo, 
	# ∀ nodo v di grado >2, 
	# - considera la coppia di archi (u,v) e (v,w) in S che massimizza cuv+cvw–cuw, con (u,w)∉S, mantenendo la connessione, 
	# - sostituisci gli archi (u,v) e (v,w) con l’arco (u,w), garantendo la connessione di S

    christofides_graph_no_recharge= create_christofides_graph(mst_graph,G,dizionario_citta, Max_Axis)

    #print("\n\n\n -------------------------------------------------------------------------------------------------")
    #print("\nchristofide_graph_no_recharge: " + str(christofides_graph_no_recharge))
    #print("\n\n\n -------------------------------------------------------------------------------------------------")

    plt.draw_Christofides(christofides_graph_no_recharge, dizionario_citta, Max_Axis)

    # UNA VOLTA TROVATO IL CIRCUITO HAMILTONIANO BISOGNA MODIFICARE IL GRAFO CONSIDERANDO L'AUTONOMIA DELL'AUTO

    christofides_graph, distanza_percorsa, tempo_ricarica, percorso, tempo_totale= create_green_graph(christofides_graph_no_recharge, dizionario_stazioni, dizionario_citta, k)
    
    #christofides_graph, distanza_percorsa, tempo_ricarica, percorso, tempo_totale= create_green_opt(christofides_graph_no_recharge, dizionario_stazioni, dizionario_citta, k)
    
    plt.draw_Christofides_green(christofides_graph, dizionario_citta, dizionario_stazioni, Max_Axis)

    # print("christofide_graph: " + str(christofides_graph))

    dizionario_Christofides= {}
    dizionario_Christofides['percorso']= percorso
    dizionario_Christofides['distanza']= distanza_percorsa
    dizionario_Christofides['tempo_tot']= tempo_totale
    dizionario_Christofides['tempo_ricarica']= tempo_ricarica

    return  dizionario_Christofides




if __name__ == "__main__":

    N_CITIES= 10
    Max_Axis= 20
    k= 56
    dizionario_stazioni = {1: [10, 10], 2: [10, -10], 3: [-10, -10], 4: [-10, 10]}

    lista_citta=[
                [10, -19],
                [-10, 9],
                [-9, 7],
                [-10, -9],
                [2, -20],
                [9, -10],
                [13, -16],
                [-15, -10],
                [8, 18]
            ] 

    G={ 0: {1: 21, 2: 13, 3: 11, 4: 13, 5: 20, 6: 13, 7: 20, 8: 18, 9: 19},
        1: {0: 21, 2: 34, 3: 32, 4: 22, 5: 8, 6: 9, 7: 4, 8: 26, 9: 37},
        2: {0: 13, 1: 34, 3: 2, 4: 18, 5: 31, 6: 26, 7: 33, 8: 19, 9: 20},
        3: {0: 11, 1: 32, 2: 2, 4: 16, 5: 29, 6: 24, 7: 31, 8: 18, 9: 20},
        4: {0: 13, 1: 22, 2: 18, 3: 16, 5: 16, 6: 19, 7: 24, 8: 5, 9: 32},
        5: {0: 20, 1: 8, 2: 31, 3: 29, 4: 16, 6: 12, 7: 11, 8: 19, 9: 38},
        6: {0: 13, 1: 9, 2: 26, 3: 24, 4: 19, 5: 12, 7: 7, 8: 24, 9: 28},
        7: {0: 20, 1: 4, 2: 33, 3: 31, 4: 24, 5: 11, 6: 7, 8: 28, 9: 34},
        8: {0: 18, 1: 26, 2: 19, 3: 18, 4: 5, 5: 19, 6: 24, 7: 28, 9: 36},
        9: {0: 19, 1: 37, 2: 20, 3: 20, 4: 32, 5: 38, 6: 28, 7: 34, 8: 36}
    }


    i = 1
    dizionario_citta= {}
    for element in lista_citta: 
        cliente= Cliente(element[0],element[1],dizionario_stazioni,i)
        dizionario_citta[i]= cliente
        i += 1

    """# ------------------------ Nearest Neighbour --------------------------------------------
    print("--------- Nearest Neighbour -------------")
    dizionario_Nearest_Neighbour= NearestNeighbour(dizionario_citta, dizionario_stazioni, k, N_CITIES, Max_Axis)
    percorso= dizionario_Nearest_Neighbour['percorso']
    distanza_percorsa= dizionario_Nearest_Neighbour['distanza']
    tempo_totale= dizionario_Nearest_Neighbour['tempo_tot']
    tempo_ricarica= dizionario_Nearest_Neighbour['tempo_ricarica']

    print("percorso: " + str(percorso))
    print("distanza_percorso: " + str(distanza_percorsa))
    print("tempo_totale: " + str(tempo_totale))
    print("tempo_ricarica: " + str(tempo_ricarica))"""

    # ------------------------ Christofides --------------------------------------------------
    print("--------- Christofides -------------")
    dizionario_Christofides= Christofides_Algorithm(dizionario_citta, dizionario_stazioni, Max_Axis, k)
    
    percorso= dizionario_Christofides['percorso']
    distanza_percorsa= dizionario_Christofides['distanza']
    tempo_totale= dizionario_Christofides['tempo_tot']
    tempo_ricarica= dizionario_Christofides['tempo_ricarica']

    print("\n\n\n -------------------------------------------------------------------------------------------------")
    print("percorso: " + str(percorso))
    print("distanza_percorso: " + str(distanza_percorsa))
    print("tempo_totale: " + str(tempo_totale))
    print("tempo_ricarica: " + str(tempo_ricarica))

    print(" ------------------ Controllo soluzione ------------------------------------------------")
    resAccettabilita= soluzione_accettabile(percorso, G, k, dizionario_citta, dizionario_stazioni)
    costo= calcola_costo(G, k, dizionario_citta, dizionario_stazioni, percorso)
    print("res: " + str(resAccettabilita))
    print("costo: " + str(costo))
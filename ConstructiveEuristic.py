import copy
import sys
import time
import PlotGenerator as plt
from Cliente import Cliente, euclidean_distance, soluzione_accettabile, calcola_costo


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

    plt.draw_map(percorso, dizionario_citta, dizionario_stazioni, Max_Axis, '/NearestNeighbour/NearestNeighbour_GreenTSP.jpg')


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
                    try:
                        stazione= int(last_station.replace('S',''))
                    except:
                        sys.exit("percorso[-1]: " + str(percorso[-1]))
                        
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

    pm_list=[]

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
        pm_list.append([v,closest,length])
        odd_vert.remove(closest)
    return pm_list

def Christofides_Algorithm(dizionario_citta, dizionario_stazioni, Max_Axis, k):
    G= create_distance_dict(dizionario_citta)
    # print("G: " + str(G))
    # 1) Trovare MST del grafo
    # dizionario_distanze_citta, dizionario_uso_archi, distanza_mst, mst_graph= MinimumSpanningTree(dizionario_citta)  # archi_usati[element1,element2,..], element= [nodoA,nodoB, peso arco] 
    mst_graph= MinimumSpanningTree(dizionario_citta)
    # print("mst_graph: ", str(mst_graph))
    # Creo il plot
    plt.draw_mst(dizionario_citta, Max_Axis, mst_graph,0)

    nodi= list(dizionario_citta.keys())
    nodi.append(0)

    # 2) Ottenere l'insieme dei vertici di grado dispari del mst
    odd_degree_verteces=  find_odd_degree_verteces(nodi,mst_graph)

    # print("odd_degree_vertex: " + str(odd_degree_verteces))
    # 3) Creare il sottografo indotto dati i vertici di grado dispari trovati prima, da questo grafo, trovare il Perfect Matching di peso minimo
    # add minimum weight matching edges to MST, ovvero, confronto tutti i nodi dispari e cerco di collegarli con i nodi dispari con distanza minore

    pm_list= minimum_weight_matching(mst_graph,G,odd_degree_verteces)
    #print("pm_list: " + str(pm_list))
    plt.draw_mst(dizionario_citta, Max_Axis, pm_list,1)
    # print("mst_graph dopo: " + str(mst_graph))
    # Creo il plot
    #plt.draw_mst(dizionario_citta, Max_Axis, mst_graph,1)

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

    N_CITIES= 50
    Max_Axis= 50
    k= 141
    dizionario_stazioni = {1: [25, 25], 2: [25, -25], 3: [-25, -25], 4: [-25, 25]}
    lista_citta=[
                    [-24, 12],
                    [27, 1],
                    [-10, -34],
                    [-50, -18],
                    [-9, -15],
                    [21, -19],
                    [-35, -37],
                    [-6, 8],
                    [36, -16],
                    [-26, -18],
                    [3, -8],
                    [-19, -38],
                    [8, 28],
                    [-27, -32],
                    [42, 21],
                    [36, 36],
                    [-37, -31],
                    [21, -36],
                    [6, 26],
                    [-7, 21],
                    [-50, -31],
                    [-36, 7],
                    [49, 28],
                    [3, 48],
                    [20, -34],
                    [15, -13],
                    [-26, 20],
                    [44, 42],
                    [25, -44],
                    [6, -35],
                    [-42, 29],
                    [9, 8],
                    [40, -37],
                    [-26, 22],
                    [31, -27],
                    [-41, 7],
                    [18, 37],
                    [42, 16],
                    [-10, 7],
                    [32, 6],
                    [-3, 21],
                    [0, -4],
                    [-48, 38],
                    [-17, 4],
                    [-48, 16],
                    [17, -35],
                    [-31, 21],
                    [-45, -47],
                    [-39, 34]
                ]

    G={ 
        0: {1: 26, 2: 27, 3: 35, 4: 53, 5: 17, 6: 28, 7: 50, 8: 10, 9: 39, 10: 31, 11: 8, 12: 42, 13: 29, 14: 41, 15: 46, 16: 50, 17: 48, 18: 41, 19: 26, 20: 22, 21: 58, 22: 36, 23: 56, 24: 48, 25: 39, 26: 19, 27: 32, 28: 60, 29: 50, 30: 35, 31: 51, 32: 12, 33: 54, 34: 34, 35: 41, 36: 41, 37: 41, 38: 44, 39: 12, 40: 32, 41: 21, 42: 4, 43: 61, 44: 17, 45: 50, 46: 38, 47: 37, 48: 65, 49: 51},
        1: {0: 26, 2: 52, 3: 48, 4: 39, 5: 30, 6: 54, 7: 50, 8: 18, 9: 66, 10: 30, 11: 33, 12: 50, 13: 35, 14: 44, 15: 66, 16: 64, 17: 44, 18: 65, 19: 33, 20: 19, 21: 50, 22: 13, 23: 74, 24: 45, 25: 63, 26: 46, 27: 8, 28: 74, 29: 74, 30: 55, 31: 24, 32: 33, 33: 80, 34: 10, 35: 67, 36: 17, 37: 48, 38: 66, 39: 14, 40: 56, 41: 22, 42: 28, 43: 35, 44: 10, 45: 24, 46: 62, 47: 11, 48: 62, 49: 26},
        2: {0: 27, 1: 52, 3: 50, 4: 79, 5: 39, 6: 20, 7: 72, 8: 33, 9: 19, 10: 56, 11: 25, 12: 60, 13: 33, 14: 63, 15: 25, 16: 36, 17: 71, 18: 37, 19: 32, 20: 39, 21: 83, 22: 63, 23: 34, 24: 52, 25: 35, 26: 18, 27: 56, 28: 44, 29: 45, 30: 41, 31: 74, 32: 19, 33: 40, 34: 57, 35: 28, 36: 68, 37: 37, 38: 21, 39: 37, 40: 7, 41: 36, 42: 27, 43: 83, 44: 44, 45: 76, 46: 37, 47: 61, 48: 86, 49: 73},
        3: {0: 35, 1: 48, 2: 50, 4: 43, 5: 19, 6: 34, 7: 25, 8: 42, 9: 49, 10: 22, 11: 29, 12: 9, 13: 64, 14: 17, 15: 75, 16: 83, 17: 27, 18: 31, 19: 62, 20: 55, 21: 40, 22: 48, 23: 85, 24: 83, 25: 30, 26: 32, 27: 56, 28: 93, 29: 36, 30: 16, 31: 70, 32: 46, 33: 50, 34: 58, 35: 41, 36: 51, 37: 76, 38: 72, 39: 41, 40: 58, 41: 55, 42: 31, 43: 81, 44: 38, 45: 62, 46: 27, 47: 58, 48: 37, 49: 73},
        4: {0: 53, 1: 39, 2: 79, 3: 43, 5: 41, 6: 71, 7: 24, 8: 51, 9: 86, 10: 24, 11: 53, 12: 36, 13: 74, 14: 26, 15: 99, 16: 101, 17: 18, 18: 73, 19: 71, 20: 58, 21: 13, 22: 28, 23: 109, 24: 84, 25: 71, 26: 65, 27: 44, 28: 111, 29: 79, 30: 58, 31: 47, 32: 64, 33: 91, 34: 46, 35: 81, 36: 26, 37: 87, 38: 98, 39: 47, 40: 85, 41: 61, 42: 51, 43: 56, 44: 39, 45: 34, 46: 69, 47: 43, 48: 29, 49: 53},
        5: {0: 17, 1: 30, 2: 39, 3: 19, 4: 41, 6: 30, 7: 34, 8: 23, 9: 45, 10: 17, 11: 13, 12: 25, 13: 46, 14: 24, 15: 62, 16: 68, 17: 32, 18: 36, 19: 43, 20: 36, 21: 44, 22: 34, 23: 72, 24: 64, 25: 34, 26: 24, 27: 38, 28: 77, 29: 44, 30: 25, 31: 55, 32: 29, 33: 53, 34: 40, 35: 41, 36: 38, 37: 58, 38: 59, 39: 22, 40: 46, 41: 36, 42: 14, 43: 65, 44: 20, 45: 49, 46: 32, 47: 42, 48: 48, 49: 57},
        6: {0: 28, 1: 54, 2: 20, 3: 34, 4: 71, 5: 30, 7: 58, 8: 38, 9: 15, 10: 47, 11: 21, 12: 44, 13: 48, 14: 49, 15: 45, 16: 57, 17: 59, 18: 17, 19: 47, 20: 48, 21: 72, 22: 62, 23: 54, 24: 69, 25: 15, 26: 8, 27: 61, 28: 65, 29: 25, 30: 21, 31: 79, 32: 29, 33: 26, 34: 62, 35: 12, 36: 67, 37: 56, 38: 40, 39: 40, 40: 27, 41: 46, 42: 25, 43: 89, 44: 44, 45: 77, 46: 16, 47: 65, 48: 71, 49: 80},
        7: {0: 50, 1: 50, 2: 72, 3: 25, 4: 24, 5: 34, 6: 58, 8: 53, 9: 74, 10: 21, 11: 47, 12: 16, 13: 77, 14: 9, 15: 96, 16: 101, 17: 6, 18: 56, 19: 75, 20: 64, 21: 16, 22: 44, 23: 106, 24: 93, 25: 55, 26: 55, 27: 57, 28: 111, 29: 60, 30: 41, 31: 66, 32: 62, 33: 75, 34: 59, 35: 66, 36: 44, 37: 91, 38: 93, 39: 50, 40: 79, 41: 66, 42: 48, 43: 76, 44: 44, 45: 54, 46: 52, 47: 58, 48: 14, 49: 71},
        8: {0: 10, 1: 18, 2: 33, 3: 42, 4: 51, 5: 23, 6: 38, 7: 53, 9: 48, 10: 32, 11: 18, 12: 47, 13: 24, 14: 45, 15: 49, 16: 50, 17: 49, 18: 51, 19: 21, 20: 13, 21: 58, 22: 30, 23: 58, 24: 41, 25: 49, 26: 29, 27: 23, 28: 60, 29: 60, 30: 44, 31: 41, 32: 15, 33: 64, 34: 24, 35: 50, 36: 35, 37: 37, 38: 48, 39: 4, 40: 38, 41: 13, 42: 13, 43: 51, 44: 11, 45: 42, 46: 48, 47: 28, 48: 67, 49: 42},
        9: {0: 39, 1: 66, 2: 19, 3: 49, 4: 86, 5: 45, 6: 15, 7: 74, 8: 48, 10: 62, 11: 33, 12: 59, 13: 52, 14: 65, 15: 37, 16: 52, 17: 74, 18: 25, 19: 51, 20: 56, 21: 87, 22: 75, 23: 45, 24: 72, 25: 24, 26: 21, 27: 71, 28: 58, 29: 30, 30: 35, 31: 90, 32: 36, 33: 21, 34: 72, 35: 12, 36: 80, 37: 55, 38: 32, 39: 51, 40: 22, 41: 53, 42: 37, 43: 99, 44: 56, 45: 89, 46: 26, 47: 76, 48: 86, 49: 90},
        10: {0: 31, 1: 30, 2: 56, 3: 22, 4: 24, 5: 17, 6: 47, 7: 21, 8: 32, 9: 62, 11: 30, 12: 21, 13: 57, 14: 14, 15: 78, 16: 82, 17: 17, 18: 50, 19: 54, 20: 43, 21: 27, 22: 26, 23: 87, 24: 72, 25: 48, 26: 41, 27: 38, 28: 92, 29: 57, 30: 36, 31: 49, 32: 43, 33: 68, 34: 40, 35: 57, 36: 29, 37: 70, 38: 76, 39: 29, 40: 62, 41: 45, 42: 29, 43: 60, 44: 23, 45: 40, 46: 46, 47: 39, 48: 34, 49: 53},
        11: {0: 8, 1: 33, 2: 25, 3: 29, 4: 53, 5: 13, 6: 21, 7: 47, 8: 18, 9: 33, 10: 30, 12: 37, 13: 36, 14: 38, 15: 48, 16: 55, 17: 46, 18: 33, 19: 34, 20: 30, 21: 57, 22: 41, 23: 58, 24: 56, 25: 31, 26: 13, 27: 40, 28: 64, 29: 42, 30: 27, 31: 58, 32: 17, 33: 47, 34: 41, 35: 33, 36: 46, 37: 47, 38: 45, 39: 19, 40: 32, 41: 29, 42: 5, 43: 68, 44: 23, 45: 56, 46: 30, 47: 44, 48: 61, 49: 59},
        12: {0: 42, 1: 50, 2: 60, 3: 9, 4: 36, 5: 25, 6: 44, 7: 16, 8: 47, 9: 59, 10: 21, 11: 37, 13: 71, 14: 10, 15: 84, 16: 92, 17: 19, 18: 40, 19: 68, 20: 60, 21: 31, 22: 48, 23: 94, 24: 88, 25: 39, 26: 42, 27: 58, 28: 101, 29: 44, 30: 25, 31: 70, 32: 53, 33: 59, 34: 60, 35: 51, 36: 50, 37: 83, 38: 81, 39: 45, 40: 67, 41: 61, 42: 38, 43: 81, 44: 42, 45: 61, 46: 36, 47: 60, 48: 27, 49: 74},
        13: {0: 29, 1: 35, 2: 33, 3: 64, 4: 74, 5: 46, 6: 48, 7: 77, 8: 24, 9: 52, 10: 57, 11: 36, 12: 71, 14: 69, 15: 34, 16: 29, 17: 74, 18: 65, 19: 2, 20: 16, 21: 82, 22: 48, 23: 41, 24: 20, 25: 63, 26: 41, 27: 34, 28: 38, 29: 73, 30: 63, 31: 50, 32: 20, 33: 72, 34: 34, 35: 59, 36: 53, 37: 13, 38: 36, 39: 27, 40: 32, 41: 13, 42: 32, 43: 56, 44: 34, 45: 57, 46: 63, 47: 39, 48: 91, 49: 47},
        14: {0: 41, 1: 44, 2: 63, 3: 17, 4: 26, 5: 24, 6: 49, 7: 9, 8: 45, 9: 65, 10: 14, 11: 38, 12: 10, 13: 69, 15: 87, 16: 92, 17: 10, 18: 48, 19: 66, 20: 56, 21: 23, 22: 40, 23: 96, 24: 85, 25: 47, 26: 46, 27: 52, 28: 102, 29: 53, 30: 33, 31: 62, 32: 53, 33: 67, 34: 54, 35: 58, 36: 41, 37: 82, 38: 84, 39: 42, 40: 70, 41: 58, 42: 38, 43: 73, 44: 37, 45: 52, 46: 44, 47: 53, 48: 23, 49: 67},
        15: {0: 46, 1: 66, 2: 25, 3: 75, 4: 99, 5: 62, 6: 45, 7: 96, 8: 49, 9: 37, 10: 78, 11: 48, 12: 84, 13: 34, 14: 87, 16: 16, 17: 94, 18: 60, 19: 36, 20: 49, 21: 105, 22: 79, 23: 9, 24: 47, 25: 59, 26: 43, 27: 68, 28: 21, 29: 67, 30: 66, 31: 84, 32: 35, 33: 58, 34: 68, 35: 49, 36: 84, 37: 28, 38: 5, 39: 53, 40: 18, 41: 45, 42: 48, 43: 91, 44: 61, 45: 90, 46: 61, 47: 73, 48: 110, 49: 82},
        16: {0: 50, 1: 64, 2: 36, 3: 83, 4: 101, 5: 68, 6: 57, 7: 101, 8: 50, 9: 52, 10: 82, 11: 55, 12: 92, 13: 29, 14: 92, 15: 16, 17: 99, 18: 73, 19: 31, 20: 45, 21: 109, 22: 77, 23: 15, 24: 35, 25: 71, 26: 53, 27: 64, 28: 10, 29: 80, 30: 77, 31: 78, 32: 38, 33: 73, 34: 63, 35: 63, 36: 82, 37: 18, 38: 20, 39: 54, 40: 30, 41: 41, 42: 53, 43: 84, 44: 61, 45: 86, 46: 73, 47: 68, 48: 115, 49: 75},
        17: {0: 48, 1: 44, 2: 71, 3: 27, 4: 18, 5: 32, 6: 59, 7: 6, 8: 49, 9: 74, 10: 17, 11: 46, 12: 19, 13: 74, 14: 10, 15: 94, 16: 99, 18: 58, 19: 71, 20: 60, 21: 13, 22: 38, 23: 104, 24: 88, 25: 57, 26: 55, 27: 52, 28: 109, 29: 63, 30: 43, 31: 60, 32: 60, 33: 77, 34: 54, 35: 68, 36: 38, 37: 87, 38: 91, 39: 46, 40: 78, 41: 62, 42: 45, 43: 69, 44: 40, 45: 48, 46: 54, 47: 52, 48: 17, 49: 65},
        18: {0: 41, 1: 65, 2: 37, 3: 31, 4: 73, 5: 36, 6: 17, 7: 56, 8: 51, 9: 25, 10: 50, 11: 33, 12: 40, 13: 65, 14: 48, 15: 60, 16: 73, 17: 58, 19: 63, 20: 63, 21: 71, 22: 71, 23: 69, 24: 85, 25: 2, 26: 23, 27: 73, 28: 81, 29: 8, 30: 15, 31: 90, 32: 45, 33: 19, 34: 74, 35: 13, 36: 75, 37: 73, 38: 56, 39: 53, 40: 43, 41: 61, 42: 38, 43: 101, 44: 55, 45: 86, 46: 4, 47: 77, 48: 66, 49: 92},
        19: {0: 26, 1: 33, 2: 32, 3: 62, 4: 71, 5: 43, 6: 47, 7: 75, 8: 21, 9: 51, 10: 54, 11: 34, 12: 68, 13: 2, 14: 66, 15: 36, 16: 31, 17: 71, 18: 63, 20: 13, 21: 79, 22: 46, 23: 43, 24: 22, 25: 61, 26: 40, 27: 32, 28: 41, 29: 72, 30: 61, 31: 48, 32: 18, 33: 71, 34: 32, 35: 58, 36: 50, 37: 16, 38: 37, 39: 24, 40: 32, 41: 10, 42: 30, 43: 55, 44: 31, 45: 54, 46: 61, 47: 37, 48: 89, 49: 45},
        20: {0: 22, 1: 19, 2: 39, 3: 55, 4: 58, 5: 36, 6: 48, 7: 64, 8: 13, 9: 56, 10: 43, 11: 30, 12: 60, 13: 16, 14: 56, 15: 49, 16: 45, 17: 60, 18: 63, 19: 13, 21: 67, 22: 32, 23: 56, 24: 28, 25: 61, 26: 40, 27: 19, 28: 55, 29: 72, 30: 57, 31: 35, 32: 20, 33: 74, 34: 19, 35: 61, 36: 36, 37: 29, 38: 49, 39: 14, 40: 41, 41: 4, 42: 25, 43: 44, 44: 19, 45: 41, 46: 60, 47: 24, 48: 77, 49: 34},
        21: {0: 58, 1: 50, 2: 83, 3: 40, 4: 13, 5: 44, 6: 72, 7: 16, 8: 58, 9: 87, 10: 27, 11: 57, 12: 31, 13: 82, 14: 23, 15: 105, 16: 109, 17: 13, 18: 71, 19: 79, 20: 67, 22: 40, 23: 115, 24: 95, 25: 70, 26: 67, 27: 56, 28: 119, 29: 76, 30: 56, 31: 60, 32: 70, 33: 90, 34: 58, 35: 81, 36: 39, 37: 96, 38: 103, 39: 55, 40: 89, 41: 70, 42: 56, 43: 69, 44: 48, 45: 47, 46: 67, 47: 55, 48: 16, 49: 65},
        22: {0: 36, 1: 13, 2: 63, 3: 48, 4: 28, 5: 34, 6: 62, 7: 44, 8: 30, 9: 75, 10: 26, 11: 41, 12: 48, 13: 48, 14: 40, 15: 79, 16: 77, 17: 38, 18: 71, 19: 46, 20: 32, 21: 40, 23: 87, 24: 56, 25: 69, 26: 54, 27: 16, 28: 87, 29: 79, 30: 59, 31: 22, 32: 45, 33: 87, 34: 18, 35: 75, 36: 5, 37: 61, 38: 78, 39: 26, 40: 68, 41: 35, 42: 37, 43: 33, 44: 19, 45: 15, 46: 67, 47: 14, 48: 54, 49: 27},
        23: {0: 56, 1: 74, 2: 34, 3: 85, 4: 109, 5: 72, 6: 54, 7: 106, 8: 58, 9: 45, 10: 87, 11: 58, 12: 94, 13: 41, 14: 96, 15: 9, 16: 15, 17: 104, 18: 69, 19: 43, 20: 56, 21: 115, 22: 87, 24: 50, 25: 68, 26: 53, 27: 75, 28: 14, 29: 75, 30: 76, 31: 91, 32: 44, 33: 65, 34: 75, 35: 57, 36: 92, 37: 32, 38: 13, 39: 62, 40: 27, 41: 52, 42: 58, 43: 97, 44: 70, 45: 97, 46: 70, 47: 80, 48: 120, 49: 88},
        24: {0: 48, 1: 45, 2: 52, 3: 83, 4: 84, 5: 64, 6: 69, 7: 93, 8: 41, 9: 72, 10: 72, 11: 56, 12: 88, 13: 20, 14: 85, 15: 47, 16: 35, 17: 88, 18: 85, 19: 22, 20: 28, 21: 95, 22: 56, 23: 50, 25: 83, 26: 62, 27: 40, 28: 41, 29: 94, 30: 83, 31: 48, 32: 40, 33: 92, 34: 38, 35: 80, 36: 60, 37: 18, 38: 50, 39: 43, 40: 51, 41: 27, 42: 52, 43: 51, 44: 48, 45: 60, 46: 84, 47: 43, 48: 106, 49: 44},
        25: {0: 39, 1: 63, 2: 35, 3: 30, 4: 71, 5: 34, 6: 15, 7: 55, 8: 49, 9: 24, 10: 48, 11: 31, 12: 39, 13: 63, 14: 47, 15: 59, 16: 71, 17: 57, 18: 2, 19: 61, 20: 61, 21: 70, 22: 69, 23: 68, 24: 83, 26: 21, 27: 70, 28: 79, 29: 11, 30: 14, 31: 88, 32: 43, 33: 20, 34: 72, 35: 13, 36: 73, 37: 71, 38: 54, 39: 50, 40: 41, 41: 59, 42: 36, 43: 99, 44: 53, 45: 84, 46: 3, 47: 75, 48: 66, 49: 90},
        26: {0: 19, 1: 46, 2: 18, 3: 32, 4: 65, 5: 24, 6: 8, 7: 55, 8: 29, 9: 21, 10: 41, 11: 13, 12: 42, 13: 41, 14: 46, 15: 43, 16: 53, 17: 55, 18: 23, 19: 40, 20: 40, 21: 67, 22: 54, 23: 53, 24: 62, 25: 21, 27: 52, 28: 62, 29: 32, 30: 23, 31: 70, 32: 21, 33: 34, 34: 53, 35: 21, 36: 59, 37: 50, 38: 39, 39: 32, 40: 25, 41: 38, 42: 17, 43: 81, 44: 36, 45: 69, 46: 22, 47: 57, 48: 68, 49: 71},
        27: {0: 32, 1: 8, 2: 56, 3: 56, 4: 44, 5: 38, 6: 61, 7: 57, 8: 23, 9: 71, 10: 38, 11: 40, 12: 58, 13: 34, 14: 52, 15: 68, 16: 64, 17: 52, 18: 73, 19: 32, 20: 19, 21: 56, 22: 16, 23: 75, 24: 40, 25: 70, 26: 52, 28: 73, 29: 81, 30: 63, 31: 18, 32: 37, 33: 87, 34: 2, 35: 73, 36: 19, 37: 47, 38: 68, 39: 20, 40: 59, 41: 23, 42: 35, 43: 28, 44: 18, 45: 22, 46: 69, 47: 5, 48: 69, 49: 19},
        28: {0: 60, 1: 74, 2: 44, 3: 93, 4: 111, 5: 77, 6: 65, 7: 111, 8: 60, 9: 58, 10: 92, 11: 64, 12: 101, 13: 38, 14: 102, 15: 21, 16: 10, 17: 109, 18: 81, 19: 41, 20: 55, 21: 119, 22: 87, 23: 14, 24: 41, 25: 79, 26: 62, 27: 73, 29: 88, 30: 85, 31: 86, 32: 48, 33: 79, 34: 72, 35: 70, 36: 91, 37: 26, 38: 26, 39: 64, 40: 37, 41: 51, 42: 63, 43: 92, 44: 71, 45: 95, 46: 81, 47: 77, 48: 125, 49: 83},
        29: {0: 50, 1: 74, 2: 45, 3: 36, 4: 79, 5: 44, 6: 25, 7: 60, 8: 60, 9: 30, 10: 57, 11: 42, 12: 44, 13: 73, 14: 53, 15: 67, 16: 80, 17: 63, 18: 8, 19: 72, 20: 72, 21: 76, 22: 79, 23: 75, 24: 94, 25: 11, 26: 32, 27: 81, 28: 88, 30: 21, 31: 99, 32: 54, 33: 16, 34: 83, 35: 18, 36: 83, 37: 81, 38: 62, 39: 61, 40: 50, 41: 70, 42: 47, 43: 109, 44: 63, 45: 94, 46: 12, 47: 85, 48: 70, 49: 100},
        30: {0: 35, 1: 55, 2: 41, 3: 16, 4: 58, 5: 25, 6: 21, 7: 41, 8: 44, 9: 35, 10: 36, 11: 27, 12: 25, 13: 63, 14: 33, 15: 66, 16: 77, 17: 43, 18: 15, 19: 61, 20: 57, 21: 56, 22: 59, 23: 76, 24: 83, 25: 14, 26: 23, 27: 63, 28: 85, 29: 21, 31: 80, 32: 43, 33: 34, 34: 65, 35: 26, 36: 63, 37: 72, 38: 62, 39: 44, 40: 48, 41: 56, 42: 31, 43: 90, 44: 45, 45: 74, 46: 11, 47: 67, 48: 52, 49: 82},
        31: {0: 51, 1: 24, 2: 74, 3: 70, 4: 47, 5: 55, 6: 79, 7: 66, 8: 41, 9: 90, 10: 49, 11: 58, 12: 70, 13: 50, 14: 62, 15: 84, 16: 78, 17: 60, 18: 90, 19: 48, 20: 35, 21: 60, 22: 22, 23: 91, 24: 48, 25: 88, 26: 70, 27: 18, 28: 86, 29: 99, 30: 80, 32: 55, 33: 105, 34: 17, 35: 92, 36: 22, 37: 60, 38: 85, 39: 38, 40: 77, 41: 39, 42: 53, 43: 10, 44: 35, 45: 14, 46: 87, 47: 13, 48: 76, 49: 5},
        32: {0: 12, 1: 33, 2: 19, 3: 46, 4: 64, 5: 29, 6: 29, 7: 62, 8: 15, 9: 36, 10: 43, 11: 17, 12: 53, 13: 20, 14: 53, 15: 35, 16: 38, 17: 60, 18: 45, 19: 18, 20: 20, 21: 70, 22: 45, 23: 44, 24: 40, 25: 43, 26: 21, 27: 37, 28: 48, 29: 54, 30: 43, 31: 55, 33: 54, 34: 37, 35: 41, 36: 50, 37: 30, 38: 33, 39: 19, 40: 23, 41: 17, 42: 15, 43: 64, 44: 26, 45: 57, 46: 43, 47: 42, 48: 77, 49: 54},
        33: {0: 54, 1: 80, 2: 40, 3: 50, 4: 91, 5: 53, 6: 26, 7: 75, 8: 64, 9: 21, 10: 68, 11: 47, 12: 59, 13: 72, 14: 67, 15: 58, 16: 73, 17: 77, 18: 19, 19: 71, 20: 74, 21: 90, 22: 87, 23: 65, 24: 92, 25: 20, 26: 34, 27: 87, 28: 79, 29: 16, 30: 34, 31: 105, 32: 54, 34: 88, 35: 13, 36: 92, 37: 77, 38: 53, 39: 66, 40: 43, 41: 72, 42: 51, 43: 115, 44: 70, 45: 102, 46: 23, 47: 91, 48: 85, 49: 106},
        34: {0: 34, 1: 10, 2: 57, 3: 58, 4: 46, 5: 40, 6: 62, 7: 59, 8: 24, 9: 72, 10: 40, 11: 41, 12: 60, 13: 34, 14: 54, 15: 68, 16: 63, 17: 54, 18: 74, 19: 32, 20: 19, 21: 58, 22: 18, 23: 75, 24: 38, 25: 72, 26: 53, 27: 2, 28: 72, 29: 83, 30: 65, 31: 17, 32: 37, 33: 88, 35: 75, 36: 21, 37: 46, 38: 68, 39: 21, 40: 60, 41: 23, 42: 36, 43: 27, 44: 20, 45: 22, 46: 71, 47: 5, 48: 71, 49: 17},
        35: {0: 41, 1: 67, 2: 28, 3: 41, 4: 81, 5: 41, 6: 12, 7: 66, 8: 50, 9: 12, 10: 57, 11: 33, 12: 51, 13: 59, 14: 58, 15: 49, 16: 63, 17: 68, 18: 13, 19: 58, 20: 61, 21: 81, 22: 75, 23: 57, 24: 80, 25: 13, 26: 21, 27: 73, 28: 70, 29: 18, 30: 26, 31: 92, 32: 41, 33: 13, 34: 75, 36: 79, 37: 65, 38: 44, 39: 53, 40: 33, 41: 58, 42: 38, 43: 102, 44: 57, 45: 89, 46: 16, 47: 78, 48: 78, 49: 92},
        36: {0: 41, 1: 17, 2: 68, 3: 51, 4: 26, 5: 38, 6: 67, 7: 44, 8: 35, 9: 80, 10: 29, 11: 46, 12: 50, 13: 53, 14: 41, 15: 84, 16: 82, 17: 38, 18: 75, 19: 50, 20: 36, 21: 39, 22: 5, 23: 92, 24: 60, 25: 73, 26: 59, 27: 19, 28: 91, 29: 83, 30: 63, 31: 22, 32: 50, 33: 92, 34: 21, 35: 79, 37: 66, 38: 83, 39: 31, 40: 73, 41: 40, 42: 42, 43: 31, 44: 24, 45: 11, 46: 71, 47: 17, 48: 54, 49: 27},
        37: {0: 41, 1: 48, 2: 37, 3: 76, 4: 87, 5: 58, 6: 56, 7: 91, 8: 37, 9: 55, 10: 70, 11: 47, 12: 83, 13: 13, 14: 82, 15: 28, 16: 18, 17: 87, 18: 73, 19: 16, 20: 29, 21: 96, 22: 61, 23: 32, 24: 18, 25: 71, 26: 50, 27: 47, 28: 26, 29: 81, 30: 72, 31: 60, 32: 30, 33: 77, 34: 46, 35: 65, 36: 66, 38: 31, 39: 41, 40: 34, 41: 26, 42: 44, 43: 66, 44: 48, 45: 69, 46: 72, 47: 51, 48: 105, 49: 57},
        38: {0: 44, 1: 66, 2: 21, 3: 72, 4: 98, 5: 59, 6: 40, 7: 93, 8: 48, 9: 32, 10: 76, 11: 45, 12: 81, 13: 36, 14: 84, 15: 5, 16: 20, 17: 91, 18: 56, 19: 37, 20: 49, 21: 103, 22: 78, 23: 13, 24: 50, 25: 54, 26: 39, 27: 68, 28: 26, 29: 62, 30: 62, 31: 85, 32: 33, 33: 53, 34: 68, 35: 44, 36: 83, 37: 31, 39: 52, 40: 14, 41: 45, 42: 46, 43: 92, 44: 60, 45: 90, 46: 56, 47: 73, 48: 107, 49: 82},
        39: {0: 12, 1: 14, 2: 37, 3: 41, 4: 47, 5: 22, 6: 40, 7: 50, 8: 4, 9: 51, 10: 29, 11: 19, 12: 45, 13: 27, 14: 42, 15: 53, 16: 54, 17: 46, 18: 53, 19: 24, 20: 14, 21: 55, 22: 26, 23: 62, 24: 43, 25: 50, 26: 32, 27: 20, 28: 64, 29: 61, 30: 44, 31: 38, 32: 19, 33: 66, 34: 21, 35: 53, 36: 31, 37: 41, 38: 52, 40: 42, 41: 15, 42: 14, 43: 49, 44: 7, 45: 39, 46: 49, 47: 25, 48: 64, 49: 39},
        40: {0: 32, 1: 56, 2: 7, 3: 58, 4: 85, 5: 46, 6: 27, 7: 79, 8: 38, 9: 22, 10: 62, 11: 32, 12: 67, 13: 32, 14: 70, 15: 18, 16: 30, 17: 78, 18: 43, 19: 32, 20: 41, 21: 89, 22: 68, 23: 27, 24: 51, 25: 41, 26: 25, 27: 59, 28: 37, 29: 50, 30: 48, 31: 77, 32: 23, 33: 43, 34: 60, 35: 33, 36: 73, 37: 34, 38: 14, 39: 42, 41: 38, 42: 33, 43: 86, 44: 49, 45: 80, 46: 43, 47: 64, 48: 93, 49: 76},
        41: {0: 21, 1: 22, 2: 36, 3: 55, 4: 61, 5: 36, 6: 46, 7: 66, 8: 13, 9: 53, 10: 45, 11: 29, 12: 61, 13: 13, 14: 58, 15: 45, 16: 41, 17: 62, 18: 61, 19: 10, 20: 4, 21: 70, 22: 35, 23: 52, 24: 27, 25: 59, 26: 38, 27: 23, 28: 51, 29: 70, 30: 56, 31: 39, 32: 17, 33: 72, 34: 23, 35: 58, 36: 40, 37: 26, 38: 45, 39: 15, 40: 38, 42: 25, 43: 48, 44: 22, 45: 45, 46: 59, 47: 28, 48: 79, 49: 38},
        42: {0: 4, 1: 28, 2: 27, 3: 31, 4: 51, 5: 14, 6: 25, 7: 48, 8: 13, 9: 37, 10: 29, 11: 5, 12: 38, 13: 32, 14: 38, 15: 48, 16: 53, 17: 45, 18: 38, 19: 30, 20: 25, 21: 56, 22: 37, 23: 58, 24: 52, 25: 36, 26: 17, 27: 35, 28: 63, 29: 47, 30: 31, 31: 53, 32: 15, 33: 51, 34: 36, 35: 38, 36: 42, 37: 44, 38: 46, 39: 14, 40: 33, 41: 25, 43: 63, 44: 18, 45: 52, 46: 35, 47: 39, 48: 62, 49: 54},
        43: {0: 61, 1: 35, 2: 83, 3: 81, 4: 56, 5: 65, 6: 89, 7: 76, 8: 51, 9: 99, 10: 60, 11: 68, 12: 81, 13: 56, 14: 73, 15: 91, 16: 84, 17: 69, 18: 101, 19: 55, 20: 44, 21: 69, 22: 33, 23: 97, 24: 51, 25: 99, 26: 81, 27: 28, 28: 92, 29: 109, 30: 90, 31: 10, 32: 64, 33: 115, 34: 27, 35: 102, 36: 31, 37: 66, 38: 92, 39: 49, 40: 86, 41: 48, 42: 63, 44: 46, 45: 22, 46: 97, 47: 24, 48: 85, 49: 9},
        44: {0: 17, 1: 10, 2: 44, 3: 38, 4: 39, 5: 20, 6: 44, 7: 44, 8: 11, 9: 56, 10: 23, 11: 23, 12: 42, 13: 34, 14: 37, 15: 61, 16: 61, 17: 40, 18: 55, 19: 31, 20: 19, 21: 48, 22: 19, 23: 70, 24: 48, 25: 53, 26: 36, 27: 18, 28: 71, 29: 63, 30: 45, 31: 35, 32: 26, 33: 70, 34: 20, 35: 57, 36: 24, 37: 48, 38: 60, 39: 7, 40: 49, 41: 22, 42: 18, 43: 46, 45: 33, 46: 51, 47: 22, 48: 58, 49: 37},
        45: {0: 50, 1: 24, 2: 76, 3: 62, 4: 34, 5: 49, 6: 77, 7: 54, 8: 42, 9: 89, 10: 40, 11: 56, 12: 61, 13: 57, 14: 52, 15: 90, 16: 86, 17: 48, 18: 86, 19: 54, 20: 41, 21: 47, 22: 15, 23: 97, 24: 60, 25: 84, 26: 69, 27: 22, 28: 95, 29: 94, 30: 74, 31: 14, 32: 57, 33: 102, 34: 22, 35: 89, 36: 11, 37: 69, 38: 90, 39: 39, 40: 80, 41: 45, 42: 52, 43: 22, 44: 33, 46: 82, 47: 17, 48: 63, 49: 20},
        46: {0: 38, 1: 62, 2: 37, 3: 27, 4: 69, 5: 32, 6: 16, 7: 52, 8: 48, 9: 26, 10: 46, 11: 30, 12: 36, 13: 63, 14: 44, 15: 61, 16: 73, 17: 54, 18: 4, 19: 61, 20: 60, 21: 67, 22: 67, 23: 70, 24: 84, 25: 3, 26: 22, 27: 69, 28: 81, 29: 12, 30: 11, 31: 87, 32: 43, 33: 23, 34: 71, 35: 16, 36: 71, 37: 72, 38: 56, 39: 49, 40: 43, 41: 59, 42: 35, 43: 97, 44: 51, 45: 82, 47: 73, 48: 63, 49: 88},
        47: {0: 37, 1: 11, 2: 61, 3: 58, 4: 43, 5: 42, 6: 65, 7: 58, 8: 28, 9: 76, 10: 39, 11: 44, 12: 60, 13: 39, 14: 53, 15: 73, 16: 68, 17: 52, 18: 77, 19: 37, 20: 24, 21: 55, 22: 14, 23: 80, 24: 43, 25: 75, 26: 57, 27: 5, 28: 77, 29: 85, 30: 67, 31: 13, 32: 42, 33: 91, 34: 5, 35: 78, 36: 17, 37: 51, 38: 73, 39: 25, 40: 64, 41: 28, 42: 39, 43: 24, 44: 22, 45: 17, 46: 73, 48: 69, 49: 15},
        48: {0: 65, 1: 62, 2: 86, 3: 37, 4: 29, 5: 48, 6: 71, 7: 14, 8: 67, 9: 86, 10: 34, 11: 61, 12: 27, 13: 91, 14: 23, 15: 110, 16: 115, 17: 17, 18: 66, 19: 89, 20: 77, 21: 16, 22: 54, 23: 120, 24: 106, 25: 66, 26: 68, 27: 69, 28: 125, 29: 70, 30: 52, 31: 76, 32: 77, 33: 85, 34: 71, 35: 78, 36: 54, 37: 105, 38: 107, 39: 64, 40: 93, 41: 79, 42: 62, 43: 85, 44: 58, 45: 63, 46: 63, 47: 69, 49: 81},
        49: {0: 51, 1: 26, 2: 73, 3: 73, 4: 53, 5: 57, 6: 80, 7: 71, 8: 42, 9: 90, 10: 53, 11: 59, 12: 74, 13: 47, 14: 67, 15: 82, 16: 75, 17: 65, 18: 92, 19: 45, 20: 34, 21: 65, 22: 27, 23: 88, 24: 44, 25: 90, 26: 71, 27: 19, 28: 83, 29: 100, 30: 82, 31: 5, 32: 54, 33: 106, 34: 17, 35: 92, 36: 27, 37: 57, 38: 82, 39: 39, 40: 76, 41: 38, 42: 54, 43: 9, 44: 37, 45: 20, 46: 88, 47: 15, 48: 81}
    }

    #percorso= [0, 8, 39, 44, 22, 36, 45, 43, 49, 31, 47, 34, 27, 1, '4S', 20, 41, 19, 13, 24, 37, 16, 28, 23, 15, '1S', 38, 40, 2, '1S', 48, 7, 14, '3S', 17, 21, 4, 10, 12, 3, 30, 46, 25, 18, '2S', 29, 35, 33, 9, 6, 26, 11, '2S', 42, 5, 32, 0]
    
    i = 1
    dizionario_citta= {}
    for element in lista_citta: 
        cliente= Cliente(element[0],element[1],dizionario_stazioni,i)
        dizionario_citta[i]= cliente
        i += 1

    # ------------------------ Nearest Neighbour --------------------------------------------
    print("--------- Nearest Neighbour -------------")
    dizionario_Nearest_Neighbour= NearestNeighbour(dizionario_citta, dizionario_stazioni, k, N_CITIES, Max_Axis)
    percorsoN= dizionario_Nearest_Neighbour['percorso']
    distanza_percorsa= dizionario_Nearest_Neighbour['distanza']
    tempo_totale= dizionario_Nearest_Neighbour['tempo_tot']
    tempo_ricarica= dizionario_Nearest_Neighbour['tempo_ricarica']

    print("percorso: " + str(percorsoN))
    print("distanza_percorso: " + str(distanza_percorsa))
    print("tempo_totale: " + str(tempo_totale))
    print("tempo_ricarica: " + str(tempo_ricarica))

    # ------------------------ Christofides --------------------------------------------------
    print("--------- Christofides -------------")
    dizionario_Christofides= Christofides_Algorithm(dizionario_citta, dizionario_stazioni, Max_Axis, k)
    
    percorsoC= dizionario_Christofides['percorso']
    distanza_percorsa= dizionario_Christofides['distanza']
    tempo_totale= dizionario_Christofides['tempo_tot']
    tempo_ricarica= dizionario_Christofides['tempo_ricarica']

    print("\n\n\n -------------------------------------------------------------------------------------------------")
    print("percorso: " + str(percorsoC))
    print("distanza_percorso: " + str(distanza_percorsa))
    print("tempo_totale: " + str(tempo_totale))
    print("tempo_ricarica: " + str(tempo_ricarica))

    print(" ------------------ Controllo soluzione ------------------------------------------------")
    print("--------- Christofides -------------")
    resAccettabilita= soluzione_accettabile(percorsoC, G, k, dizionario_citta, dizionario_stazioni)
    costo= calcola_costo(G, k, dizionario_citta, dizionario_stazioni, percorsoC)
    print("res: " + str(resAccettabilita))
    print("costo: " + str(costo))
    print("\n\n--------- Nearest Neighbour -------------")
    resAccettabilita= soluzione_accettabile(percorsoN, G, k, dizionario_citta, dizionario_stazioni)
    costo= calcola_costo(G, k, dizionario_citta, dizionario_stazioni, percorsoN)
    print("res: " + str(resAccettabilita))
    print("costo: " + str(costo))
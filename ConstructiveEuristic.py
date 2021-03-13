import math
import copy
from PlotGenerator import draw_mst, draw_perfect_matching, draw_Christofides, draw_multigraph

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
def ricerca_arco_minimo_mst(dizionario_distanze_citta, dizionario_uso_archi):

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
        
        elif insiemeNodo1 == insiemeNodo2:
            return False

def find_odd_degree_verteces(nodi,archi_usati):

    dizionario_incidenze= {}

    odd_degree_verteces_list= []

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

def find_greater_2_degree_verteces(unione_PM_MST_graph, dizionario_citta):

    greater_2_verteces= []

    nodi_list1= [0]
    nodi_list2= list(dizionario_citta.keys())
    nodi_list= nodi_list1 + nodi_list2

    count_list= []

    for node in nodi_list:
        occ= 0
        for arco in unione_PM_MST_graph:
            if node in arco:
                occ += 1
        count_list.append(occ)

    i= 0
    for vertex in count_list:
        if vertex > 2:
            greater_2_verteces.append(i)
        i += 1

    return greater_2_verteces

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

    return dizionario_distanze_citta, dizionario_uso_archi, distanza_mst, archi_usati

def create_induced_subgraph(dizionario_citta, odd_degree_verteces):
    
    subgraph= {}

    # Devo creare gli archi che connettono ogni nodo con tutti gli altri
    for vertice in odd_degree_verteces:
        dizionario_distanze= {}

        for nodo in odd_degree_verteces:
            if nodo != vertice:
                if nodo != 0:
                    element_nodo= dizionario_citta.get(int(nodo))
                    coordinate_nodo= element_nodo.coordinate
                else:
                    coordinate_nodo= [0,0]

                if vertice != 0:
                    element_vertice= dizionario_citta.get(int(vertice))
                    coordinate_vertice= element_vertice.coordinate
                else:
                    coordinate_vertice= [0,0]

                distanza_arco= round(euclidean_distance(coordinate_vertice,coordinate_nodo),2)
                dizionario_distanze[nodo]= distanza_arco

        subgraph[vertice]= dizionario_distanze
    
    return subgraph

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

    return perfect_matching, distanza_perfect_matching
        
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
    for edge in perfect_matching_graph:
        dict_list= dict_multi_graph_s[edge[0]]

        dict_list_nodes= list(dict_list.keys())

        # Se un arco tra i due nodi esiste gia, faccio l'append e aggiungo la distanza del secondo arco ( che dovrebbe avere distanza uguale ) 
        if edge[1] in dict_list_nodes:
            dict_list[edge[1]].append(int(round(edge[2],0)))
        else:
            # Se un arco tra i due nodi non esiste, creo una lista con la distanza di un arco soltanto
            distanza= [edge[2]]
            dict_list[edge[1]]= distanza

        # Devo fare il simmetrico
        dict_list2= dict_multi_graph_s[edge[1]]
        dict_list_nodes2= list(dict_list2.keys())

        if edge[0] in dict_list_nodes2:
            dict_list2[edge[0]].append(int(round(edge[2],0)))
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
            dict_list[edge[1]].append(int(round(edge[2],0)))
        else:
            # Se un arco tra i due nodi non esiste, creo una lista con la distanza di un arco soltanto
            distanza= [int(round(edge[2],0))]
            dict_list[edge[1]]= distanza

        # Devo fare il simmetrico
        dict_list2= dict_multi_graph_s[edge[1]]
        dict_list_nodes2= list(dict_list2.keys())

        if edge[0] in dict_list_nodes2:
            dict_list2[edge[0]].append(int(round(edge[2],0)))
        else:
            # Se un arco tra i due nodi non esiste, creo una lista con la distanza di un arco soltanto
            distanza= [int(round(edge[2],0))]
            dict_list2[edge[0]]= distanza

    return dict_multi_graph_s

# Controlla che se si tolgono gli archi (u,v),(v,w) e aggiungendo (u,w) il multigrafo rimane connesso
def check_connection_multigraph(u,w,v,archi_v,dict_multi_graph_s):
    node_v= copy.deepcopy(archi_v)

    print("--connection_multigraph--\n")
    print("u: " + str(u))
    print("v: " + str(v))
    print("w: " + str(w))
    print("node_v :" + str(node_v))
    new_dict= copy.deepcopy(dict_multi_graph_s)

    # Cancello arco (v,u)
    node_v.pop(u)
    # cancello arco (v,w)
    node_v.pop(w)

    # una volta aggiornato i collegamenti di v ( che sono le chiavi del dizionario che tiro fuori con new_dict.pop(v)) reinserisco il nodo v nel dizionario
    new_dict[v]= node_v

    # tolto gli archi (uv), (vw) e aggiungo (u,w)
    node_u= new_dict.pop(u)
    
    # Al nodo u inserisco il collegamento con w ( e poi faro il viceversa), per aggiungere questo collegamento basta aggiungere la chiave w , l'importante è che ci sia la chiave, il valore corrispettivo a tale chiave non è importante
    # perchè qui devo solo guardare i nodi, non i valori degli archi
    node_u[w]= 1000
    new_dict[u]= node_u

    node_w= new_dict.pop(w)

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
    
    print("nodi_visitati: " + str(nodi_visitati))
    # Vado a leggere il primo valore nello stack, inserisco nello stack tutti i nodi che non sono gia presenti nello stack  a cui v è collegato e che non sono gia stati visitati
    # Una volta inseriti i nodi non ancora visitati nello stack, faccio il pop del valore appena letto e lo segno come visitato
    stack= [int(v)]

    while len(stack) > 0:
        print("stack: " + str(stack))
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
        return False
    else:
        return True



def create_christofides_graph(perfect_matching_graph, mst_graph, dizionario_citta):
    
    pm_archi= []
    for element in perfect_matching_graph:
        pm_archi.append([element[0],element[1]])

    mst_archi= []
    for element in mst_graph:
        mst_archi.append([element[0],element[1]])

    multi_graph_S= pm_archi + mst_archi

    dict_multi_graph_s= createDictGraph(perfect_matching_graph, mst_graph, dizionario_citta)
    print("dict_multi_graph_s: " + str(dict_multi_graph_s))
    draw_multigraph(dict_multi_graph_s, dizionario_citta, 20)
    # Per prima cosa devo trovare i nodi con grado > 2
    
    greater_2_verteces= find_greater_2_degree_verteces(multi_graph_S, dizionario_citta)

    print("greater_2_verteces: " + str(greater_2_verteces))
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
        #print("archi_v: " + str(archi_v))
        for u in nodi2_list:
            #print("archi_v.get(int(u)): " + str(archi_v.get(int(u))))
            weight_edge_u_v=  list(archi_v.get(int(u)))
            weight_edge_u_v= weight_edge_u_v[0]
            for w in nodi2_list:
                # Qui devo verificare che se togliessi u,v e v,w aggiungendo u,w il grafo rimarrebbe connesso, se non rimane connesso la scelta va scartata
                if w != u and check_connection_multigraph(u,w,vertex,archi_v,dict_multi_graph_s):
                    print("v: " + str(vertex))
                    print("u: " + str(u))
                    print("w: " + str(w))
                    print("archi_v.get(int(w)): " + str(archi_v.get(int(w))))
                    weight_edge_v_w= list(archi_v.get(int(w)))
                    weight_edge_v_w= weight_edge_v_w[0]
                    if u == 0:
                        coordinate_u= [0,0]
                    else:
                        coordinate_u= dizionario_citta.get(int(u)).coordinate
                    
                    if w == 0:
                        coordinate_w= [0,0]
                    else:
                        coordinate_w= dizionario_citta.get(int(w)).coordinate

                    weight_edge_u_w= int(round(euclidean_distance(coordinate_u,coordinate_w),0))    
                    print("weight_edge_u_w: "+ str(weight_edge_u_w))
                    cost= weight_edge_u_v + weight_edge_v_w - weight_edge_u_w
                    print("Cost: " + str(cost))
                    if cost >= max_cost:
                        max_cost= cost
                        U= u
                        V= vertex
                        W= w
                        weight_edge_U_W= weight_edge_u_w

        # Finito il ciclo tra gli archi vado a cancellare gli archi che devo cancellare (u,v) e (v,w) e aggiungere l'arco che devo aggiungere (u,w)
        print("---FineCiclo---")
        print("V: " + str(V))
        print("U: " + str(U))
        print("W: " + str(W))
        print("weight_edge_U_W: " + str(weight_edge_U_W))
        print("max_cost: " + str(max_cost))

        # Cancello (v,u)
        arco_v_u= archi_v.pop(U)

        # Se ci sono due stessi archi ne elimino solo 1 e l'altro lo lascio
        if len(arco_v_u) > 1:
            archi_v[U]= arco_v_u[0]

        # cancello il simmetrico(u,v) 

        archi_u= dict_multi_graph_s.pop(int(U))
        
        arco_u_v= archi_u.pop(V)

        if len(arco_u_v) > 1:
            archi_u[V]= arco_u_v[0]

        # Aggiungo l'arco (u,w)
        archi_u[W]= [weight_edge_U_W]
        dict_multi_graph_s[U]= archi_u

        # Cancello (v,w)
        arco_v_w= archi_v.pop(W)

        if len(arco_v_w) > 1:
            archi_v[W]= arco_v_w[0]
        
        # cancello il simmetrico(w,v)
        archi_w= dict_multi_graph_s.pop(int(W))
        arco_w_v= archi_w.pop(V)

        if len(arco_w_v) > 1:
            archi_w[V]= arco_w_v[0]
        
        # Aggiungo l'arco (w,u)
        archi_w[U]= [weight_edge_U_W]
        dict_multi_graph_s[W]= archi_w

        dict_multi_graph_s[V]= archi_v

    return dict_multi_graph_s

def Christofides_Algorithm(dizionario_citta, dizionario_stazioni, Max_Axis):

    # 1) Trovare MST del grafo
    dizionario_distanze_citta, dizionario_uso_archi, distanza_mst, mst_graph= MinimumSpanningTree(dizionario_citta)  # archi_usati[element1,element2,..], element= [nodoA,nodoB, peso arco] 
    print("----mst-----")
    print("mst_graph: " + str(mst_graph))
    # Creo il plot
    draw_mst(dizionario_citta, Max_Axis, mst_graph)

    nodi= list(dizionario_citta.keys())
    nodi.append(0)

    # 2) Ottenere l'insieme dei vertici di grado dispari del mst
    odd_degree_verteces=  find_odd_degree_verteces(nodi,mst_graph)


    # 3) Creare il sottografo indotto dati i vertici di grado dispari trovati prima, da questo grafo, trovare il Perfect Matching di peso minimo
    subgraph= create_induced_subgraph(dizionario_citta, odd_degree_verteces)
    perfect_matching_graph, distanza_perfect_matching= find_perfect_matching(subgraph)
    print("--perfect matching---")
    print("perfect_matching: " + str(perfect_matching_graph))
    # Creo il plot
    subgraph_keys= list(subgraph.keys())
    draw_perfect_matching(dizionario_citta, Max_Axis, subgraph_keys, perfect_matching_graph)

    """ 4) n modo iterativo, 
	∀ nodo v di grado >2, 
	- considera la coppia di archi (u,v) e (v,w) in S che massimizza cuv+cvw–cuw, con (u,w)∉S, mantenendo la connessione, 
	- sostituisci gli archi (u,v) e (v,w) con l’arco (u,w), garantendo la connessione di S """

    christofides_graph_no_recharge= create_christofides_graph(perfect_matching_graph, mst_graph, dizionario_citta)

    print("christofide_graph_no_recharge: " + str(christofides_graph_no_recharge))
    draw_Christofides(christofides_graph_no_recharge, dizionario_citta, Max_Axis)

    # UNA VOLTA TROVATO IL CIRCUITO HAMILTONIANO BISOGNA MODIFICARE IL GRAFO CONSIDERANDO L'AUTONOMIA DELL'AUTO
"""    print("odd_degree_verteces: " + str(odd_degree_verteces))
    print("n_odd_degree: " + str(len(odd_degree_verteces)))"""
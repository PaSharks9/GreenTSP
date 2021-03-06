import random
import sys
import time
from Cliente import euclidean_distance, Cliente, calcola_costo, soluzione_accettabile
from LocalSearch import local_search_2_otp

# Crea le sottosequenze su cui effettuare la local search
def spli_tour(percorso):

    dizionario_sottopercorsi={}

    lunghezza_percorso= len(percorso)

    i= 0
    key = 0
    sottosequenza= []
    while i <= lunghezza_percorso - 1:
        
        sottosequenza.append(percorso[i])

        if 'S' in str(percorso[i]):

            dizionario_sottopercorsi[key]= sottosequenza

            sottosequenza= [percorso[i]]
            key += 1
        
        i += 1

    dizionario_sottopercorsi[key]= sottosequenza

    return dizionario_sottopercorsi


def scegli_sottopercorsi(dizionario_sottopercorsi, n_sottopercorsi):
    if n_sottopercorsi > 1:
        nSpercorso1= random.randint(0,n_sottopercorsi)
    else:
        nSpercorso1= 0

    #print("dizionario sotto_p: " + str(dizionario_sottopercorsi))

    nSpercorso2= random.randint(0,n_sottopercorsi)
    while nSpercorso2 == nSpercorso1:
        nSpercorso2= random.randint(0,n_sottopercorsi)


    sPercorso1= dizionario_sottopercorsi[nSpercorso1]
    sPercorso2= dizionario_sottopercorsi[nSpercorso2]

    return sPercorso1,sPercorso2, nSpercorso1, nSpercorso2

def perturbazione(percorso,G,k,dizionario_citta,dizionario_stazioni):
    dizionario_sottopercorsi= spli_tour(percorso)

    n_sottopercorsi= len(dizionario_sottopercorsi) - 1

    sPercorso1,sPercorso2, nSpercorso1, nSpercorso2= scegli_sottopercorsi(dizionario_sottopercorsi, n_sottopercorsi)

    #print("sPercorso1 before: " + str(sPercorso1))
    #print("sPercorso2 before: " + str(sPercorso2))
    len_sottopercorso1= len(sPercorso1)
    len_sottopercorso2= len(sPercorso2)

    while len_sottopercorso1 == len_sottopercorso2 == 2:
        sPercorso1,sPercorso2, nSpercorso1, nSpercorso2= scegli_sottopercorsi(dizionario_sottopercorsi, n_sottopercorsi)

    if len_sottopercorso1 == 2 and len_sottopercorso2 > 2:  # caso in cui sp1= ['1s','2s'] sp2= ['1s',1,3,..,'4s']
        if  len_sottopercorso2 == 3:
            index_nodeSP2= 1
        else:
            index_nodeSP2= random.randint(1,len_sottopercorso2-2)

        sPercorso1.insert(1,sPercorso2[index_nodeSP2])
        sPercorso2.pop(index_nodeSP2)

    elif len_sottopercorso1 > 2 and len_sottopercorso2 == 2:

        if len_sottopercorso1 == 3:
            index_nodeSP1= 1
        else:
            index_nodeSP1= random.randint(1,len_sottopercorso1-2)

        sPercorso2.insert(1,sPercorso1[index_nodeSP1])
        sPercorso1.pop(index_nodeSP1)
    
    else:

        if len_sottopercorso1 == 3:
            index_nodeSP1 = 1
        else:
            index_nodeSP1= random.randint(1,len_sottopercorso1-2)

        
        if len_sottopercorso2 == 3:
            index_nodeSP2= 1
        else:
            index_nodeSP2= random.randint(1,len_sottopercorso2-2)

        nodo_appoggio= sPercorso1[index_nodeSP1]
        sPercorso1[index_nodeSP1]= sPercorso2[index_nodeSP2]
        sPercorso2[index_nodeSP2]= nodo_appoggio


    tour= []
    for key in list(dizionario_sottopercorsi.keys()):
        if key == nSpercorso1:
            if key == 0:
                tour= tour + sPercorso1
            else:
                tour= tour + sPercorso1[1:]
        elif key == nSpercorso2:
            if key == 0:
                tour= tour + sPercorso2
            else:
                tour=tour + sPercorso2[1:]
        else:
            if key == 0:
                tour=tour + dizionario_sottopercorsi[key]
            else:
                tour=tour + dizionario_sottopercorsi[key][1:]
    
    tempo_tot, _= calcola_costo(G, k, dizionario_citta, dizionario_stazioni, tour)
   
    return tour, tempo_tot

def acceptance_test(tour1, tour2, tempo1, tempo2, error_tolerance):

    if tour1 != tour2:
        if tempo2 > tempo1:
            p= random.randint(0,10)
            if p < error_tolerance:
                print("tolleranza errori")
                print("p: " + str(p))
                #time.sleep(1)
                return 1
            else:
                return 0
        else:
            return 1
    else:
        return 0


def calcola_indice_max(percorso,autonomia,dizionario_citta,dizionario_stazioni):
    
    i= 0
    while i < len(percorso) - 1:
        # Quando guardiamo al primo elemento del percorso, questo pu?? essere o 0 (partenza del percorso) o una stazione (caso in cui si stia processando uno sottotour)

        #print("\nnodo1: " + str(percorso[i]))
        #print("nodo2: " + str(percorso[i+1]))

        if percorso[i] == 0: # caso in cui il primo elemento ?? il deposito

            coordinate1 = [0,0]

        elif 'S' in str(percorso[i]): # caso in cui il primo elemento del percorso sia una stazione

            stazione= int(percorso[i].replace('S',''))
            coordinate1= dizionario_stazioni[stazione]
        else:

            citta= dizionario_citta[int(percorso[i])]
            coordinate1= citta.coordinate

        # calcolo coordinate del secondo elemento

        if percorso[i+1] == 0: # caso in cui il secondo elemento ?? il deposito finale

            coordinate2 = [0,0]

        elif 'S' in str(percorso[i+1]):

            stazione2= int(percorso[i+1].replace('S',''))
            coordinate2= dizionario_stazioni[stazione2]
        else:

            citta2= dizionario_citta[int(percorso[i+1])]
            coordinate2= citta2.coordinate

        distanza= euclidean_distance(coordinate1, coordinate2)

        autonomia_futura= autonomia - distanza
        
        #print("autonomia: " + str(autonomia))
        #print("distanza: " + str(distanza))
        
        if 'S' in str(percorso[i+1]) or percorso[i+1] == 0: # vuol dire che siamo arrivati in fondo

            #if autonomia_futura < 0 :
                #print("autonomia_futura < 0")
            
            return i   # i indica l'indice della citt?? da guardare per aggiungere in i+1 la stazione di ricarica

        else: # Caso in cui la seconda citt?? non sia un nodo di fine percorso
            distanza_citta2_stazione= citta2.distanza_stazione
            #print("distanza_citta2_stazione: " + str(distanza_citta2_stazione))
            if distanza_citta2_stazione > autonomia_futura: # Se la distanza della citta2 dal deposito ?? maggiore dell'autonomia futura vuol dire che non posso raggiungere la citta nell'indice i+1
                #print("\ndistanza_citta2_stazione > autonomia_futura")
                return i 
            else:
                autonomia= autonomia_futura
        
        i += 1
    
    print("--------------ERROR---------------")
    print("nodo: " + str(percorso[i]))
    print("i: " + str(i))
    time.sleep(20)

def put_recharge_station(percorso,k,dizionario_citta,dizionario_stazioni):
    autonomia= k

    new_percorso= percorso.copy()

    i= 0

    while i < len(new_percorso)-1:
        #print("nodo1: " + str(new_percorso[i]))
        #print("nodo2: " + str(new_percorso[i+1]))
        #print("autonomia: " + str(autonomia))
        if new_percorso[i] == 0:
            coordinate1= [0,0]
        elif 'S' in str(new_percorso[i]):
            stazione= new_percorso[i].replace('S','')
            coordinate1= dizionario_stazioni[int(stazione)]
        else:
            citta1= dizionario_citta[new_percorso[i]]
            coordinate1= citta1.coordinate

        # Come citta2 non posso avere una stazione di ricarica in quanto in questo percorso non ci sono stazioni di ricarica, questa funzione le deve mettere
        if new_percorso[i+1] == 0:
            coordinate2= [0,0]
        else:
            citta2= dizionario_citta[new_percorso[i+1]]
            coordinate2= citta2.coordinate

        if i == 0:
            if new_percorso[i+1] == 0:
                return new_percorso
            # Non ?? mai possibile che dalla stazione di ricarica di partenza del sottopercorso o dal deposito iniziale del percorso, come primo spostamento si vada verso 
            # una stazione di ricarica, quindi quello che faccio ?? calcolare la distanza del primo spostamento
            distanza1_2= euclidean_distance(coordinate1,coordinate2)
            autonomia -= distanza1_2

        else:
            
            # Distinguo due casi, il primo considero che il nodo successivo sia il nodo finale del percorso ( quindi il deposito 0 ), in questo caso l'autonomia futura
            # dovr?? essere maggiore della sua distanza dal deposito
            if new_percorso[i+1] == 0:
                distanza_deposito= citta1.distanza_deposito

                if autonomia - distanza_deposito < 0:
                    citta= dizionario_citta[new_percorso[i]]
                    quadrante= citta.get_quadrant()

                    stazione= str(quadrante) + 'S'

                    new_percorso.insert(i+1,stazione)

                    # siamo arrivati alla fine quindi una volta inserita l'ultima stazione posso restituire il nuovo percorso
                #print("new_percorso: " + str(new_percorso))
                return new_percorso
            
            else:

                distanza1_2= euclidean_distance(coordinate1,coordinate2)
                autonomia_futura= autonomia - distanza1_2

                distanza_stazione= citta2.distanza_stazione

                if autonomia_futura < distanza_stazione:

                    citta= dizionario_citta[new_percorso[i]]
                    quadrante= citta.get_quadrant()
                    stazione= str(quadrante) + 'S'

                    new_percorso.insert(i+1,stazione)

                    # inserendo una stazione, resetto anche l'autonomia
                    autonomia= k
                else:
                    autonomia -= distanza1_2

        i += 1
    
    print("-----------Errore---------------")
    print("percorso: " + str(new_percorso))
    time.sleep(20)

# deprecato
def perturbazione2(percorso, G, k, dizionario_citta, dizionario_stazioni):

    # Find stations
    indici_stazioni={}
    i= 0
    for element in percorso:
        if 'S' in str(element):
            stazione= element.replace('S','')
            indici_stazioni[i]= int(stazione)
        i += 1

    new_percorso= percorso.copy()

    # Scelta randomica della chiave da eliminare
    lista_indici= list(indici_stazioni.keys())
    indice_stazione= random.choice(lista_indici)

    # Trovo indice_stazione precedente, se ce n'?? uno
    indice_precedente= 0
 
    for indice in lista_indici:
        if indice < indice_stazione:
            indice_precedente= indice

    # ora tolgo  tutte le stazioni con indice >= di questo
    i = 0 # contatore che tiene conto delle stazioni eliminate ( per poter tarare gli indici )
    for indice in lista_indici:
        if indice == indice_stazione:
            new_percorso.pop(indice)
            i += 1
        elif indice > indice_stazione:
            new_percorso.pop(indice-i)
            i += 1

    # Suddivido il percorso in spezzoni usando le stazioni rimanenti come divisori degli spezzoni
    dizionario_sotto_tour= spli_tour(new_percorso)
    chiavi= list(dizionario_sotto_tour.keys())

    # prendo la chiave pi?? alta che ?? quella che identifica l'ultimo spezzone, ovvero quello in cui sono state cancellate le stazioni ed ?? da ripopolare con nuove stazioni
    chiave_sotto_tour_finale= max(chiavi)

    # sottotour_finale ?? il percorso da popolare con le stazioni
    sottotour_finale= dizionario_sotto_tour[chiave_sotto_tour_finale]

   
    if indice_precedente != 0:
        indice_m= calcola_indice_max(sottotour_finale,k,dizionario_citta, dizionario_stazioni)
        #print("indice_m: " + str(indice_m))
        indice_max= indice_m + indice_precedente
        #print("indice_m: " + str(indice_m))
        #print("Indici_max: " + str(indice_max))
        #print("indice_prcedente: " + str(indice_precedente))

        indice_nuova_stazione= random.randint(indice_precedente + 1, indice_max)
    else:
        indice_max= calcola_indice_max(new_percorso,k,dizionario_citta, dizionario_stazioni)
        #print("Indici_max: " + str(indice_max))

        indice_nuova_stazione= random.randint(1,indice_max)

    #print("Indice precedente: " + str(indice_precedente))
    #print("Indice_nuova_stazione: " + str(indice_nuova_stazione))

    id_cliente= new_percorso[indice_nuova_stazione]
    cliente= dizionario_citta[int(id_cliente)]
    quadrante_cliente= cliente.get_quadrant()
    if quadrante_cliente == None:
        print("\ndizionario_citta: " + str(dizionario_citta))
        print("indice_nuova_stazione: " + str(indice_nuova_stazione))
        print("id_cliente: " + str(id_cliente))
        print("cliente: " + str(cliente))
        print("quadrante_cliente: " + str(quadrante_cliente))
        print("coordinate_cliente: " + str(cliente.coordinate))
        
    new_station= str(quadrante_cliente) + 'S'

    # aggiungo la nuova stazione al sottopercorso in modo da poter calcolare la giusta distanza da percorrere nel sotto_percorso
    try:
        sotto_percorso= [new_station] + new_percorso[indice_nuova_stazione+1:]
    except:
        print("\n\nnew_station: " + str([new_station]))
        print("new_percorso[indice_nuova_stazione+1:]: " + str(new_percorso[indice_nuova_stazione+1:]))
        sys.exit()

    new_green_tour= put_recharge_station(sotto_percorso,k,dizionario_citta,dizionario_stazioni)

    try:
        new_final_tour= new_percorso[0:indice_nuova_stazione+1] + new_green_tour
    except:
        print("\n\n new_percorso[0:indice_nuova_stazione+1]: " + str(new_percorso[0:indice_nuova_stazione+1]))
        print("new_green_tour: " + str(new_green_tour))
        sys.exit()
    
    tempo_tot, _= calcola_costo(G, k, dizionario_citta, dizionario_stazioni, new_final_tour)

    return new_final_tour, tempo_tot

def iterative_local_search(percorso, tempo_tot_Percorso, G, k, dizionario_citta, dizionario_stazioni, n_iterazioni, error_tolerance): 
    # 1) Soluzione iniziale x0 ?? percorso ed ?? la soluzione ottenuta dalle euristiche costruttive


    # 2) Calcolo il primo ottimo locale x*
    tour, tempo_tot= local_search_2_otp(percorso, tempo_tot_Percorso,  G, k, dizionario_citta, dizionario_stazioni)

    best_tour= tour
    best_tempo_tot= tempo_tot

    #3) Entro nel ciclo (quante volte ciclare?)
    for i in range(0,n_iterazioni+1):
        print("==============================================================" + str(i) + "==============================================================================")
        acceptance_flag= 0

        tour1, tempo_tot1= perturbazione(tour, G, k, dizionario_citta, dizionario_stazioni) # bisogna tenere conto delle soluzioni precedenti

        # tour2, tempo_tot2= local_search_2_otp(tour1, tempo_tot1,  G, k, dizionario_citta, dizionario_stazioni)
        # local_search effettua una local search sui sottopercorsi del percorso totale, i sottopercorsi sono i percorsi delimitati tra deposito-stazione_rifornimento, o tra due stazioni_rifornimento
        tour2, tempo_tot2= local_search_2_otp(tour1, tempo_tot1, G, k, dizionario_citta, dizionario_stazioni)
        # da local_search_2_otp esce sempre una soluzione accettabile, se nell'intorno generato di tour1 non ci sono soluzioni ammissibili , l'ottimo locale ?? tour1 e ritorna tour1

        acceptance_flag= acceptance_test(tour, tour2, tempo_tot, tempo_tot2, error_tolerance)

        # Se la soluzione passa il test di accettazione allora processo la nuova soluzione
        if acceptance_flag == 1:
            print("Tempo 1: " + str(tempo_tot))
            print("Tempo 2: " + str(tempo_tot2))
            #time.sleep(20)
            # Se passo il test posso processare una soluzione diversa (che pu?? essere peggiore)
            tour= tour2
            tempo_tot= tempo_tot2

            # Se il tour2 ?? meglio del best_tempo aggiorno
            if tempo_tot2 < best_tempo_tot:
                best_tour= tour2
                best_tempo_tot= tempo_tot2



    # Impacchetto il risultato
    dizionario_ILS= {}
    dizionario_ILS['percorso']= best_tour
    dizionario_ILS['tempo_tot']= best_tempo_tot
    
    return dizionario_ILS


if __name__ == "__main__":
    k= 56
    dizionario_stazioni = {1: [10, 10], 2: [10, -10], 3: [-10, -10], 4: [-10, 10]}

    lista_citta=[
        [2, -1],
        [-13, -2],
        [-11, 3],
        [8, 7],
        [12, 20],
        [-6, 1],
        [11, -13],
        [-17, -13],
        [1, -1]
    ]

    G={ 
        0: {1: 2, 2: 13, 3: 11, 4: 10, 5: 23, 6: 6, 7: 17, 8: 21, 9: 1},
        1: {0: 2, 2: 15, 3: 13, 4: 10, 5: 23, 6: 8, 7: 15, 8: 22, 9: 1},
        2: {0: 13, 1: 15, 3: 5, 4: 22, 5: 33, 6: 7, 7: 26, 8: 11, 9: 14},
        3: {0: 11, 1: 13, 2: 5, 4: 19, 5: 28, 6: 5, 7: 27, 8: 17, 9: 12},
        4: {0: 10, 1: 10, 2: 22, 3: 19, 5: 13, 6: 15, 7: 20, 8: 32, 9: 10},
        5: {0: 23, 1: 23, 2: 33, 3: 28, 4: 13, 6: 26, 7: 33, 8: 43, 9: 23},
        6: {0: 6, 1: 8, 2: 7, 3: 5, 4: 15, 5: 26, 7: 22, 8: 17, 9: 7},
        7: {0: 17, 1: 15, 2: 26, 3: 27, 4: 20, 5: 33, 6: 22, 8: 28, 9: 15},
        8: {0: 21, 1: 22, 2: 11, 3: 17, 4: 32, 5: 43, 6: 17, 7: 28, 9: 21},
        9: {0: 1, 1: 1, 2: 14, 3: 12, 4: 10, 5: 23, 6: 7, 7: 15, 8: 21}
    }

    i = 1
    dizionario_citta= {}
    for element in lista_citta: 
        cliente= Cliente(element[0],element[1],dizionario_stazioni,i)
        dizionario_citta[i]= cliente
        i += 1

    percorso= [0, 9, 1, 6, 3, 2, 8, '3S', 7, 4, '1S', 5, 0]

    #percorso= [0,'1S', 9, 1, 6, 3, 2, 8, 7, 4, 5,  0]
    #costo1= calcola_costo(G,k,dizionario_citta, dizionario_stazioni, percorso)
    #dizionario_ILS= iterative_local_search(percorso, 135.5, G, k, dizionario_citta, dizionario_stazioni,1000,3)
    tour= perturbazione(percorso,G,k,dizionario_citta,dizionario_stazioni)
    #print("costo1: " + str(costo1))
    #print("percorso: " + str(dizionario_ILS['percorso']))
    #print("tempo_tot: " + str(dizionario_ILS['tempo_tot']))
    #print("solAcc: "  + str(soluzione_accettabile(percorso, G, k, dizionario_citta, dizionario_stazioni)))
    print("\ntour: " + str(tour)) 
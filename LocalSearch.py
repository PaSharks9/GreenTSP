import random
import time
import math
from Cliente import Cliente, euclidean_distance, soluzione_accettabile, calcola_costo

def scelta_nodi(Percorso):
    index_nodi_scelti= []
    index_nodo1= -1
    index_nodo2= -1
    
    lunghezza_percorso= len(Percorso)

    while len(index_nodi_scelti) != 2:

        while index_nodo1 == index_nodo2:
            index_nodo1= random.randint(0,lunghezza_percorso-1)
            index_nodo2= random.randint(0,lunghezza_percorso-1)

            if Percorso[index_nodo1] == 0:
                index_nodo1= 0
            
            if Percorso[index_nodo2] == 0:
                index_nodo2= 0
            
            arco1= (index_nodo1,index_nodo1 + 1)
            arco2= (index_nodo2,index_nodo2 + 1)

            if arco1[0] in arco2 or arco1[1] in arco2:
                index_nodo1= -1
                index_nodo2= -1
            else:
                index_nodi_scelti= [index_nodo1,index_nodo2]
                archi_scelti= [[arco1[0],arco1[1]], [arco2[0],arco2[1]]]

    return archi_scelti

def two_opt(Percorso, dizionario_citta, dizionario_stazioni):
    nuovo_percorso= []

    # Devo selezionare due archi NON adiacenti su cui fare lo swap 
    # L'arco viene identificato dal nodo selezionato e dal suo successivo
    archi_scelti= scelta_nodi(Percorso)

    # Ora devo collegarli nell'unico modo legale possibile
    # Ovvero il primo nodo di ogni arco selezionato deve connettersi con il secondo nodo dell'altro arco

    """if archi_scelti[0][1] == 0:  #Se è un arco che ha come secondo vertice il deposito, l'indice di 0 è l'ultimo elemento del percorso, lo specifico perchè altrimenti index darebbe come indice di 0, 0
        index2arco1= len(Percorso) - 1 
        index1arco1= Percorso.index(archi_scelti[0][0])
    else:
        index1arco1= Percorso.index(archi_scelti[0][0])
        index2arco1= Percorso.index(archi_scelti[0][1])

    if archi_scelti[1][1] == 0:
        index2arco2= len(Percorso) - 1
        index1arco2= Percorso.index(archi_scelti[1][0])
    else:
        index1arco2= Percorso.index(archi_scelti[1][0])
        index2arco2= Percorso.index(archi_scelti[1][1])"""


    # Ordino gli archi, ovvero, arco1 è tra i due il primo arco che viene attraversato nel Percorso
    index1arco1= archi_scelti[0][0]
    index2arco1= archi_scelti[0][1]

    index1arco2= archi_scelti[1][0]
    index2arco2= archi_scelti[1][1]

    if index1arco1 > index1arco2:
        v= index1arco1
        index1arco1= index1arco2
        index1arco2= v

        v= index2arco1
        index2arco1= index2arco2
        index2arco2= v

    if index1arco1 != 0:
        nuovo_percorso= Percorso[0:(index1arco1 + 1)]
    else:
        # Se il primo vertice del primo arco ha indice 0 allora è per forza il nodo 0
        nuovo_percorso.append(0)
    
    # Arrivato al primo vertice del primo arco devo aggiungere al percorso il primo vertice del secondo arco
    nuovo_percorso.append(Percorso[index1arco2])

    # Ora devo aggiungere a ritroso, a partire dal primo vertice del secondo arco, fino al secondo vertice del primo arco
    lista= Percorso[(index2arco1 + 1):index1arco2]
    lista.reverse()

    nuovo_percorso=  nuovo_percorso + lista

    nuovo_percorso.append(Percorso[index2arco1])


    # Se il secondo vertice del secondo arco è 0 allora devo solo aggiungere 0 
    if index2arco2 == len(Percorso) - 1:
        nuovo_percorso.append(0)
    else:

        listaFinale= Percorso[index2arco2:]
        nuovo_percorso = nuovo_percorso + listaFinale

    #print("\narchi_scelti: " + str(archi_scelti))
    
    return archi_scelti, nuovo_percorso





# Versione con scelta nodi fuori da two_opt in modo da fare una tabella di coppie di archi gia scelti
# ---------------------------------------------
def scelta_nodi1(Percorso, tabella_archi):
    index_nodi_scelti= []
    index_nodo1= -1
    index_nodo2= -1
    
    lunghezza_percorso= len(Percorso)

    while len(index_nodi_scelti) != 2:

        while index_nodo1 == index_nodo2:
            index_nodo1= random.randint(0,lunghezza_percorso-1)
            index_nodo2= random.randint(0,lunghezza_percorso-1)

            if Percorso[index_nodo1] == 0:
                index_nodo1= 0
            
            if Percorso[index_nodo2] == 0:
                index_nodo2= 0
            
            arco1= (index_nodo1,index_nodo1 + 1)
            arco2= (index_nodo2,index_nodo2 + 1)

            if arco1[0] in arco2 or arco1[1] in arco2:
                index_nodo1= -1
                index_nodo2= -1
            else:
                index_nodi_scelti= [index_nodo1,index_nodo2]
                archi_scelti= [[arco1[0],arco1[1]], [arco2[0],arco2[1]]]

    return archi_scelti

def two_opt1(Percorso, dizionario_citta, dizionario_stazioni, archi_scelti):
    nuovo_percorso= []
    print("archi_scelti: " + str(archi_scelti))
    # Ora devo collegarli nell'unico modo legale possibile
    # Ovvero il primo nodo di ogni arco selezionato deve connettersi con il secondo nodo dell'altro arco

    # Ordino gli archi, ovvero, arco1 è tra i due il primo arco che viene attraversato nel Percorso
    index1arco1= archi_scelti[0][0]
    index2arco1= archi_scelti[0][1]

    index1arco2= archi_scelti[1][0]
    index2arco2= archi_scelti[1][1]

    if index1arco1 > index1arco2:
        v= index1arco1
        index1arco1= index1arco2
        index1arco2= v

        v= index2arco1
        index2arco1= index2arco2
        index2arco2= v

    if index1arco1 != 0:
        nuovo_percorso= Percorso[0:(index1arco1 + 1)]
    else:
        # Se il primo vertice del primo arco ha indice 0 allora è per forza il nodo 0
        nuovo_percorso.append(0)
    
    # Arrivato al primo vertice del primo arco devo aggiungere al percorso il primo vertice del secondo arco
    nuovo_percorso.append(Percorso[index1arco2])

    # Ora devo aggiungere a ritroso, a partire dal primo vertice del secondo arco, fino al secondo vertice del primo arco
    lista= Percorso[(index2arco1 + 1):index1arco2]
    lista.reverse()

    nuovo_percorso=  nuovo_percorso + lista

    nuovo_percorso.append(Percorso[index2arco1])


    # Se il secondo vertice del secondo arco è 0 allora devo solo aggiungere 0 
    if index2arco2 == len(Percorso) - 1:
        nuovo_percorso.append(0)
    else:

        listaFinale= Percorso[index2arco2:]
        nuovo_percorso = nuovo_percorso + listaFinale

    #print("\narchi_scelti: " + str(archi_scelti))
    
    return nuovo_percorso
# ---------------------------------------------


def genera_archi(Percorso):

    lista_archi= []
    lunghezza_percorso= len(Percorso)

    for i in range(0,lunghezza_percorso - 1):
        lista_archi.append([i,i+1])
    
    return lista_archi

def genera_coppie_intorno(Percorso, lista_archi):
    coppie_intorno= []
    n_archi= len(lista_archi)

    for i in range(0, n_archi - 2):
        
        for j in range( i + 2, n_archi):
            arco1= lista_archi[i]
            arco2= lista_archi[j]
            coppie_intorno.append([arco1,arco2])
    
    return coppie_intorno



if __name__ == "__main__":
    k= 56
    dizionario_stazioni = {1: [10, 10], 2: [10, -10], 3: [-10, -10], 4: [-10, 10]}

    G={ 
        0: {1: 21, 2: 13, 3: 11, 4: 13, 5: 20, 6: 13, 7: 20, 8: 18, 9: 19},
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
                
    i = 1
    dizionario_citta= {}
    for element in lista_citta: 
        cliente= Cliente(element[0],element[1],dizionario_stazioni,i)
        dizionario_citta[i]= cliente
        i += 1

    Percorso= [0, 3, 2, 8, 4, '3S', 5, 1, 7, '2S', 6, 9, 0]
    
    print("soluzione_accettabile: " + str(soluzione_accettabile(Percorso, G, k , dizionario_citta, dizionario_stazioni)))
    
    tempo_tot_Percorso,_= calcola_costo(G, k, dizionario_citta, dizionario_stazioni,Percorso)
    
    print("costo: " + str(tempo_tot_Percorso))

    # -------------------------------------------------------------------------------------------------
    tour= Percorso
    tempo_tot= tempo_tot_Percorso
    # Sia genera_archi che genera_coppie_intorno ritornano indici perchè two_opt lavora sugli indici
    lista_archi= genera_archi(Percorso)
    coppie_intorno= genera_coppie_intorno(Percorso, lista_archi)
    print("coppie_intorno: " + str(coppie_intorno))
    i= 0
    dizionario_intorni= {}
    for coppia in coppie_intorno:
        nuovo_percorso= two_opt1(Percorso,dizionario_citta,dizionario_stazioni,coppia)

        if soluzione_accettabile(nuovo_percorso,G,k,dizionario_citta,dizionario_stazioni):
            tempo_tot_nuovo_percorso,_=  calcola_costo(G, k, dizionario_citta, dizionario_stazioni, nuovo_percorso)

            if tempo_tot_nuovo_percorso < tempo_tot:
                tour= nuovo_percorso
                tempo_tot= tempo_tot_nuovo_percorso

                chiave= []
                for el in coppia: 
                    chiave1= tuple(el)
                    chiave.append(chiave1)
                    
                dizionario_intorni[tuple(chiave)]= [tour, tempo_tot]
    
    print("S0: " + str(Percorso))
    print("tempo_tot_percorso: " + str(tempo_tot_Percorso))

    print("dizionario_intorni: " + str(dizionario_intorni))

    print("ottimo_locale: " + str(tour))
    print("costo_ottimo_locale: " + str(tempo_tot))  
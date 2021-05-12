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

            # Non posso selezionare 2 archi consecutivi
            arco1_nodi= [ Percorso[arco1[0]], Percorso[arco1[1]] ]
            arco2_nodi= [ Percorso[arco2[0]], Percorso[arco2[1]] ]
            
            if arco1_nodi[0] in arco2_nodi or arco1_nodi[1] in arco2_nodi:
                index_nodo1= -1
                index_nodo2= -1
            else:
                index_nodi_scelti= [index_nodo1,index_nodo2]
                archi_scelti= [[arco1[0],arco1[1]], [arco2[0],arco2[1]]]

    return archi_scelti

# Mossa generatrice di intorno
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


# Versione con scelta nodi fuori da two_opt in modo da fare una tabella di coppie di archi gia scelti (Per local search)
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
    #print("archi_scelti: " + str(archi_scelti))
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



def two_opt_subsequence(Subsequence, dizionario_citta, dizionario_stazioni, archi_scelti):
    
    nuovo_percorso= []
    #print("archi_scelti: " + str(archi_scelti))
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
        nuovo_percorso= Subsequence[0:(index1arco1 + 1)]
    else:
        # Se il primo vertice del primo arco ha indice 0 allora è per forza il nodo 0
        nuovo_percorso.append(Subsequence[0])
    
    # Arrivato al primo vertice del primo arco devo aggiungere al percorso il primo vertice del secondo arco
    nuovo_percorso.append(Subsequence[index1arco2])

    # Ora devo aggiungere a ritroso, a partire dal primo vertice del secondo arco, fino al secondo vertice del primo arco
    lista= Subsequence[(index2arco1 + 1):index1arco2]
    lista.reverse()

    nuovo_percorso=  nuovo_percorso + lista

    nuovo_percorso.append(Subsequence[index2arco1])


    # Se il secondo vertice del secondo arco è 0 allora devo solo aggiungere 0 
    if index2arco2 == len(Subsequence) - 1:
        nuovo_percorso.append(Subsequence[len(Subsequence) - 1])
    else:

        listaFinale= Subsequence[index2arco2:]
        nuovo_percorso = nuovo_percorso + listaFinale

    #print("\narchi_scelti: " + str(archi_scelti))
    
    return nuovo_percorso


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

    
# ---------------------------------------------


def local_search_2_otp(percorso, tempo_tot_Percorso, G, k, dizionario_citta, dizionario_stazioni):
    dizionario_intorni= {}

    tour= percorso
    tempo_tot= tempo_tot_Percorso

    # Sia genera_archi che genera_coppie_intorno ritornano indici perchè two_opt lavora sugli indici
    lista_archi= genera_archi(percorso)
    coppie_intorno= genera_coppie_intorno(percorso, lista_archi)

    #print("coppie_intorno: " + str(coppie_intorno))

    coppia_scelta= -1
    for coppia in coppie_intorno:
        nuovo_percorso= two_opt_subsequence(percorso,dizionario_citta,dizionario_stazioni,coppia)
        #nuovo_percorso= two_opt1(percorso,dizionario_citta,dizionario_stazioni,coppia)

        if soluzione_accettabile(nuovo_percorso,G,k,dizionario_citta,dizionario_stazioni):
            tempo_tot_nuovo_percorso,_=  calcola_costo(G, k, dizionario_citta, dizionario_stazioni, nuovo_percorso)

            if tempo_tot_nuovo_percorso < tempo_tot:
                coppia_scelta= coppia
                tour= nuovo_percorso
                tempo_tot= tempo_tot_nuovo_percorso

                chiave= []
                for el in coppia: 
                    chiave1= tuple(el)
                    chiave.append(chiave1)
                    
                dizionario_intorni[tuple(chiave)]= [tour, tempo_tot]
    
    """print("S0: " + str(percorso))
    print("tempo_tot_percorso: " + str(tempo_tot_Percorso))

    #print("dizionario_intorni: " + str(dizionario_intorni))
    print("\nCoppia Scelta(Indici): " + str(coppia_scelta))
    print("ottimo_locale: " + str(tour))
    print("costo_ottimo_locale: " + str(tempo_tot)) """

    return tour, tempo_tot



if __name__ == "__main__":
    k= 56
    dizionario_stazioni = {1: [10, 10], 2: [10, -10], 3: [-10, -10], 4: [-10, 10] }
    #Istanza 4
    lista_citta=[
                [17, 16],
                [-5, -6],
                [16, -11],
                [11, -10],
                [-2, 20],
                [-2, 4],
                [18, 11],
                [6, -15],
                [-3, -12],
                [7, 15],
                [-16, -15],
                [-9, -10],
                [3, -18],
                [18, -16],
                [-5, -8],
                [-17, 4],
                [-18, -16],
                [-3, -9],
                [17, 4],
                [-1, -10],
                [-11, -13],
                [18, 6],
                [-10, 14],
                [-5, -10],
                [-15, -1],
                [7, 14],
                [4, 20],
                [-20, 9],
                [-12, -9]
            ]

    G={ 
        0: {1: 23, 2: 7, 3: 19, 4: 14, 5: 20, 6: 4, 7: 21, 8: 16, 9: 12, 10: 16, 11: 21, 12: 13, 13: 18, 14: 24, 15: 9, 16: 17, 17: 24, 18: 9, 19: 17, 20: 10, 21: 17, 22: 18, 23: 17, 24: 11, 25: 15, 26: 15, 27: 20, 28: 21, 29: 15},
        1: {0: 23, 2: 31, 3: 27, 4: 26, 5: 19, 6: 22, 7: 5, 8: 32, 9: 34, 10: 10, 11: 45, 12: 36, 13: 36, 14: 32, 15: 32, 16: 36, 17: 47, 18: 32, 19: 12, 20: 31, 21: 40, 22: 10, 23: 27, 24: 34, 25: 36, 26: 10, 27: 13, 28: 37, 29: 38},
        2: {0: 7, 1: 31, 3: 21, 4: 16, 5: 26, 6: 10, 7: 28, 8: 14, 9: 6, 10: 24, 11: 14, 12: 5, 13: 14, 14: 25, 15: 2, 16: 15, 17: 16, 18: 3, 19: 24, 20: 5, 21: 9, 22: 25, 23: 20, 24: 4, 25: 11, 26: 23, 27: 27, 28: 21, 29: 7},
        3: {0: 19, 1: 27, 2: 21, 4: 5, 5: 35, 6: 23, 7: 22, 8: 10, 9: 19, 10: 27, 11: 32, 12: 25, 13: 14, 14: 5, 15: 21, 16: 36, 17: 34, 18: 19, 19: 15, 20: 17, 21: 27, 22: 17, 23: 36, 24: 21, 25: 32, 26: 26, 27: 33, 28: 41, 29: 28},
        4: {0: 14, 1: 26, 2: 16, 3: 5, 5: 32, 6: 19, 7: 22, 8: 7, 9: 14, 10: 25, 11: 27, 12: 20, 13: 11, 14: 9, 15: 16, 16: 31, 17: 29, 18: 14, 19: 15, 20: 12, 21: 22, 22: 17, 23: 31, 24: 16, 25: 27, 26: 24, 27: 30, 28: 36, 29: 23},
        5: {0: 20, 1: 19, 2: 26, 3: 35, 4: 32, 6: 16, 7: 21, 8: 35, 9: 32, 10: 10, 11: 37, 12: 30, 13: 38, 14: 41, 15: 28, 16: 21, 17: 39, 18: 29, 19: 24, 20: 30, 21: 34, 22: 24, 23: 10, 24: 30, 25: 24, 26: 10, 27: 6, 28: 21, 29: 30},
        6: {0: 4, 1: 22, 2: 10, 3: 23, 4: 19, 5: 16, 7: 21, 8: 20, 9: 16, 10: 14, 11: 23, 12: 15, 13: 22, 14: 28, 15: 12, 16: 15, 17: 25, 18: 13, 19: 19, 20: 14, 21: 19, 22: 20, 23: 12, 24: 14, 25: 13, 26: 13, 27: 17, 28: 18, 29: 16},
        7: {0: 21, 1: 5, 2: 28, 3: 22, 4: 22, 5: 21, 6: 21, 8: 28, 9: 31, 10: 11, 11: 42, 12: 34, 13: 32, 14: 27, 15: 29, 16: 35, 17: 45, 18: 29, 19: 7, 20: 28, 21: 37, 22: 5, 23: 28, 24: 31, 25: 35, 26: 11, 27: 16, 28: 38, 29: 36},
        8: {0: 16, 1: 32, 2: 14, 3: 10, 4: 7, 5: 35, 6: 20, 7: 28, 9: 9, 10: 30, 11: 22, 12: 15, 13: 4, 14: 12, 15: 13, 16: 29, 17: 24, 18: 10, 19: 21, 20: 8, 21: 17, 22: 24, 23: 33, 24: 12, 25: 25, 26: 29, 27: 35, 28: 35, 29: 18},
        9: {0: 12, 1: 34, 2: 6, 3: 19, 4: 14, 5: 32, 6: 16, 7: 31, 8: 9, 10: 28, 11: 13, 12: 6, 13: 8, 14: 21, 15: 4, 16: 21, 17: 15, 18: 3, 19: 25, 20: 2, 21: 8, 22: 27, 23: 26, 24: 2, 25: 16, 26: 27, 27: 32, 28: 27, 29: 9},
        10: {0: 16, 1: 10, 2: 24, 3: 27, 4: 25, 5: 10, 6: 14, 7: 11, 8: 30, 9: 28, 11: 37, 12: 29, 13: 33, 14: 32, 15: 25, 16: 26, 17: 39, 18: 26, 19: 14, 20: 26, 21: 33, 22: 14, 23: 17, 24: 27, 25: 27, 26: 1, 27: 5, 28: 27, 29: 30},
        11: {0: 21, 1: 45, 2: 14, 3: 32, 4: 27, 5: 37, 6: 23, 7: 42, 8: 22, 9: 13, 10: 37, 12: 8, 13: 19, 14: 34, 15: 13, 16: 19, 17: 2, 18: 14, 19: 38, 20: 15, 21: 5, 22: 39, 23: 29, 24: 12, 25: 14, 26: 37, 27: 40, 28: 24, 29: 7},
        12: {0: 13, 1: 36, 2: 5, 3: 25, 4: 20, 5: 30, 6: 15, 7: 34, 8: 15, 9: 6, 10: 29, 11: 8, 13: 14, 14: 27, 15: 4, 16: 16, 17: 10, 18: 6, 19: 29, 20: 8, 21: 3, 22: 31, 23: 24, 24: 4, 25: 10, 26: 28, 27: 32, 28: 21, 29: 3},
        13: {0: 18, 1: 36, 2: 14, 3: 14, 4: 11, 5: 38, 6: 22, 7: 32, 8: 4, 9: 8, 10: 33, 11: 19, 12: 14, 14: 15, 15: 12, 16: 29, 17: 21, 18: 10, 19: 26, 20: 8, 21: 14, 22: 28, 23: 34, 24: 11, 25: 24, 26: 32, 27: 38, 28: 35, 29: 17},
        14: {0: 24, 1: 32, 2: 25, 3: 5, 4: 9, 5: 41, 6: 28, 7: 27, 8: 12, 9: 21, 10: 32, 11: 34, 12: 27, 13: 15, 15: 24, 16: 40, 17: 36, 18: 22, 19: 20, 20: 19, 21: 29, 22: 22, 23: 41, 24: 23, 25: 36, 26: 31, 27: 38, 28: 45, 29: 30},
        15: {0: 9, 1: 32, 2: 2, 3: 21, 4: 16, 5: 28, 6: 12, 7: 29, 8: 13, 9: 4, 10: 25, 11: 13, 12: 4, 13: 12, 14: 24, 16: 16, 17: 15, 18: 2, 19: 25, 20: 4, 21: 7, 22: 26, 23: 22, 24: 2, 25: 12, 26: 25, 27: 29, 28: 22, 29: 7},
        16: {0: 17, 1: 36, 2: 15, 3: 36, 4: 31, 5: 21, 6: 15, 7: 35, 8: 29, 9: 21, 10: 26, 11: 19, 12: 16, 13: 29, 14: 40, 15: 16, 17: 20, 18: 19, 19: 34, 20: 21, 21: 18, 22: 35, 23: 12, 24: 18, 25: 5, 26: 26, 27: 26, 28: 5, 29: 13},
        17: {0: 24, 1: 47, 2: 16, 3: 34, 4: 29, 5: 39, 6: 25, 7: 45, 8: 24, 9: 15, 10: 39, 11: 2, 12: 10, 13: 21, 14: 36, 15: 15, 16: 20, 18: 16, 19: 40, 20: 18, 21: 7, 22: 42, 23: 31, 24: 14, 25: 15, 26: 39, 27: 42, 28: 25, 29: 9},
        18: {0: 9, 1: 32, 2: 3, 3: 19, 4: 14, 5: 29, 6: 13, 7: 29, 8: 10, 9: 3, 10: 26, 11: 14, 12: 6, 13: 10, 14: 22, 15: 2, 16: 19, 17: 16, 19: 23, 20: 2, 21: 8, 22: 25, 23: 24, 24: 2, 25: 14, 26: 25, 27: 29, 28: 24, 29: 9},
        19: {0: 17, 1: 12, 2: 24, 3: 15, 4: 15, 5: 24, 6: 19, 7: 7, 8: 21, 9: 25, 10: 14, 11: 38, 12: 29, 13: 26, 14: 20, 15: 25, 16: 34, 17: 40, 18: 23, 20: 22, 21: 32, 22: 2, 23: 28, 24: 26, 25: 32, 26: 14, 27: 20, 28: 37, 29: 31},
        20: {0: 10, 1: 31, 2: 5, 3: 17, 4: 12, 5: 30, 6: 14, 7: 28, 8: 8, 9: 2, 10: 26, 11: 15, 12: 8, 13: 8, 14: 19, 15: 4, 16: 21, 17: 18, 18: 2, 19: 22, 21: 10, 22: 24, 23: 25, 24: 4, 25: 16, 26: 25, 27: 30, 28: 26, 29: 11},
        21: {0: 17, 1: 40, 2: 9, 3: 27, 4: 22, 5: 34, 6: 19, 7: 37, 8: 17, 9: 8, 10: 33, 11: 5, 12: 3, 13: 14, 14: 29, 15: 7, 16: 18, 17: 7, 18: 8, 19: 32, 20: 10, 22: 34, 23: 27, 24: 6, 25: 12, 26: 32, 27: 36, 28: 23, 29: 4},
        22: {0: 18, 1: 10, 2: 25, 3: 17, 4: 17, 5: 24, 6: 20, 7: 5, 8: 24, 9: 27, 10: 14, 11: 39, 12: 31, 13: 28, 14: 22, 15: 26, 16: 35, 17: 42, 18: 25, 19: 2, 20: 24, 21: 34, 23: 29, 24: 28, 25: 33, 26: 13, 27: 19, 28: 38, 29: 33},
        23: {0: 17, 1: 27, 2: 20, 3: 36, 4: 31, 5: 10, 6: 12, 7: 28, 8: 33, 9: 26, 10: 17, 11: 29, 12: 24, 13: 34, 14: 41, 15: 22, 16: 12, 17: 31, 18: 24, 19: 28, 20: 25, 21: 27, 22: 29, 24: 24, 25: 15, 26: 17, 27: 15, 28: 11, 29: 23},
        24: {0: 11, 1: 34, 2: 4, 3: 21, 4: 16, 5: 30, 6: 14, 7: 31, 8: 12, 9: 2, 10: 27, 11: 12, 12: 4, 13: 11, 14: 23, 15: 2, 16: 18, 17: 14, 18: 2, 19: 26, 20: 4, 21: 6, 22: 28, 23: 24, 25: 13, 26: 26, 27: 31, 28: 24, 29: 7},
        25: {0: 15, 1: 36, 2: 11, 3: 32, 4: 27, 5: 24, 6: 13, 7: 35, 8: 25, 9: 16, 10: 27, 11: 14, 12: 10, 13: 24, 14: 36, 15: 12, 16: 5, 17: 15, 18: 14, 19: 32, 20: 16, 21: 12, 22: 33, 23: 15, 24: 13, 26: 26, 27: 28, 28: 11, 29: 8},
        26: {0: 15, 1: 10, 2: 23, 3: 26, 4: 24, 5: 10, 6: 13, 7: 11, 8: 29, 9: 27, 10: 1, 11: 37, 12: 28, 13: 32, 14: 31, 15: 25, 16: 26, 17: 39, 18: 25, 19: 14, 20: 25, 21: 32, 22: 13, 23: 17, 24: 26, 25: 26, 27: 6, 28: 27, 29: 29},
        27: {0: 20, 1: 13, 2: 27, 3: 33, 4: 30, 5: 6, 6: 17, 7: 16, 8: 35, 9: 32, 10: 5, 11: 40, 12: 32, 13: 38, 14: 38, 15: 29, 16: 26, 17: 42, 18: 29, 19: 20, 20: 30, 21: 36, 22: 19, 23: 15, 24: 31, 25: 28, 26: 6, 28: 26, 29: 33},
        28: {0: 21, 1: 37, 2: 21, 3: 41, 4: 36, 5: 21, 6: 18, 7: 38, 8: 35, 9: 27, 10: 27, 11: 24, 12: 21, 13: 35, 14: 45, 15: 22, 16: 5, 17: 25, 18: 24, 19: 37, 20: 26, 21: 23, 22: 38, 23: 11, 24: 24, 25: 11, 26: 27, 27: 26, 29: 19},
        29: {0: 15, 1: 38, 2: 7, 3: 28, 4: 23, 5: 30, 6: 16, 7: 36, 8: 18, 9: 9, 10: 30, 11: 7, 12: 3, 13: 17, 14: 30, 15: 7, 16: 13, 17: 9, 18: 9, 19: 31, 20: 11, 21: 4, 22: 33, 23: 23, 24: 7, 25: 8, 26: 29, 27: 33, 28: 19}
    }    

    percorso= [0, 6, 19, 22, 7, 1, 26, 10, '1S', 27, 5, 23, 28, 16, '4S', 25, 29, 12, 21, 11, 17, '3S', 14, 3, 4, 8, '2S', 13, 20, 18, 24, 9, 15, 2, 0]

    i = 1
    dizionario_citta= {}
    for element in lista_citta: 
        cliente= Cliente(element[0],element[1],dizionario_stazioni,i)
        dizionario_citta[i]= cliente
        i += 1

    
    #print("soluzione_accettabile: " + str(soluzione_accettabile(percorso, G, k , dizionario_citta, dizionario_stazioni)))
    
    tempo_tot_Percorso,_= calcola_costo(G, k, dizionario_citta, dizionario_stazioni,percorso)
    
    print("costo: " + str(tempo_tot_Percorso))

    print("percorso: " + str(percorso) + "\n")

    tour, tempo_tot= local_search_2_otp(percorso, tempo_tot_Percorso, G, k, dizionario_citta, dizionario_stazioni)

    print("tour: " + str(tour))

    print("tempo_tot: " + str(tempo_tot)) 
import random
from Cliente import Cliente, euclidean_distance


def scelta_nodi(Percorso):
    nodi_scelti=[]

    while len(nodi_scelti) < 2:
        adiacenti= False
        nodo= random.choice(Percorso)

        # Se un nodo è gia stato selezionato, controllo che quello scelto non sia adiacente
        if len(nodi_scelti) == 1:
            nodo_list= nodi_scelti[0]
            
            index_nodo= Percorso.index(nodo)
            index_nodoList= Percorso.index(nodo_list)

            distanza= index_nodo - index_nodoList
            distanza_abs= abs(distanza)

            # L'adiacenza c'è anche tra il primo e l'ultimo, quindi la differenza tra il primo e l'ultimo sara sempre len(Percorso) - 1
            if distanza_abs != 1 or distanza_abs == len(Percorso) - 2:  # Metto - 2 e non - 1 perchè nella lista Percorso, l'ultimo elemento è uguale al primo
                adiacenti= False
            else:
                adiacenti= True
            
        if nodo not in nodi_scelti and not adiacenti:
            nodi_scelti.append(nodo)
        
    archi_scelti= []
    archi_scelti= [ [ nodi_scelti[0] , Percorso[Percorso.index(nodi_scelti[0]) + 1] ], [ nodi_scelti[1] , Percorso[Percorso.index(nodi_scelti[1]) + 1]] ]
    return archi_scelti

def two_opt(Percorso, dizionario_citta, dizionario_stazioni):
    nuovo_percorso= Percorso.copy()

    # Devo selezionare due archi NON adiacenti su cui fare lo swap 
    # L'arco viene identificato dal nodo selezionato e dal suo successivo
    archi_scelti= scelta_nodi(Percorso)

    # Ora devo collegarli nell'unico modo legale possibile
    # Ovvero il primo nodo di ogni arco selezionato deve connettersi con il secondo nodo dell'altro arco



    index1arco1= nuovo_percorso.index(archi_scelti[0][0])
    index1arco2= nuovo_percorso.index(archi_scelti[1][0])

    index2arco1= nuovo_percorso.index(archi_scelti[0][1])
    index2arco2= nuovo_percorso.index(archi_scelti[1][1])


    # Il nodo di partenza e di arrivo nel percorso deve essere sempre il deposito
    if 0 in archi_scelti[0]:
        # Significa che l'arco selezionato è l'arco di partenza
        if 0 == archi_scelti[0][0]:
            nuovo_percorso[index2arco1]= archi_scelti[1][1]
            nuovo_percorso[index2arco2]= archi_scelti[0][1]
        # Significa che l'arco selezionato è l'arco di arrivo
        elif 0 == archi_scelti[0][1]:
            nuovo_percorso[index1arco1]= archi_scelti[1][1]
            nuovo_percorso[index2arco1]= archi_scelti[0][1]

    elif 0 in archi_scelti[1]:
        if 0 == archi_scelti[1][0]:
            nuovo_percorso[index2arco2]= archi_scelti[0][0]
            nuovo_percorso[index1arco1]= archi_scelti[1][1]
        elif 0 == archi_scelti[1][1]:
            nuovo_percorso[index1arco2]= archi_scelti[0][1]
            nuovo_percorso[index2arco1]= archi_scelti[1][0]
    else:
        # Devo controllare l'ordine dei nodi visitati del nuovo percorso
        if index1arco1 < index1arco2:
            nuovo_percorso[index2arco1]= archi_scelti[1][0]
            nuovo_percorso[index1arco2]= archi_scelti[0][1]
        elif index1arco1 > index1arco2:
            nuovo_percorso[index2arco2]= archi_scelti[0][0]
            nuovo_percorso[index1arco1]= archi_scelti[1][1]

    print("Percorso: " + str(Percorso))
    print("archi_scelti: " + str(archi_scelti))
    print("nuovo_percorso: " + str(nuovo_percorso))

    return archi_scelti, nuovo_percorso
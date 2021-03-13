import math
from InstanceGenerator import generateInstance, euclidean_distance, manualInstance
from PlotGenerator import draw_map
from ConstructiveEuristic import NearestNeighbour, MinimumSpanningTree, Christofides_Algorithm


def print_mst(dizionario_distanze_citta, dizionario_uso_archi, distanza_mst, archi_usati):
    
    citta = list(dizionario_distanze_citta.keys())

    for n in citta:
        if n != 0:
            print("Citta: " + str(n))
        else:
            print("Deposito: ")
        print("Distanze: " + str(dizionario_distanze_citta.get(n)))


    for n in dizionario_uso_archi:
        if n != 0:
            print("Citta: " + str(n))
        else:
            print("Deposito: ")

        print("Lista_usi: " + str(dizionario_uso_archi.get(n)))


    print("Distanza_mst: " + str(distanza_mst))
    
    for arco in archi_usati:
        print("Archi usati: " + str(arco))

def print_nearest_neighbour(percorso, distanza_percorsa, tempo_totale, tempo_ricarica):
    
    città= list(dizionario_citta.keys())
    stazioni= list(dizionario_stazioni.keys())
    
    print("------------------------Citta------------------------\n")
    for key in città:
        cliente= dizionario_citta.get(int(key))
        print("\nCittà: " + str(key))
        print("\nCoordinate: " + str(cliente.coordinate))
 
    print("------------------------Stazioni di Ricarica------------------------\n")
    for key in stazioni:
        stazione= dizionario_stazioni.get(int(key))
        print("\nStazione: " + str(key) + 'S')
        print("\nCoordinate: " + str(stazione))

    print("------------------------PERCORSO------------------------\n")
    print("Percorso: " + str(percorso) + "\n")
    print("Distanza Percorsa: " + str(distanza_percorsa) + "\n")
    print("Tempo totale di viaggio: " + str(tempo_totale) + "\t di cui tempo speso in ricarica: " + str(tempo_ricarica))



if __name__ == "__main__":

    Max_Axis= int(input("Inserire i valori degli assi cartesiani: "))

    N_CITIES= int(input("Inserire il numero di città che si vogliono avere: "))

    # Per avere garantita una soluzione avremo come autonomia minima la massima distanza percorribile, ovvero la diagonale del piano cartesiano
    autonomia_minima = round(euclidean_distance([-Max_Axis,-Max_Axis],[Max_Axis,Max_Axis]),0)
    k = 0
    while k < autonomia_minima:
        k= int(input("L'autonomia minima possibile è: " + str(autonomia_minima) + "\nInserire autonomia auto: "))


    print("------------------------------------ Menu Scelta Istanze ------------------------------------ ")
    scelta_istanze= 0
    while scelta_istanze not in range(1,3):
        print("\n 1- Generare istanza randomicamente\n 2- Inserire manualmente dati istanza")
        scelta_istanze= int(input("\nDigitare scelta: "))

    if scelta_istanze == 1:
        dizionario_citta, dizionario_stazioni, coordinate_deposito= generateInstance(Max_Axis, N_CITIES) 
    elif scelta_istanze == 2:
        dizionario_citta, dizionario_stazioni, coordinate_deposito= manualInstance(Max_Axis,N_CITIES)

    deposito= 0


    #dizionario_distanze_citta, dizionario_uso_archi, distanza_mst, archi_usati= MinimumSpanningTree(dizionario_citta)
    percorso, distanza_percorsa, tempo_totale, tempo_ricarica= NearestNeighbour(dizionario_citta,dizionario_stazioni,deposito,k,N_CITIES)

    Christofides_Algorithm(dizionario_citta, dizionario_stazioni, Max_Axis)
    
    scelta_stampe= 1
    while scelta_stampe != 0:

        print("------------------------------------ Menu Stampe ------------------------------------ ")
        print("\n1- Stampa risultati Nearest Neighbour")
        print("2- Stampa risultati Minimum Spanning Tree (Kruskal Algorithm)")
        print("0- Exit")

        scelta_stampe= int(input("\nScelta: "))
    # Stampo i risultati
        if scelta_stampe == 1:
            print_nearest_neighbour(percorso, distanza_percorsa, tempo_totale, tempo_ricarica)
        #elif scelta_stampe == 2:
        # print_mst(dizionario_distanze_citta, dizionario_uso_archi, distanza_mst, archi_usati)
        elif scelta_stampe == 0:
            break








    
    
    #print("subgraph_keys: " + str(subgraph_keys))
# Creo le immagini
    # Disegna NearestNeighbour
    draw_map(percorso, dizionario_citta, dizionario_stazioni, Max_Axis)


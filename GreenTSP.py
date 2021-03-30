import math
import time
import PlotGenerator as plt
from InstanceHandler import generateInstance, manualInstance, leggi_istanza, salva_istanza
from PlotGenerator import draw_map, print_2_opt, print_2_opt_arc_selected
from ConstructiveEuristic import NearestNeighbour, Christofides_Algorithm, NearestNeighbour_ottimizzazione_ricarica, MinimumSpanningTree, find_odd_degree_verteces, create_induced_subgraph, find_perfect_matching
from Cliente import euclidean_distance
from LocalSearch import two_opt



if __name__ == "__main__":
    scelta_istanze= 1
    scelta_directory= 1
    while scelta_istanze != 0:
        print("------------------------------------ Menu Scelta Istanze ------------------------------------ ")
        print("\n 1- Generare istanza randomicamente\n 2- Inserire manualmente dati istanza\n 3- Leggi Istanza da istanze salvate\n 0- Exit")
        scelta_istanze= int(input("\nDigitare scelta: "))

        if scelta_istanze == 0:
            break

        if scelta_istanze == 1 or scelta_istanze == 2:

            Max_Axis= int(input("Inserire i valori degli assi cartesiani: "))

            N_CITIES= int(input("Inserire il numero di città che si vogliono avere: "))

            # Per avere garantita una soluzione avremo come autonomia minima la massima distanza percorribile, ovvero la diagonale del piano cartesiano
            autonomia_minima = round(euclidean_distance([-Max_Axis,-Max_Axis],[Max_Axis,Max_Axis]),0)
            k = 0
            while k < autonomia_minima:
                k= int(input("L'autonomia minima possibile è: " + str(autonomia_minima) + "\nInserire autonomia auto: "))

            # Scelta
            if scelta_istanze == 1:
                dizionario_citta, dizionario_stazioni, coordinate_deposito= generateInstance(Max_Axis, N_CITIES)
            else:
                dizionario_citta, dizionario_stazioni, coordinate_deposito= manualInstance(Max_Axis,N_CITIES)

            scelta_directory= 1
            
        elif scelta_istanze == 3:

            coordinate_deposito= [0,0]
            dizionario_citta, dizionario_stazioni, k , Max_Axis, N_CITIES, scelta_directory= leggi_istanza()
  
        if scelta_directory != 0:

            scelta_algoritmi= 1
            print("------------------------------------ Menu Algoritmi Costruttivi ------------------------------------")
            print("Eseguo algoritmi...")
            print("...Esecuzione Nearest_Neighbour...")
            start_NN= time.time()
            dizionario_Nearest_Neighbour= NearestNeighbour(dizionario_citta,dizionario_stazioni,k,N_CITIES, Max_Axis)
            endt_NN= time.time()
            print("Tempo esecuzione: " + str(endt_NN - start_NN))
            print("... Fine Esecuzione Nearest_Neighbour...")
            print("... Esecuzione Christofides ...")
            start_Christofides= time.time()
            dizionario_Christofides= Christofides_Algorithm(dizionario_citta, dizionario_stazioni, Max_Axis, k)
            end_Christofides= time.time()
            print("Tempo esecuzione: " + str(end_Christofides - start_Christofides))
            print("... Fine Esecuzione Christofides...")
            print("Fine eseguzione algoritmi...")
            print("--Esecuzione NearestNeighbour con ricarica ottimizzata...")
            start_NN_Opt= time.time()
            dizionario_Nearest_Neighbour_ott_ricarica= NearestNeighbour_ottimizzazione_ricarica(dizionario_citta,dizionario_stazioni,k,N_CITIES,Max_Axis)
            end_NN_Opt= time.time()
            print("Tempo esecuzione: " + str(end_NN_Opt - start_NN_Opt))
            print("--Fine Esecuzione NearestNeighbour con ricarica ottimizzata...")
            print("------------------------------------ Menu Stampe ------------------------------------ ") 
            scelta_stampe= 1
            while scelta_stampe != 0:
                print("\n1- Stampa Christofides")
                print("2- Stampa Nearest Neighbour")
                print("3- Stampa NNOttimizzazione Ricarica")
                print("0- Exit")

                scelta_stampe= int(input("\nScelta: "))

            # Stampo i risultati

                if scelta_stampe == 1:
                    print("------ Algoritmo Costruttivo non Greedy Christofides ------")
                    print("Percorso Christofides: " + str(dizionario_Christofides['percorso']))
                    print("Distanza: "  + str(dizionario_Christofides['distanza']))
                    print("Tempo viaggio: " + str(dizionario_Christofides['tempo_tot']))
                    print("Tempo ricarica: " + str(dizionario_Christofides['tempo_ricarica']))
                elif scelta_stampe == 2:
                    print("------ Algoritmo Costruttivo Greedy Nearest_Neighbour ------")
                    print("Percorso Nearest_Neighbour: " + str(dizionario_Nearest_Neighbour['percorso']))
                    print("Distanza: "  + str(dizionario_Nearest_Neighbour['distanza']))
                    print("Tempo viaggio: " + str(dizionario_Nearest_Neighbour['tempo_tot']))
                    print("Tempo ricarica: " + str(dizionario_Nearest_Neighbour['tempo_ricarica']))
                elif scelta_stampe == 3:
                    print("------ Algoritmo Costruttivo Greedy Nearest_Neighbour con ricarica ottimizzata ------")
                    print("Percorso Nearest_Neighbour: " + str(dizionario_Nearest_Neighbour_ott_ricarica['percorso']))
                    print("Distanza: "  + str(dizionario_Nearest_Neighbour_ott_ricarica['distanza']))
                    print("Tempo viaggio: " + str(dizionario_Nearest_Neighbour_ott_ricarica['tempo_tot']))
                    print("Tempo ricarica: " + str(dizionario_Nearest_Neighbour_ott_ricarica['tempo_ricarica']))
                elif scelta_stampe == 0:
                    break


            print("\nSalvare l'istanza corrente? y/n:")
            scelta_salvataggio=input("\nScelta: ")
            if scelta_salvataggio == 'y':
                salva_istanza(dizionario_Nearest_Neighbour, dizionario_Christofides, dizionario_Nearest_Neighbour_ott_ricarica, dizionario_citta, dizionario_stazioni, Max_Axis, k)

            print("----------- Local Search -----------")
            
            archi_scelti, nuovo_percorso= two_opt(dizionario_Christofides['percorso'], dizionario_citta, dizionario_stazioni)

            print_2_opt(nuovo_percorso, dizionario_citta, dizionario_stazioni, Max_Axis)
            print_2_opt_arc_selected(dizionario_Christofides['percorso'], archi_scelti, dizionario_citta, dizionario_stazioni, Max_Axis)
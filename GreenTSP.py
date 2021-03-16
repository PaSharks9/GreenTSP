import math
from InstanceGenerator import generateInstance, euclidean_distance, manualInstance, leggi_istanza, salva_istanza
from PlotGenerator import draw_map
from ConstructiveEuristic import NearestNeighbour, MinimumSpanningTree, Christofides_Algorithm

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
            deposito= 0

            scelta_algoritmi= 1
            print("------------------------------------ Menu Algoritmi Costruttivi ------------------------------------")
            print("Eseguo algoritmi...")
            print("...Esecuzione Nearest_Neighbour...")
            dizionario_Nearest_Neighbour= NearestNeighbour(dizionario_citta,dizionario_stazioni,deposito,k,N_CITIES, Max_Axis)
            print("... Fine Esecuzione Nearest_Neighbour...")
            print("... Esecuzione Christofides ...")
            dizionario_Christofides= Christofides_Algorithm(dizionario_citta, dizionario_stazioni, Max_Axis, k)
            print("... Fine Esecuzione Christofides...")
            print("Fine eseguzione algoritmi...")
            print("------------------------------------ Menu Stampe ------------------------------------ ") 
            scelta_stampe= 1
            while scelta_stampe != 0:
                print("\n1- Stampa Nearest Neighbour")
                print("2- Stampa Christofides")
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
                elif scelta_stampe == 0:
                    break


            print("\nSalvare l'istanza corrente? y/n:")
            scelta_salvataggio=input("\nScelta: ")

            if scelta_salvataggio == 'y':
                salva_istanza(dizionario_Nearest_Neighbour, dizionario_Christofides, dizionario_citta, dizionario_stazioni, Max_Axis, k)


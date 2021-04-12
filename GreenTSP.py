import math
import time
import PlotGenerator as plt
from SimulatedAnnealing import simulated_annealing
from InstanceHandler import generateInstance, manualInstance, leggi_istanza, salva_risultati
from PlotGenerator import draw_map, print_2_opt, print_2_opt_arc_selected
from ConstructiveEuristic import NearestNeighbour, Christofides_Algorithm, NearestNeighbour_ottimizzazione_ricarica, create_distance_dict
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

        # Creo il dizionario delle distanze delle citta
        G= create_distance_dict(dizionario_citta)

        if scelta_directory != 0:

            scelta_algoritmi= 1
            print("------------------------------------  Algoritmi Costruttivi ------------------------------------")
            print("Eseguo algoritmi...")
            print("...Esecuzione Nearest_Neighbour...")
            start_NN= time.time()
            dizionario_Nearest_Neighbour= NearestNeighbour(dizionario_citta,dizionario_stazioni,k,N_CITIES, Max_Axis)
            endt_NN= time.time()
            dizionario_Nearest_Neighbour['tempo_esec']= str(endt_NN - start_NN)
            print("... Fine Esecuzione Nearest_Neighbour...")
            print("... Esecuzione Christofides ...")
            start_Christofides= time.time()
            dizionario_Christofides= Christofides_Algorithm(dizionario_citta, dizionario_stazioni, Max_Axis, k)
            end_Christofides= time.time()
            dizionario_Christofides['tempo_esec']= str(end_Christofides - start_Christofides)
            print("... Fine Esecuzione Christofides...")
            print("Fine eseguzione algoritmi...")

            print("------------------------------------ Menu Stampe ------------------------------------ ") 
            scelta_stampe= 1
            while scelta_stampe != 0:
                print("\n1- Stampa Christofides")
                print("2- Stampa Nearest Neighbour")
                print("0- Exit")

                scelta_stampe= int(input("\nScelta: "))

            # Stampo i risultati

                if scelta_stampe == 1:
                    print("------ Algoritmo Costruttivo non Greedy Christofides ------")
                    print("Percorso Christofides: " + str(dizionario_Christofides['percorso']))
                    print("Distanza: "  + str(dizionario_Christofides['distanza']))
                    print("Tempo viaggio: " + str(dizionario_Christofides['tempo_tot']))
                    print("Tempo ricarica: " + str(dizionario_Christofides['tempo_ricarica']))
                    print("Tempo esecuzione: " + str(end_Christofides - start_Christofides))
                elif scelta_stampe == 2:
                    print("------ Algoritmo Costruttivo Greedy Nearest_Neighbour ------")
                    print("Percorso Nearest_Neighbour: " + str(dizionario_Nearest_Neighbour['percorso']))
                    print("Distanza: "  + str(dizionario_Nearest_Neighbour['distanza']))
                    print("Tempo viaggio: " + str(dizionario_Nearest_Neighbour['tempo_tot']))
                    print("Tempo ricarica: " + str(dizionario_Nearest_Neighbour['tempo_ricarica']))
                    print("Tempo esecuzione: " + str(endt_NN - start_NN))
                elif scelta_stampe == 0:
                    break


            print("------------------------------------ Esecuzione Meta-Euristiche ------------------------------------")
            print("----------- Simulated Annealing -----------")
            numero_iterazioni= math.factorial(N_CITIES-1)//500
            Temperature=  N_CITIES*100
            Tfrozen= 10
            n_esecuzioni= 5
            print("Parametri di Default:")
            print("Temperature: " + str(Temperature))
            print("Tfrozen: " + str(Tfrozen))
            print("Numero Iterazioni: " + str(numero_iterazioni))
            print("Numero di esecuzioni dell'algoritmo: " + str(n_esecuzioni))
            scelta_param= input("Inserire y/n per usare parametri di default: ")
            if scelta_param == 'n':
                numero_iterazioni= int(input("\nInserire il numero di iterazioni da effettuare: "))
                Temperature= int(input("\nInserire la temperatura iniziale desiderata: "))
                Tfrozen= int(input("\nInserire il valore di TFrozen: "))
                n_esecuzioni= int(input("\nInserire il numero di volte che si vuole eseguire l'algoritmo: "))
            
            scelta_meta_euristica= -1
            while scelta_meta_euristica != 0:
                dizionario_SA_NN= {}
                dizionario_SA_C= {}
                
                print("\nScegliere quale soluzione processare tramite Simulated Annealing: ")
                print("-1 Nearest Neighbour Solution")
                print("-2 Christofides Solution")
                print("-3 Entrambe le soluzioni")
                print("-0 Exit")
                scelta_meta_euristica= int(input("Scelta: "))

                if scelta_meta_euristica == 1:    # SA con Nearest Neighbour
                    print("\nSimulated Annealing con soluzione Nearest Neighbour")
                    start_SA_NN= time.time()
                    dizionario_SA_NN, dizionario_sol_migliore_NN= simulated_annealing(dizionario_Nearest_Neighbour, dizionario_citta, dizionario_stazioni, G, k, Temperature, Tfrozen, numero_iterazioni, n_esecuzioni)
                    end_SA_NN= time.time()
                    
                    dizionario_SA_NN['tempo_esec']= str(end_SA_NN - start_SA_NN)
                    # Stampa risultati
                    print("----------- Risultati Simulated Annealing -----------")
                    print("--- Matrice Distanza ---")
                    print(str(G))
                    print("--- Dizionario Stazioni ---")
                    print(str(dizionario_stazioni))
                    citta= list(dizionario_citta.keys())
                    for citt in citta:
                        coord= dizionario_citta.get(citt)
                        coordinate= coord.coordinate
                        print(str(citt) + ': ' + str(coordinate))

                    print("- Con Nearest Neighbour")
                    N_esecuzioni= list(dizionario_SA_NN.keys())
                    for esec in N_esecuzioni:
                        if esec  != 'tempo_esec':
                            dizionario_NN= dizionario_SA_NN[int(esec)]
                            print("Tour: " + str(dizionario_NN['soluzione_migliore']))
                            print("Distanza percorsa: " + str(dizionario_NN['distanza_percorsa_migliore']))
                            print("Durata Tour: " + str(dizionario_NN['costo_sol_migliore']))
                            print("Tempo esecuzione:  " + str(dizionario_NN['tempo_esecuzione']))
                    
                    print("\nTempo esecuzione totale: " + str(dizionario_SA_NN['tempo_esec']))

                elif scelta_meta_euristica == 2:   # SA con Christofides
                    print("\nSimulated Annealing con soluzione Christofides")

                    start_SA_C= time.time()
                    dizionario_SA_C, dizionario_sol_migliore_C= simulated_annealing(dizionario_Christofides, dizionario_citta, dizionario_stazioni, G, k, Temperature, Tfrozen, numero_iterazioni, n_esecuzioni)
                    start_SA_NN= time.time()
                    end_SA_C= time.time()
                    
                    dizionario_SA_C['tempo_esec']= str(end_SA_C - start_SA_C)

                    # Stampa risultati
                    print("----------- Risultati Simulated Annealing -----------")
                    print("--- Matrice Distanza ---")
                    print(str(G))
                    print("--- Dizionario Stazioni ---")
                    print(str(dizionario_stazioni))
                    print("--- Coordinate Citta ---")

                    citta= list(dizionario_citta.keys())
                    for citt in citta:
                        coord= dizionario_citta.get(citt)
                        coordinate= coord.coordinate
                        print(str(citt) + ': ' + str(coordinate))

                    print("- Con Christofides")
                    N_esecuzioni= list(dizionario_SA_C.keys())
                    for esec in N_esecuzioni:
                        if esec  != 'tempo_esec':
                            dizionario_C= dizionario_SA_C[int(esec)]
                            print("Tour: " + str(dizionario_C['soluzione_migliore']))
                            print("Distanza percorsa: " + str(dizionario_C['distanza_percorsa_migliore']))
                            print("Durata Tour: " + str(dizionario_C['costo_sol_migliore']))
                            print("Tempo esecuzione:  " + str(dizionario_C['tempo_esecuzione']))
                    print("\nTempo esecuzione totale: " + str(dizionario_SA_C['tempo_esec']))

                elif scelta_meta_euristica == 3:

                    print("\nSimulated Annealing con soluzione Nearest Neighbour")
                    start_SA_NN= time.time()
                    dizionario_SA_NN, dizionario_sol_migliore_NN= simulated_annealing(dizionario_Nearest_Neighbour, dizionario_citta, dizionario_stazioni, G, k, Temperature, Tfrozen, numero_iterazioni, n_esecuzioni)
                    end_SA_NN= time.time()

                    print("\nSimulated Annealing con soluzione Christofides")
                    start_SA_C= time.time()
                    dizionario_SA_C, dizionario_sol_migliore_C= simulated_annealing(dizionario_Christofides, dizionario_citta, dizionario_stazioni, G, k, Temperature, Tfrozen, numero_iterazioni, n_esecuzioni)
                    end_SA_C= time.time()

                    dizionario_SA_NN['tempo_esec']= str(end_SA_NN - start_SA_NN)
                    dizionario_SA_C['tempo_esec']= str(end_SA_C - start_SA_C)


                    # Stampa risultati
                    print("----------- Risultati Simulated Annealing -----------")
                    print("--- Matrice Distanza ---")
                    print(str(G))
                    print("--- Dizionario Stazioni ---")
                    print(str(dizionario_stazioni))
                    print("--- Coordinate Citta ---")

                    citta= list(dizionario_citta.keys())
                    for citt in citta:
                        coord= dizionario_citta.get(citt)
                        coordinate= coord.coordinate
                        print(str(citt) + ': ' + str(coordinate))

                    print("- Con Nearest Neighbour")
                    N_esecuzioni= list(dizionario_SA_NN.keys())
                    for esec in N_esecuzioni:
                        if esec  != 'tempo_esec':
                            dizionario_NN= dizionario_SA_NN[int(esec)]
                            print("Tour: " + str(dizionario_NN['soluzione_migliore']))
                            print("Distanza percorsa: " + str(dizionario_NN['distanza_percorsa_migliore']))
                            print("Durata Tour: " + str(dizionario_NN['costo_sol_migliore']))
                            print("Tempo esecuzione:  " + str(dizionario_NN['tempo_esecuzione']))
                    print("\nTempo esecuzione totale: " + str(dizionario_SA_NN['tempo_esec']))

                    print("- Con Christofides")
                    n_esecuzioni= list(dizionario_SA_C.keys())
                    for esec in n_esecuzioni:
                        if esec  != 'tempo_esec':
                            dizionario_C= dizionario_SA_C[int(esec)]
                            print("Tour: " + str(dizionario_NN['soluzione_migliore']))
                            print("Distanza percorsa: " + str(dizionario_C['distanza_percorsa_migliore']))
                            print("Durata Tour: " + str(dizionario_C['costo_sol_migliore']))
                            print("Tempo esecuzione:  " + str(dizionario_C['tempo_esecuzione']))
                    print("\nTempo esecuzione totale: " + str(dizionario_SA_C['tempo_esec']))



                # ----------------------- Salvataggio Risultati Algoritmi------------------------------------
                if scelta_meta_euristica != 0:
                    print("\n----------- Salvataggio Risultati -----------")
                    scelta_salvataggioSA= -1
                    while scelta_salvataggioSA != 'y' and scelta_salvataggioSA != 'n':
                        scelta_salvataggioSA= input("Salvare risultati? y/n\n")
                        if scelta_salvataggioSA != 'y' and scelta_salvataggioSA != 'n':
                            print("Inserimento errato... Inserire o 'y' o 'n'\n")
                        else:
                            if scelta_salvataggioSA == 'y':

                                dizionario_risultati= {}
                                dizionario_SA={}
                                dizionario_ILS={} #Iterative Local Search
                                dizionario_Costructive= {}

                                dizionario_Costructive['NearestNeighbour']= dizionario_Nearest_Neighbour
                                dizionario_Costructive['Christofides']= dizionario_Christofides
                                dizionario_risultati['Costruttive']= dizionario_Costructive

                                # Caratteristiche con cui viene svolto il SA
                                dizionario_SA['n_iterazioni']=  numero_iterazioni
                                dizionario_SA['Temperatura']= Temperature
                                dizionario_SA['Tfrozen']= Tfrozen

                                dizionario_SA['NN']= dizionario_SA_NN
                                dizionario_SA['C']= dizionario_SA_C
                                dizionario_risultati['SA']= dizionario_SA

                                """dizionario_ILS['NN']= dizionario_ILS_NN
                                dizionario_ILS['C']= dizionario_ILS_C
                                dizionario_risultati['ILS']= dizionario_ILS"""
                                if scelta_meta_euristica == 1:
                                    dizionario_risultati['sol_migl_C'] = {}
                                    dizionario_risultati['sol_migl_NN']= dizionario_sol_migliore_NN
                                elif scelta_meta_euristica == 2:
                                    dizionario_risultati['sol_migl_NN']= {}
                                    dizionario_risultati['sol_migl_C']= dizionario_sol_migliore_C
                                else:
                                    dizionario_risultati['sol_migl_NN']= dizionario_sol_migliore_NN
                                    dizionario_risultati['sol_migl_C']= dizionario_sol_migliore_C
                                
                                salva_risultati('Istanze', dizionario_risultati, dizionario_citta, dizionario_stazioni, G, Max_Axis, k)

                

            print("\n----------- Fine Simulated Annealing -----------")
            print("------------------------------------ Fine Esecuzione Meta-Euristiche ------------------------------------")
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

            print("------------------------------------ Menu Stampe ----------------------------------------------- ") 
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
            print("------------------------------------ Simulated Annealing ------------------------------------")

            processazione_soluzione= 1
            # processazione_soluzione permette di svolgere il SA in differenti modi sulla stessa soluzione
            while processazione_soluzione != 0: 
                print("Scegliere il tipo di esecuzione del SA: ")
                print("\n1) Manuale")
                print("\n2)Da File Config (Testing)")
                scelta_esecuzione= int(input("Scelta"))

                while scelta_esecuzione != 1 and scelta_esecuzione!= 2:
                    print("scelta non valida, riprovare...")
                    print("\nScegliere il tipo di esecuzione del SA: ")
                    print("\n1) Automatica (Testing, lettura dei parametri da file di config)")
                    print("\n2) Manuale")
                    scelta_esecuzione= int(input("Scelta"))

                if scelta_esecuzione == 1: # Esecuzione Automatica
                    config_file= open("config_file.txt", 'r')
                    # Temperature, decreaseT, Tfrozen, numero_iterazioni, n_esecuzioni
                    i= 0
                    n_esecuzione= 0
                    dizionario_config={}
                    dizionario={}
                    for line in config_file:
                        print("line: " + str(line))
                        if line != '\n' and '%' not in line:
                            i += 1
                            if i == 1:
                                n_esecuzione += 1
                                scelta_soluzione= int(line)
                            elif i == 2:
                                numero_iterazioni= int(line)
                                dizionario['numero_iterazioni']= numero_iterazioni
                            elif i == 3:
                                Temperature= int(line)
                                dizionario['Temperature']= Temperature
                            elif i == 4:
                                Tfrozen= int(line)
                                dizionario['Tfrozen']= Tfrozen
                            elif i == 5:
                                n_esecuzioni= int(line)
                                dizionario['n_esecuzioni']= n_esecuzioni
                            elif i == 6:
                                
                                decreaseT= float(line)
                                dizionario['decreaseT']= decreaseT
                                dizionario_config[n_esecuzione]= dizionario
                                dizionario={} 
                                i= 0
                        config_file.close()

                elif scelta_esecuzione == 2:  # Esecuzione Manuale
                    
                    # Impostazione parametri di Default
                    numero_iterazioni= math.factorial(N_CITIES-1)//500
                    Temperature=  N_CITIES*100
                    decreaseT= 0,90
                    Tfrozen= 10
                    n_esecuzioni= 5
                    
                    print("\n----------------------Parametri di Default:----------------------")
                    print("Temperature: " + str(Temperature))
                    print("Fattore di decrescita: " + str(decreaseT))
                    print("Tfrozen: " + str(Tfrozen))
                    print("Numero Iterazioni: " + str(numero_iterazioni))
                    print("Numero di esecuzioni dell'algoritmo: " + str(n_esecuzioni))
                    print("\n-----------------------------------------------------------------")

                    print("\n\nScelta letture parametri:")
                    print("\n1) Uso dei parametri di default")
                    print("\n2) Inserimento manuale parametri")
                    scelta_param= int(input("Scelta: "))
                    while scelta_param != 1 and scelta_param != 2:
                        print("\n\nscelta non valida, riprovare..")
                        print("\n\nMenu selezione metodologia scelta parametri:")
                        print("\n1) Uso dei parametri di default")
                        print("\n2) Inserimento manuale parametri")
                        scelta_param= int(input("Scelta: "))

                    if scelta_param == 2:
                        numero_iterazioni= int(input("\nInserire il numero di iterazioni da effettuare: "))
                        Temperature= int(input("\nInserire la temperatura iniziale desiderata: "))
                        Tfrozen= int(input("\nInserire il valore di TFrozen: "))
                        n_esecuzioni= int(input("\nInserire il numero di volte che si vuole eseguire l'algoritmo: "))
                        decreaseT= float(input("\nInserire il fattore di diminuzione della temperatura (valore compreso tra 0 e 1): "))


                    print("\nScegliere quale soluzione processare tramite Simulated Annealing: ")
                    print("-1 Nearest Neighbour Solution")
                    print("-2 Christofides Solution")
                    print("-3 Entrambe le soluzioni")
                    print("-0 Exit")
                    scelta_soluzione= int(input("Scelta: "))

                    while scelta_soluzione not in range(0,4):
                        print("\nscelta non valida, riprovare...")
                        print("\nScegliere quale soluzione processare tramite Simulated Annealing: ")
                        print("-1 Nearest Neighbour Solution")
                        print("-2 Christofides Solution")
                        print("-3 Entrambe le soluzioni")
                        print("-0 Exit")
                        scelta_soluzione= int(input("Scelta: "))

                
                
                # Inizializzo dizionari dei risultati del SA
                dizionario_SA_NN= {}
                dizionario_SA_C= {}

                if scelta_soluzione == 1:
                    print("\nSimulated Annealing con soluzione Nearest Neighbour")
                    esecuzione= 0
                    start_SA_NN= time.time()

                    while esecuzione < n_esecuzioni:   
                        
                        dizionario_SA_NN_Esecuzione, dizionario_Evoluzione_Soluzioni_NN= simulated_annealing(dizionario_Nearest_Neighbour, dizionario_citta, dizionario_stazioni, G, k, Temperature, decreaseT, Tfrozen, numero_iterazioni, n_esecuzioni)

                        dizionario_SA_NN[esecuzione]= [dizionario_SA_NN_Esecuzione,dizionario_Evoluzione_Soluzioni_NN]

                        esecuzione += 1

                    end_SA_NN= time.time()
                    dizionario_SA_NN['Tempo Esecuzione Totale']= str(end_SA_NN - start_SA_NN)
                        
                elif scelta_soluzione == 2:
                    print("\nSimulated Annealing con soluzione Christofides")
                    esecuzione= 0
                    start_SA_C= time.time()
                    
                    while esecuzione < n_esecuzioni:


                        dizionario_SA_C_Esecuzione, dizionario_Evoluzione_Soluzioni_C= simulated_annealing(dizionario_Christofides, dizionario_citta, dizionario_stazioni, G, k, Temperature, decreaseT, Tfrozen, numero_iterazioni, n_esecuzioni)
                        
                        dizionario_SA_C[esecuzione]= [dizionario_SA_C_Esecuzione,dizionario_Evoluzione_Soluzioni_C]

                        esecuzione += 1
                    
                    end_SA_C= time.time()
                    dizionario_SA_C['Tempo Esecuzione Totale']= str(end_SA_C - start_SA_C)                

                elif scelta_soluzione == 3:
                    print("\nSimulated Annealing con soluzione Nearest Neighbour")
                    esecuzione= 0
                    start_SA_NN= time.time()

                    while esecuzione < n_esecuzioni:
                      
                        dizionario_SA_NN_Esecuzione, dizionario_Evoluzione_Soluzioni_NN= simulated_annealing(dizionario_Nearest_Neighbour, dizionario_citta, dizionario_stazioni, G, k, Temperature, decreaseT, Tfrozen, numero_iterazioni, n_esecuzioni)
                                  
                        dizionario_SA_NN[esecuzione]= [dizionario_SA_NN_Esecuzione,dizionario_Evoluzione_Soluzioni_NN]
                        
                        esecuzione += 1

                    end_SA_NN= time.time()
                    dizionario_SA_NN['Tempo Esecuzione Totale']= str(end_SA_NN - start_SA_NN) 

                    print("\nSimulated Annealing con soluzione Christofides")
                    esecuzione= 0
                    start_SA_C= time.time()

                    while esecuzione < n_esecuzioni:

                        dizionario_SA_C_Esecuzione, dizionario_Evoluzione_Soluzioni_C= simulated_annealing(dizionario_Christofides, dizionario_citta, dizionario_stazioni, G, k, Temperature, decreaseT, Tfrozen, numero_iterazioni, n_esecuzioni)

                        dizionario_SA_C[esecuzione]= [dizionario_SA_C_Esecuzione,dizionario_Evoluzione_Soluzioni_C]

                        esecuzione += 1
                    
                    end_SA_C= time.time()                    
                    dizionario_SA_C['Tempo Esecuzione Totale']= str(end_SA_C - start_SA_C)
                    
                    
                # In dizionario_SA_C (e reciproco NN) ho come chiavi il numero di esecuzione e come valore il dizionario rispettivo della soluzione di quell'esecuzione
                #
                # ----------------------- Salvataggio Risultati Algoritmi------------------------------------
                #
                # Prima di fare il salvataggio devo impacchettare tutti i dati nei relativi dizionari
                #
                # Legenda:
                #
                #   -  indica la chiave
                #   --> indica il dizionario risultante dall'uso di quella chiave
                #
                #
                # ---------------------------------------------------------------------------------------------
                # Come è costituito l'albero del dizionario: dizionario_soluzioni:
                #
                # dizionario_soluzioni: -Costruttive --> dizionario_Costruttive: -NN --> dizionario_Nearest_Neighbour(chiavi elencate sotto)
                #                                                                -C --> dizionario_Christofides (chiavi elencate sotto)              
                #                        
                #                       -Meta Euristiche --> dizionario_MetaEuristiche: -SA --> dizionario_SA:   -NN -->   dizionario_SA_NN  -Esecuzione --> [dizionario_SA_NN_Esecuzione (chiavi elencate sotto), dizionario_Evoluzione_Soluzioni_NN]
                #                                                                                                                            -Tempo Esecuzione Totale               
                #
                #                                                                                                -C  -->   dizionario_SA_C   -Esecuzione --> [dizionario_SA_C_Esecuzione  (chiavi elencate sotto), dizionario_Evoluzione_Soluzioni_C]
                #                                                                                                                            -Tempo Esecuzione Totale
                #
                #                                                                       -ILS --> dizionario_ILS: {}(Per ora vuoto)
                #
                #
                # In Costruttive, NN e C hanno le seguenti chiavi:
                #                       - percorso
                #                       - distanza
                #                       - tempo_tot
                #                       - tempo_ricarica
                #                       - tempo_esec
                #
                #                                       
                # In SA , NN e C sono composti dalle seguenti chiavi:
                #                       - Percorso
                #                       - Distanza Totale
                #                       - Tempo Totale (di percorrenza)
                #                       - Tempo Ricarica
                #                       - Tempo Esecuzione (relativo a quella singola esecuzione)
                #
                # Sia dizionario_Evoluzione_Soluzioni_C che dizionario_Evoluzione_Soluzioni_NN sono relativi ad una esecuzione, al loro interno avremo le seguenti chiavi:
                #
                #   - Soluzione corrente (precedente)
                #   - Costo soluzione corrente
                #   - Soluzione migliore (che è quella che viene trovata nell'iterazione corrente nella corrente temperatura)
                #   - Costo soluzione precedente
                #   - Temperatura
                #   - Iterazione
                #
                # ---------------------------------------------------------------------------------------------
                #   
                # dizionario_dati: -Dati --> dizionario_istanza:   - Lunghezza Assi
                #                                                  - Stazioni Ricarica --> dizionario_stazioni
                #                                                  - Citta             --> dizionario_citta
                #                                                  - Dizionario Distanze
		        #						                           - Autonomia
                #                   
                #                  - SA --> dizionario_parametri_SA: - NCitta
                #                                                    - Iterazioni
                #                                                    - Temperatura
                #                                                    - Tfrozen
                #                                                    - Fattore Decrescita
		        #                
		        #                  - ILS --> dizionario_param_ILS: {} ( per ora ancora vuoto )

                # Incapsulamento dati
                dizionario_soluzioni= {}

                # Dizionario Soluzioni 
                
                # Costruttive
                dizionario_Costruttive= {}
                dizionario_Costruttive['NN']= dizionario_Nearest_Neighbour
                dizionario_Costruttive['C']= dizionario_Christofides
                
                dizionario_soluzioni['Costruttive']=dizionario_Costruttive

                # Meta Euristiche
                dizionario_MetaEuristiche={}
                dizionario_SA= {}
                dizionario_ILS= {}

                # Simulated Annealing

                dizionario_SA['NN']= dizionario_SA_NN
                dizionario_SA['C']= dizionario_SA_C

                dizionario_MetaEuristiche['SA']= dizionario_SA

                # Iterative Local Search

                dizionario_MetaEuristiche['ILS']= dizionario_ILS

                dizionario_soluzioni['Meta Euristiche']= dizionario_MetaEuristiche

                # Dizionario Dati
                dizionario_dati={}
                
                # Dizionario Istanza
                dizionario_istanza={}
                dizionario_istanza['Lunghezza Assi']= Max_Axis
                dizionario_istanza['Stazioni Ricarica']= dizionario_stazioni
                dizionario_istanza['Citta']= dizionario_citta
                dizionario_istanza['Dizionario Distanze']= G
                dizionario_istanza['Autonomia']= k

                dizionario_dati['Dati']= dizionario_istanza

                # Parametri SA

                dizionario_parametri_SA= {}

                dizionario_parametri_SA['NCitta']= N_CITIES
                dizionario_parametri_SA['Iterazioni']= numero_iterazioni
                dizionario_parametri_SA['Temperatura']= Temperature
                dizionario_parametri_SA['Tfrozen']= Tfrozen
                dizionario_parametri_SA['Fattore Decrescita']= decreaseT

                dizionario_dati['SA']= dizionario_parametri_SA


                # Parametri ILS
                dizionario_parametri_ILS={}
                dizionario_dati['ILS']= dizionario_parametri_ILS

                # ------------------------------- Salvataggio -------------------------------------------------------------
                salva_risultati('Istanze', dizionario_soluzioni, dizionario_dati) 


                print("\nInserire:")
                print("\n1) Se continuare a processare le stesse soluzioni costruttive con Simulated Annealing")
                print("\n0) Se procedere e processare le soluzioni costruttive con Iterative Local Search o terminare il programma")
                processazione_soluzione= int(input("\nScelta: "))
                
                

            print("\n----------- Fine Simulated Annealing -----------")
            print("------------------------------------ Fine Esecuzione Meta-Euristiche ------------------------------------")
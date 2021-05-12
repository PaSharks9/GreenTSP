import math
import time
import PlotGenerator as plt
from SimulatedAnnealing import simulated_annealing
from InstanceHandler import generateInstance, manualInstance, leggi_istanza, salva_risultati
from ConstructiveEuristic import NearestNeighbour, Christofides_Algorithm, create_distance_dict
from Cliente import euclidean_distance
from IterativeLocalSearch import iterative_local_search


def stampa_soluzioni(dizionario, nome_algoritmo):
        if "Christofides" in nome_algoritmo:
            nome_algoritmo= " Algoritmo Costruttivo non Greedy " + str(nome_algoritmo)
        elif "Nearest-Neighbour":
            nome_algoritmo= " Algoritmo Costruttivo Greedy " + str(nome_algoritmo)

        chiavi = list(dizionario.keys())

        print("\n------" + str(nome_algoritmo) + " ------")

        for key in chiavi: 
            print("\n" + str(key) + ": " + str(dizionario[key]))

        print("\n" + "-" * 50)





if __name__ == "__main__":
    # Istanziazione dizionari dei risultati

    # ------- Istanziazione dizionari dati parametri ------------
    # Dizionario Dati
    dizionario_dati={}
    dizionario_istanza={}

    # Parametri
    dizionario_dati['SA']= {}
    dizionario_dati['ILS']= {}


    # ------- Istanziazione dizionari soluzioni ------------
    # Dizionario Soluzioni
    dizionario_soluzioni= {}
    
    # Soluzioni Costruttive
    dizionario_Costruttive= {}

    # Meta Euristiche
    dizionario_MetaEuristiche={}

    # Inizializzo, c'è caso che possa essere scelta l'esecuzione di una delle due meta euristiche e quindi vadano salvati solo alcuni dati 
    dizionario_MetaEuristiche['SA']= {}
    dizionario_MetaEuristiche['ILS']= {}



    # --------------------------------- Start -------------------------------------------------
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
        
        # ---------------------------------- Incapsulo dati per salvataggio -----------------------------------------
        # Immagazzino i dati ottenuti
        # Incapsulamento dati
        # Parametri Istanza

        dizionario_istanza['Lunghezza Assi']= Max_Axis
        dizionario_istanza['Stazioni Ricarica']= dizionario_stazioni
        dizionario_istanza['Citta']= dizionario_citta
        dizionario_istanza['Dizionario Distanze']= G
        dizionario_istanza['Autonomia']= k

        dizionario_dati['Dati']= dizionario_istanza

        # ------------------------------------------------------------------------------------------------------------ 

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


            # ---------------------------------- Incapsulo dati per salvataggio -----------------------------------------
            # Immagazzino i dati ottenuti delle Costruttive
            # Incapsulamento dati
            
            dizionario_Costruttive['NN']= dizionario_Nearest_Neighbour
            dizionario_Costruttive['C']= dizionario_Christofides
            
            dizionario_soluzioni['Costruttive']=dizionario_Costruttive

            # ------------------------------------------------------------------------------------------------------------ 

            print("------------------------------------ Menu Stampe ----------------------------------------------- ") 
            scelta_stampe= 1
            while scelta_stampe != 0:
                print("\n1- Stampa Christofides")
                print("2- Stampa Nearest Neighbour")
                print("0- Prosegui verso le Meta-Euristiche")

                scelta_stampe= int(input("\nScelta: "))

            # Stampo i risultati

                if scelta_stampe == 1:
                    stampa_soluzioni(dizionario_Christofides, 'Christofides')
                elif scelta_stampe == 2:
                    stampa_soluzioni(dizionario_Nearest_Neighbour, 'Nearest-Neighbour')
                elif scelta_stampe == 0:
                    break


            print("\n------------------------------------ Esecuzione Meta-Euristiche ------------------------------------")
            scelta_meta_euristiche= 1
            while scelta_meta_euristiche != 0:
                print("\nScegliere la meta-euristiche che si vuole attuare:\n1) Simulated Annealing (SA) \n2) Iterative Local Search (ILS) \n0) Exit")
                scelta_meta_euristiche= int(input("\nScelta: "))


                if scelta_meta_euristiche == 1:
                    print("------------------------------------ Simulated Annealing ---------------------------------------------")
 
                    print("Scegliere il tipo di esecuzione del SA: ")
                    print("\n1) Manuale")
                    print("\n2) Da File Config (Testing, lettura dei parametri da file di config)")
                    scelta_esecuzione= int(input("\nScelta: "))

                    while scelta_esecuzione != 1 and scelta_esecuzione!= 2:
                        print("scelta non valida, riprovare...")
                        print("\nScegliere il tipo di esecuzione del SA: ")
                        print("\n1) Manuale ")
                        print("\n2) Automatica (Testing, lettura dei parametri da file di config)")
                        scelta_esecuzione= int(input("\nScelta: "))

                    if scelta_esecuzione == 1: # Esecuzione Manuale

                        # Impostazione parametri di Default
                        # numero_iterazioni= math.factorial(N_CITIES-1)
                        #numero_iterazioni= math.factorial(N_Cities)
                        numero_iterazioni= 2000
                        Temperature=  1000
                        decreaseT= 0.8
                        Tfrozen= 1
                        n_esecuzioni= 3
                        
                        print("\n----------------------Parametri di Default:----------------------")
                        print("Temperature: " + str(Temperature))
                        print("Fattore di decrescita: " + str(decreaseT))
                        print("Tfrozen: " + str(Tfrozen))
                        print("Numero Iterazioni: " + str(numero_iterazioni))
                        print("Numero di esecuzioni dell'algoritmo: " + str(n_esecuzioni))
                        print("\n-----------------------------------------------------------------")

                        print("\n\nScelta letture parametri:")
                        print("\n1) Inserimento manuale parametri")
                        print("\n2) Uso dei parametri di default")
                        scelta_param= int(input("\nScelta: "))

                        while scelta_param != 1 and scelta_param != 2:
                            print("\n\nscelta non valida, riprovare..")
                            print("\n\nMenu selezione metodologia scelta parametri:")
                            print("\n1) Uso dei parametri di default")
                            print("\n2) Inserimento manuale parametri")
                            scelta_param= int(input("\nScelta: "))

                        if scelta_param == 1:
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
                        scelta_soluzione= int(input("\nScelta: "))

                        while scelta_soluzione not in range(0,4):
                            print("\nscelta non valida, riprovare...")
                            print("\nScegliere quale soluzione processare tramite Simulated Annealing: ")
                            print("-1 Nearest Neighbour Solution")
                            print("-2 Christofides Solution")
                            print("-3 Entrambe le soluzioni")
                            print("-0 Exit")
                            scelta_soluzione= int(input("\nScelta: "))

                    elif scelta_esecuzione == 2:  # Esecuzione Automatica

                        config_file= open("config_file.txt", 'r')
                        # Temperature, decreaseT, Tfrozen, numero_iterazioni, n_esecuzioni
                        i= 0
                        n_esecuzione= 0
                        dizionario_config={}
                        dizionario={}
                        for line in config_file:
                            #print("line: " + str(line))
                            if line != '\n' and '%' not in line:
                                i += 1
                                if i == 1:
                                    n_esecuzione += 1
                                    dizionario['scelta_soluzione']= int(line)
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

                    
                    if scelta_esecuzione == 2:  # Se l'esecuzione è automatica devo capire quante chiamate devo fare
                        n_chiamate= len(list(dizionario_config.keys()))
                        n_chiamate += 1
                        print("n_chiamate: " + str(n_chiamate))
                    else: 
                        # Se l'esecuzione non è automatica c'è solo una chiamata
                        n_chiamate= 2   
                    

                    # Dizionario Incapsulo Parametri SA
                    dizionario_parametri_SA= {}
                    
                    # Dizionario Incapsulamento dati SA
                    dizionario_SA= {}

                    chiamata= 1
                    while chiamata < n_chiamate:    

                        # Inizializzo gli eventuali parametri, se esecuzione automatica
                        if scelta_esecuzione == 2:
                            dizionario_chiamata= dizionario_config[chiamata]

                            scelta_soluzione= dizionario_chiamata['scelta_soluzione']
                            numero_iterazioni= dizionario_chiamata['numero_iterazioni']
                            Temperature= dizionario_chiamata['Temperature']
                            Tfrozen= dizionario_chiamata['Tfrozen']
                            n_esecuzioni= dizionario_chiamata['n_esecuzioni']
                            decreaseT= dizionario_chiamata['decreaseT']

                        
                        dizionario_param_SA= {}

                        # ad ogni chiamata avrò parametri diversi, e con chiamata s'intende esecuzione diversa dovuto al config_file
                        dizionario_parametri_SA[chiamata]= dizionario_param_SA

                        dizionario_param_SA['NCitta']= N_CITIES
                        dizionario_param_SA['Iterazioni']= numero_iterazioni
                        dizionario_param_SA['Temperatura']= Temperature
                        dizionario_param_SA['Tfrozen']= Tfrozen
                        dizionario_param_SA['Fattore Decrescita']= decreaseT

                        dizionario_dati['SA']= dizionario_parametri_SA


                        # Inizializzo dizionari dei risultati del SA
                        dizionario_SA_NN= {}
                        dizionario_SA_C= {}

                        if scelta_soluzione == 1:
                            print("\nSimulated Annealing con soluzione Nearest Neighbour")
                            esecuzione= 0
                            start_SA_NN= time.time()

                            while esecuzione < n_esecuzioni:   
                                
                                dizionario_SA_NN_Esecuzione, dizionario_Evoluzione_Soluzioni_NN= simulated_annealing(dizionario_Nearest_Neighbour, dizionario_citta, dizionario_stazioni, G, k, Temperature, decreaseT, Tfrozen, numero_iterazioni)

                                dizionario_SA_NN[esecuzione]= [dizionario_SA_NN_Esecuzione,dizionario_Evoluzione_Soluzioni_NN]

                                esecuzione += 1

                            end_SA_NN= time.time()
                            dizionario_SA_NN['Tempo Esecuzione Totale']= str(end_SA_NN - start_SA_NN)
                                
                        elif scelta_soluzione == 2:
                            print("\nSimulated Annealing con soluzione Christofides")
                            esecuzione= 0
                            start_SA_C= time.time()
                            
                            while esecuzione < n_esecuzioni:


                                dizionario_SA_C_Esecuzione, dizionario_Evoluzione_Soluzioni_C= simulated_annealing(dizionario_Christofides, dizionario_citta, dizionario_stazioni, G, k, Temperature, decreaseT, Tfrozen, numero_iterazioni)
                                
                                dizionario_SA_C[esecuzione]= [dizionario_SA_C_Esecuzione,dizionario_Evoluzione_Soluzioni_C]

                                esecuzione += 1
                            
                            end_SA_C= time.time()
                            dizionario_SA_C['Tempo Esecuzione Totale']= str(end_SA_C - start_SA_C)                

                        elif scelta_soluzione == 3:
                            print("\nSimulated Annealing con soluzione Nearest Neighbour")
                            esecuzione= 0
                            start_SA_NN= time.time()

                            while esecuzione < n_esecuzioni:
                            
                                dizionario_SA_NN_Esecuzione, dizionario_Evoluzione_Soluzioni_NN= simulated_annealing(dizionario_Nearest_Neighbour, dizionario_citta, dizionario_stazioni, G, k, Temperature, decreaseT, Tfrozen, numero_iterazioni)
                                        
                                dizionario_SA_NN[esecuzione]= [dizionario_SA_NN_Esecuzione,dizionario_Evoluzione_Soluzioni_NN]
                                
                                esecuzione += 1

                            end_SA_NN= time.time()
                            dizionario_SA_NN['Tempo Esecuzione Totale']= str(end_SA_NN - start_SA_NN) 

                            print("\nSimulated Annealing con soluzione Christofides")
                            esecuzione= 0
                            start_SA_C= time.time()

                            while esecuzione < n_esecuzioni:

                                dizionario_SA_C_Esecuzione, dizionario_Evoluzione_Soluzioni_C= simulated_annealing(dizionario_Christofides, dizionario_citta, dizionario_stazioni, G, k, Temperature, decreaseT, Tfrozen, numero_iterazioni)

                                dizionario_SA_C[esecuzione]= [dizionario_SA_C_Esecuzione,dizionario_Evoluzione_Soluzioni_C]

                                esecuzione += 1
                            
                            end_SA_C= time.time()                    
                            dizionario_SA_C['Tempo Esecuzione Totale']= str(end_SA_C - start_SA_C)
                            
                        # ---------------------------------- Incapsulo dati per salvataggio -----------------------------------------
                                
                        # Simulated Annealing

                        dizionario_SA_Chiamata={}

                        
                        dizionario_SA_Chiamata['NN']= dizionario_SA_NN
                        dizionario_SA_Chiamata['C']= dizionario_SA_C


                        dizionario_SA[chiamata]= dizionario_SA_Chiamata

                        dizionario_MetaEuristiche['SA']= dizionario_SA

                        dizionario_soluzioni['Meta Euristiche']= dizionario_MetaEuristiche
                        # ------------------------------------------------------------------------------------------------------------   
                        # ------------------------------- Salvataggio ----------------------------------------------------------------
                        # Ad ogni chiamata del SA salvo i dati
                        #salva_risultati(dizionario_soluzioni, dizionario_dati) 

                        # Ora dovrei fare la chiamata all'ILS

                        chiamata += 1

                    """print("dizionario_parametri_SA: " + str(dizionario_parametri_SA.keys()))
                    print("dizionario_SA: " + str(dizionario_SA.keys()))"""
                        
                    scelta_salvataggio= 1
                    while scelta_salvataggio != 'y' and scelta_salvataggio != 'n':
                        scelta_salvataggio= str(input("\n\nSi desidera salvare i risultati ottenuti?\nDigitare y/n: "))

                    if scelta_salvataggio == 'y':
                        salva_risultati(dizionario_soluzioni, dizionario_dati)
                    print("\n------------------------------------ Fine Simulated Annealing ------------------------------------------")

                elif scelta_meta_euristiche == 2:

                    print("\n\n------------------------------------ Iterative Local Search --------------------------------------------")

                    n_iterazioni= 1000
                    error_tolerance= 3

                    print("\nParametri ILS: ")
                    print("\nn_iterazioni: " + str(n_iterazioni))
                    print("\nError tolerance: " + str(error_tolerance))

                    print("\nInserimento parametri Iterative Local Search:\n1)Parametri di Default\n2)Inserimento manuale")
                    scelta_iterazioni_ILS = int(input("\nScelta: "))
                    while scelta_iterazioni_ILS != 1 and scelta_iterazioni_ILS != 2:
                        print("\nErrore nella scelta, il numero inserito non rientra tra le scelte, riprovare..")
                        print("\nInserimento parametri Iterative Local Search:\n1)Parametri di Default\n2)Inserimento manuale")
                        scelta_iterazioni_ILS = int(input("\nScelta: "))    

                    if scelta_iterazioni_ILS == 2:
                        n_iterazioni= int(input("Inserire il numero di Iterazioni da eseguire: "))
                        error_tolerance= int(input("Inserire la tolleranza agli errori (numero da 0 a 10): "))
                        while error_tolerance > 10 or error_tolerance < 0:
                            print("\n L'error tolerance deve essere compreso tra 0 e 10")
                            error_tolerance= int(input("Inserire la tolleranza agli errori (numero da 0 a 10): "))

                    processazione_soluzione= 1
                    while processazione_soluzione != 0:
                        print("\n\nProcessare:")
                        print("\n1- Soluzione Christofides")
                        print("\n2- Soluzione NearestNeighbour")
                        print("\n3- Entrambe le soluzioni")
                        print("\n0- Exit")
                        
                        processazione_soluzione= int(input("\nInserire Scelta: "))

                        if processazione_soluzione == 1:
                            tour_christofides= dizionario_Christofides['percorso']
                            tempo_tot_christofides= dizionario_Christofides['tempo_tot']
                            
                            start_time= time.time()
                            dizionario_ILS_C= iterative_local_search(tour_christofides, tempo_tot_christofides, G, k, dizionario_citta, dizionario_stazioni, n_iterazioni, error_tolerance)
                            end_time= time.time()

                            dizionario_ILS_C['execution_time']= int(end_time - start_time)

                            print("\nTour_ILS_C: " + str(dizionario_ILS_C['percorso']))
                            print("tempo_tot_C: " + str(dizionario_ILS_C['tempo_tot']))
                            print("tempo di esecuzione: " + str(int(end_time - start_time)))

                        elif processazione_soluzione == 2:
                            tour_NN= dizionario_Nearest_Neighbour['percorso']
                            tempo_tot_NN= dizionario_Nearest_Neighbour['tempo_tot']

                            start_time= time.time()
                            dizionario_ILS_NN= iterative_local_search(tour_NN, tempo_tot_NN, G, k, dizionario_citta, dizionario_stazioni, n_iterazioni, error_tolerance)
                            end_time= time.time()

                            dizionario_ILS_NN['execution_time']= int(end_time - start_time)

                            print("\nTour_ILS_NN: " + str(dizionario_ILS_NN['percorso']))
                            print("tempo_tot_NN: " + str(dizionario_ILS_NN['tempo_tot']))
                            print("tempo di esecuzione: " + str(int(end_time - start_time)))

                        elif processazione_soluzione == 3:
                            tour_christofides= dizionario_Christofides['percorso']
                            tempo_tot_christofides= dizionario_Christofides['tempo_tot']

                            tour_NN= dizionario_Nearest_Neighbour['percorso']
                            tempo_tot_NN= dizionario_Nearest_Neighbour['tempo_tot']

                            start_time_C= time.time()
                            dizionario_ILS_C= iterative_local_search(tour_christofides, tempo_tot_christofides, G, k, dizionario_citta, dizionario_stazioni, n_iterazioni, error_tolerance)
                            start_time_NN= time.time()
                            dizionario_ILS_NN= iterative_local_search(tour_NN, tempo_tot_NN, G, k, dizionario_citta, dizionario_stazioni, n_iterazioni, error_tolerance)
                            end_time_NN= time.time()

                            dizionario_ILS_C['execution_time']= int(start_time_NN - start_time_C)
                            dizionario_ILS_NN['execution_time']= int(end_time_NN - start_time_NN)


                            print("\nTour_ILS_C: " + str(dizionario_ILS_C['percorso']))
                            print("tempo_tot_C: " + str(dizionario_ILS_C['tempo_tot']))
                            print("tempo di esecuzione: " + str(int(start_time_NN - start_time_C)))

                            print("\nTour_ILS_NN: " + str(dizionario_ILS_NN['percorso']))
                            print("tempo_tot_NN: " + str(dizionario_ILS_NN['tempo_tot']))
                            print("tempo di esecuzione: " + str(int(end_time_NN - start_time_C)))
                            



                    # Parametri ILS
                    dizionario_dati['ILS']= {}
                    dizionario_parametri_ILS= {}
                    dizionario_dati['ILS']= dizionario_parametri_ILS

                    dizionario_parametri_ILS['n_iterazioni']= n_iterazioni
                    dizionario_parametri_ILS['n_citta']= N_CITIES
                    dizionario_parametri_ILS['error_tolerance']= error_tolerance
                    # Iterative Local Search

                    dizionario_MetaEuristiche['ILS']= {}
                    dizionario_ILS={}
                    dizionario_ILS['C']= {}
                    dizionario_ILS['NN']= {}

                    
                    dizionario_ILS['C']= dizionario_ILS_C
                    dizionario_ILS['NN']= dizionario_ILS_NN

                    dizionario_MetaEuristiche['ILS']= dizionario_ILS

                    dizionario_soluzioni['Meta Euristiche']= dizionario_MetaEuristiche

                    # Salvo il risultati:
                    scelta_salvataggio= 1
                    while scelta_salvataggio != 'y' and scelta_salvataggio != 'n':
                        scelta_salvataggio= str(input("\n\nSi desidera salvare i risultati ottenuti?\nDigitare y/n: "))

                    if scelta_salvataggio == 'y':
                        salva_risultati(dizionario_soluzioni, dizionario_dati)

                    print("\n------------------------------------ Fine Iterative Local Search ----------------------------------------")
                    print("\n------------------------------------ Fine Esecuzione Meta-Euristiche ------------------------------------")
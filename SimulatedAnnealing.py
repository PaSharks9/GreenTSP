
import random
import time
import math
from Cliente import euclidean_distance,Cliente
from LocalSearch import two_opt
from PlotGenerator import print_2_opt_arc_selected


def soluzione_accettabile(percorso, G, k, dizionario_citta, dizionario_stazioni):
    index= 0
    autonomia= k
    while index < len(percorso) - 1:
        """print("index/percorso: ")
        print(str(index) + "/" + str(len(percorso)))
        print("\nNodo1: " + str(percorso[index]))
        print("Nodo2: " + str(percorso[index + 1]))
        print("\nautonomia: " + str(autonomia))"""
        if 'S' not in str(percorso[index]) and 'S' not in str(percorso[index+1]):
            distanza_da_percorrere= G[percorso[index]][percorso[index+1]]
            #print("distanza_da_percorrere: " + str(distanza_da_percorrere))
            if autonomia - distanza_da_percorrere < 0:
                # Significa che non è una soluzione accettabile
                return False
            else:
                autonomia -= distanza_da_percorrere

        elif 'S' in str(percorso[index]) and 'S' not in str(percorso[index + 1]): # Tratta da una stazione 
            
            # Parto da una stazione, quindi avrò autonomia massima
            autonomia= k
            #print("Autonomia Ricaricata: " + str(autonomia))
            if percorso[index + 1] != 0:
                # Devo solo controllare di avere autonomia sufficiente per arrivare nella citta successiva
                nodo_stazione= int(percorso[index].replace('S',''))
                coordinate_stazione= dizionario_stazioni.get(nodo_stazione)
                #print("coordinate_stazione: " + str(coordinate_stazione))

                nodo_citta= dizionario_citta.get(int(percorso[index + 1]))
                coordinate_citta= nodo_citta.coordinate
                #print("coordinate_citta: " + str(coordinate_citta))

                distanza_da_percorrere= euclidean_distance(coordinate_stazione, coordinate_citta)
                #print("distanza_da_percorrere: " + str(distanza_da_percorrere))
                if autonomia - distanza_da_percorrere < 0:
                    # Significa che non è una soluzione accettabile
                    return False
                else:
                    autonomia -= distanza_da_percorrere

        elif 'S' not in str(percorso[index]) and 'S' in str(percorso[index + 1]): # Tratta da una citta ad una stazione  (TEORICAMENTE QUESTO if non dovrebbe andare in false perchè i due if precedenti controllano se una volta arrivati nella città successiva si ha autonomia a sufficienza per andare in una stazione)
            
            # Considerare caso in cui si parta dal deposito e si vada in una stazione di ricarica (Mossa legale)

            if percorso[index] == 0:
                coordinate_citta= [0,0]
            else:
                nodo_citta= dizionario_citta.get(int(percorso[index]))
                coordinate_citta= nodo_citta.coordinate
            #print("coordinate_citta: " + str(coordinate_citta))

            nodo_stazione= int(percorso[index + 1].replace('S',''))
            coordinate_stazione= dizionario_stazioni.get(nodo_stazione)
            #print("coordinate_stazione: " + str(coordinate_stazione))


            distanza_da_percorrere= euclidean_distance(coordinate_stazione, coordinate_citta)
            #print("distanza_da_percorrere: " + str(distanza_da_percorrere))
            if autonomia - distanza_da_percorrere < 0:
                # Significa che non è una soluzione accettabile
                return False
            else:
                autonomia -= distanza_da_percorrere

        index += 1

    # Se sono arrivato fino a qui significa che tutto è regolare quindi ritorno True

    return True

def calcola_costo(G, k, dizionario_citta, dizionario_stazioni, percorso):
    distanza_percorsa= 0
    autonomia= k
    tempo_tot= 0

    index= 0

    while index < len(percorso) - 1:
        """print("\nindex/percorso: ")
        print(str(index) + "/" + str(len(percorso)))
        print("\nNodo1: " + str(percorso[index]))
        print("Nodo2: " + str(percorso[index + 1]))
        print("\nautonomia: " + str(autonomia))"""
        if 'S' not in str(percorso[index]) and 'S' not in str(percorso[index+1]):  # Significa che è una tratta tra due città e non tra due stazioni o tra una città e stazione
            distanza_percorsa += G[percorso[index]][percorso[index+1]]
            #print("distanza: " + str(G[percorso[index]][percorso[index+1]]))
            autonomia -= G[percorso[index]][percorso[index+1]]
            #print("autonomia futura: " + str(autonomia))
            #print("distanza_percorsa: " + str(distanza_percorsa))
        elif 'S' in str(percorso[index]) and 'S' not in str(percorso[index + 1]): # Tratta da una stazione ad una citta, la distanza percorsa la devo ricavare dai dizionari citta e stazione
            station= percorso[index]
            station= station.replace('S','')
            coordinate_stazione= dizionario_stazioni.get(int(station))

            if percorso[index + 1] == 0:  # caso in cui sia una tratta da stazione a deposito ( ultimo arco del tour )
                coordinate_citta= [0,0]
            
            else:
                citta= dizionario_citta.get(int(percorso[index + 1]))
                coordinate_citta= citta.coordinate

            distanza_percorsa += euclidean_distance(coordinate_stazione, coordinate_citta)
            #print("distanza: " + str(euclidean_distance(coordinate_stazione, coordinate_citta)))
            autonomia -= euclidean_distance(coordinate_stazione, coordinate_citta)
            #print("autonomia futura: " + str(autonomia))
        elif 'S' not in str(percorso[index]) and 'S' in str(percorso[index + 1]): # Tratta da una citta ad una stazione, in questa tratta devo considerare anche il tempo di ricarica dato che il costo è il tempo del tour
            station= percorso[index + 1]
            station= station.replace('S','')
            coordinate_stazione= dizionario_stazioni.get(int(station))

            if percorso[index] == 0:  # caso in cui sia una tratta da deposito a stazione ( primo arco del tour )
                coordinate_citta= [0,0]
            else:
                citta= dizionario_citta.get(int(percorso[index]))
                coordinate_citta= citta.coordinate

            distanza_percorsa += euclidean_distance(coordinate_stazione, coordinate_citta)
            #print("distanza: " + str(euclidean_distance(coordinate_stazione, coordinate_citta)))
            autonomia -= euclidean_distance(coordinate_stazione, coordinate_citta)
            #print("autonomia_futura: "+ str(autonomia))
            #print("distanza_percorsa: " + str(distanza_percorsa))
            # Caso in cui prima di tornare al deposito sono in una stazione, in questo caso la ricarica sarà precisa per tornare al deposito, non carico di più
            if index + 1 == len(percorso) - 2:  # index+1 è l'indice della stazione , len(percorso) - 2 è l'indice della penultima tappa del percorso
                distanza_stazione_deposito= euclidean_distance(coordinate_stazione, [0,0])
                delta_ricarica= distanza_stazione_deposito - autonomia
            else:
                delta_ricarica=  k - autonomia
            
            #print("delta_ricarica: " + str(delta_ricarica))
            tempo_tot +=  0.25*delta_ricarica
            autonomia= k

            
        elif 'S' in str(percorso[index]) and 'S' in str(percorso[index + 1]): # Caso in cui da una stazione di rifornimento si vada all'altra         
            station1= percorso[index]
            station1= station1.replace('S','')

            coordinate_stazione1= dizionario_stazioni.get(int(station1))

            station2= percorso[index + 1]
            
            station2= station2.replace('S','')

            coordinate_stazione2= dizionario_stazioni.get(int(station2))
            

            distanza_percorsa += euclidean_distance(coordinate_stazione1, coordinate_stazione2)

            autonomia -= euclidean_distance(coordinate_stazione1, coordinate_stazione2)
            
            # Essendo partiti ed arrivati in una stazione si ricarica
            delta_ricarica=  k - autonomia

            tempo_tot +=  0.25*delta_ricarica
            autonomia= k

        index += 1
    
    tempo_tot += distanza_percorsa

    return tempo_tot, distanza_percorsa


def simulated_annealing(dizionario_soluzione, dizionario_citta, dizionario_stazioni, G, k, Temperatura, decreaseT,Tfrozen, numero_iterazioni, n_esecuzioni):
    dizionario_migliori={}
    
    dizionario_SA= {}

    esec= 0
    while esec < n_esecuzioni:
        # Inizializzo i dati

        dizionario_sol_migliori= {}
        start_esecuzione= time.time()

        Temperature= Temperatura
        soluzione_iniziale= dizionario_soluzione.get('percorso')
        distanza_soluzione_iniziale= dizionario_soluzione.get('distanza')
        tempo_totale_sol_iniziale= dizionario_soluzione.get('tempo_tot')


        soluzione_precedente= soluzione_iniziale
        soluzione_corrente= soluzione_iniziale
        soluzione_migliore= soluzione_corrente


        costo_soluzione_precedente= tempo_totale_sol_iniziale
        costo_soluzione_corrente= tempo_totale_sol_iniziale
        costo_soluzione_migliore= costo_soluzione_corrente

        distanza_percorsa_soluzione_corrente= distanza_soluzione_iniziale
        distanza_percorsa_migliore= distanza_soluzione_iniziale
        distanza_percorsa_precedente= distanza_soluzione_iniziale


        iterazione_fallimento= 0
        start_time= time.time()
        while Temperature > Tfrozen:

            j= 0
            check_time= time.time() - start_time

            if iterazione_fallimento == numero_iterazioni //2 and check_time < 1200:
                # Ripristino la temperatura allo stato precedente
                Temperature = Temperature * decreaseT

            iteration= 0
            iterazione_fallimento= 0
            # Cercare un numero di iterazioni per considerarsi in equilibrio
            while iteration < numero_iterazioni:  

                # ricerca random soluzione nell'intorno 2-opt
                archi_scelti, new_solution= two_opt(soluzione_corrente, dizionario_citta, dizionario_stazioni)
                costo_new_solution, distanza_percorsa_new_sol= calcola_costo(G,k,dizionario_citta,dizionario_stazioni, new_solution)  # I costi sono dati dal tempo totale speso per il percorso( compreso il tempo di ricarica )

                delta_E= costo_new_solution - costo_soluzione_corrente
                print("delta_E: "+ str(delta_E))

                if delta_E <= 0:

                    soluzione_precedente= soluzione_corrente
                    costo_soluzione_precedente= costo_soluzione_corrente
                    distanza_percorsa_precedente= distanza_percorsa_soluzione_corrente

                    soluzione_corrente= new_solution
                    costo_soluzione_corrente= costo_new_solution
                    distanza_percorsa_soluzione_corrente= distanza_percorsa_new_sol


                    # La soluzine migliore deve essere accettabile perchè è quella restituita

                    risultato_correttezza= soluzione_accettabile(soluzione_corrente, G, k, dizionario_citta, dizionario_stazioni)
                    
                    if risultato_correttezza and costo_soluzione_corrente <= costo_soluzione_migliore :
                        print("iteration:" + str(iteration))
                        print("Temperature: " + str(Temperature))
                        print("soluzione_corrente: " + str(soluzione_corrente))
                        print("soluzione_migliore: " + str(soluzione_migliore))
                        print("Archi_scelti: " + str(archi_scelti))
                        time.sleep(10)
                        j +=1
                        dizionario_sol_migliori[j]= [soluzione_corrente,Temperature,iteration,costo_soluzione_corrente,soluzione_migliore,archi_scelti]

                        soluzione_migliore= new_solution
                        costo_soluzione_migliore= costo_new_solution
                        distanza_percorsa_migliore= distanza_percorsa_new_sol

                else:
                    random_choice= round(random.random(),2)
                    
                    print("random_choice: "+ str(random_choice))
                    exponential_value= math.exp(-delta_E/Temperature)
                    print("exponential_value: " + str(exponential_value))

                    if random_choice < exponential_value:

                        soluzione_precedente= soluzione_corrente
                        costo_soluzione_precedente= costo_soluzione_corrente
                        distanza_percorsa_precedente= distanza_percorsa_soluzione_corrente

                        soluzione_corrente= new_solution
                        costo_soluzione_corrente= costo_new_solution
                        distanza_percorsa_soluzione_corrente= distanza_percorsa_new_sol
                        

                # Per aver raggiunto l'equilibrio la soluzione deve essere ammissibile, quindi devo fare un controllo sull'ammissibilità della soluzione, altrimenti continuo a rimanere nel ciclo
                if iteration == numero_iterazioni - 1:
                    # Se siamo nell'ultima iterazione devo controllare che la soluzione sia accettabile 
                    if soluzione_accettabile(soluzione_corrente, G, k, dizionario_citta, dizionario_stazioni):
                        # Se la soluzione è accettabile, aumento iteration e usciro dal ciclo delle iterazioni in quanto siamo in una situazione stabile
                        iteration += 1
                    else:
                        if iterazione_fallimento == numero_iterazioni // 2:
                            # Se non è riuscito a rientrare in una situazione di stabilità torno nello stato stabile precedente e rifaccio la computazione, sperando che la componente casuale mi faccia uscire dal loop
                            soluzione_corrente= soluzione_precedente
                            costo_soluzione_corrente= costo_soluzione_precedente
                            distanza_percorsa_soluzione_corrente= distanza_percorsa_precedente
                            break   
                        
                        print("soluzione non accettabile, continuo a iterare anche se dovrei abbassare la T")
                        iterazione_fallimento += 1
                    # Se invece la soluzione corrente non è accettabile alla fine delle n iterazioni, non siamo in una situazione di equilibrio (in quanto la soluzione non è accettabile) e quindi non aumento il contatore e continuo a iterare fino a quando non trovo una soluzione accettabile
                else:
                    iteration += 1
            
            # Finito While
            Temperature= Temperature * decreaseT
            print("\n ==================================================================")    
        fine_esecuzione= time.time()
        dizionario_Esecuzione= {}


        dizionario_Esecuzione['soluzione_migliore']= soluzione_migliore
        dizionario_Esecuzione['costo_sol_migliore']= costo_soluzione_migliore
        dizionario_Esecuzione['distanza_percorsa_migliore']= distanza_percorsa_migliore
        dizionario_Esecuzione['tempo_esecuzione']= fine_esecuzione - start_esecuzione 
        dizionario_SA[esec]= dizionario_Esecuzione

        dizionario_migliori[esec]= dizionario_sol_migliori

        esec += 1

    return dizionario_SA, dizionario_migliori




if __name__ == "__main__":

    k= 56
    percorso=  [0, 3, 6, 9, 7, 5, '1S', 8, 1, 4, 2, '2S', 0]
    G= {0: {1: 17, 2: 16, 3: 5, 4: 21, 5: 17, 6: 19, 7: 18, 8: 23, 9: 22},
        1: {0: 17, 2: 14, 3: 22, 4: 5, 5: 20, 6: 34, 7: 27, 8: 21, 9: 37},
        2: {0: 16, 1: 14, 3: 19, 4: 13, 5: 29, 6: 34, 7: 33, 8: 32, 9: 38},
        3: {0: 5, 1: 22, 2: 19, 4: 25, 5: 19, 6: 15, 7: 18, 8: 26, 9: 19},
        4: {0: 21, 1: 5, 2: 13, 3: 25, 5: 25, 6: 39, 7: 32, 8: 25, 9: 42},
        5: {0: 17, 1: 20, 2: 29, 3: 19, 4: 25, 6: 22, 7: 9, 8: 7, 9: 23},
        6: {0: 19, 1: 34, 2: 34, 3: 15, 4: 39, 5: 22, 7: 13, 8: 29, 9: 4},
        7: {0: 18, 1: 27, 2: 33, 3: 18, 4: 32, 5: 9, 6: 13, 8: 16, 9: 14},
        8: {0: 23, 1: 21, 2: 32, 3: 26, 4: 25, 5: 7, 6: 29, 7: 16, 9: 30},
        9: {0: 22, 1: 37, 2: 38, 3: 19, 4: 42, 5: 23, 6: 4, 7: 14, 8: 30}
    }
    dizionario_stazioni = {1: [10, 10], 2: [10, -10], 3: [-10, -10], 4: [-10, 10]}
    lista_citta=[
    [17, -3],
    [8, -14],
    [-5, 0],
    [20, -7],
    [8, 15],
    [-14, 13],
    [-1, 18],
    [15, 18],
    [-15, 17]
    ]

    i = 1
    dizionario_citta= {}
    for element in lista_citta: 
        cliente= Cliente(element[0],element[1],dizionario_stazioni,i)
        dizionario_citta[i]= cliente
        i += 1

    resAccettabilita= soluzione_accettabile(percorso, G, k, dizionario_citta, dizionario_stazioni)
    costo= calcola_costo(G, k, dizionario_citta, dizionario_stazioni, percorso)
    print("res: " + str(resAccettabilita))
    print("costo: " + str(costo))

import random
import time
import math
from Cliente import euclidean_distance,Cliente, soluzione_accettabile, calcola_costo
from LocalSearch import two_opt
from PlotGenerator import print_2_opt_arc_selected

def simulated_annealing(dizionario_soluzione, dizionario_citta, dizionario_stazioni, G, k, Temperatura, decreaseT,Tfrozen, numero_iterazioni):

    # Inizializzo i dati di riferimento

    dizionario_sol_migliori= {}

    # Dati soluzione iniziale
    soluzione_iniziale= dizionario_soluzione.get('percorso')
    distanza_soluzione_iniziale= dizionario_soluzione.get('distanza')
    tempo_totale_sol_iniziale= dizionario_soluzione.get('tempo_tot')

    # Inizializzo le 3 soluzioni di riferimento
    # soluzione_precedente= soluzione_iniziale
    soluzione_corrente= soluzione_iniziale
    soluzione_migliore= soluzione_corrente

    # Inizializzo i 3 costi di riferimento
    # costo_soluzione_precedente= tempo_totale_sol_iniziale
    costo_soluzione_corrente= tempo_totale_sol_iniziale
    costo_soluzione_migliore= costo_soluzione_corrente

    # Inizializzo le 3 distanze totali percorse di riferimento
    distanza_percorsa_soluzione_corrente= distanza_soluzione_iniziale
    distanza_percorsa_migliore= distanza_soluzione_iniziale
    # distanza_percorsa_precedente= distanza_soluzione_iniziale

    Temperature= Temperatura
    
    # Iterazione_fallimento serve per cercare di raggiungere una situazione stabile entro Iterazione//2, altrimenti si ripristina lo stato precedente(temperatura e soluzioni) e si riparte
    # iterazione_fallimento= 0

    j= 0 # parametro per salvare la chiave del numero delle soluzioni di evoluzione

    start_esecuzione= time.time()
    while Temperature > Tfrozen:

        """check_time= time.time() - start_esecuzione

        if iterazione_fallimento == numero_iterazioni //2 and check_time < 1200:
            # Ripristino la temperatura allo stato precedente
            Temperature = Temperature * decreaseT"""

        iteration= 0
        # iterazione_fallimento= 0
        # Cercare un numero di iterazioni per considerarsi in equilibrio
        while iteration < numero_iterazioni:  
            print("iterazione: " + str(iteration))
            # ricerca random soluzione nell'intorno 2-opt
            archi_scelti, new_solution= two_opt(soluzione_corrente, dizionario_citta, dizionario_stazioni)
            costo_new_solution, distanza_percorsa_new_sol= calcola_costo(G,k,dizionario_citta,dizionario_stazioni, new_solution)  # I costi sono dati dal tempo totale speso per il percorso( compreso il tempo di ricarica )

            delta_E= costo_new_solution - costo_soluzione_corrente
            #print("delta_E: "+ str(delta_E))

            if delta_E <= 0:
                
                # Siccome ho un miglioramento con la nuova soluzione rispetto a quella corrente, aggiorno le soluzioni

                # La soluzione corrente diventa quella precedente ( serve tenerne traccia per le condizioni di stabilita )
                """soluzione_precedente= soluzione_corrente
                costo_soluzione_precedente= costo_soluzione_corrente
                distanza_percorsa_precedente= distanza_percorsa_soluzione_corrente"""

                # La nuova soluzione trovata diventa quella corrente
                soluzione_corrente= new_solution
                costo_soluzione_corrente= costo_new_solution
                distanza_percorsa_soluzione_corrente= distanza_percorsa_new_sol


                # Ora controllo che la soluzione corrente sia migliore della soluzione migliore, prima però devo verificare che la soluzione corrente (ex new_solution) sia anche accettabile 
                # in quanto la soluzione_migliore deve essere SEMPRE accettabile in quanto è quella ritornata dall'algoritmo quando finisce

                risultato_correttezza= soluzione_accettabile(soluzione_corrente, G, k, dizionario_citta, dizionario_stazioni)
                
                if risultato_correttezza and costo_soluzione_corrente <= costo_soluzione_migliore :
                    
                    # In archi_scelti ho gli indici, ora tiro fuori i nodi relativi, per tenere traccia di quali archi scelti hanno portato al miglioramento, mi serve per controllare il corretto funzionamento
                    arco1= [soluzione_corrente[archi_scelti[0][0]], soluzione_corrente[archi_scelti[0][1]]]
                    arco2= [soluzione_corrente[archi_scelti[1][0]], soluzione_corrente[archi_scelti[1][1]]]
                    archi_scelti= [arco1,arco2]
                    print("iteration:" + str(iteration))
                    print("Temperature: " + str(Temperature))
                    print("soluzione_corrente: " + str(soluzione_corrente))
                    print("soluzione_migliore: " + str(soluzione_migliore))
                    print("Archi_scelti: " + str(archi_scelti))
                    #time.sleep(10)
                    j +=1
                    
                    dizionario_sol_migliori[j]= [soluzione_migliore, costo_soluzione_migliore, soluzione_corrente, costo_soluzione_corrente, Temperature, iteration, archi_scelti]

                    soluzione_migliore= soluzione_corrente
                    costo_soluzione_migliore= costo_soluzione_corrente
                    distanza_percorsa_migliore= distanza_percorsa_soluzione_corrente

            else:
                # Se sono qui la soluzione nuova che ho trovato non è migliore di quella corrente

                random_choice= round(random.random(),2)
                
                #print("random_choice: "+ str(random_choice))
                exponential_value= math.exp(-delta_E/Temperature)
                #print("exponential_value: " + str(exponential_value))

                if random_choice < exponential_value:
                    # Se random_choice è minore del valore esponenziale allora cambio soluzione corrente con quella nuova, anche se ciò non comporta un miglioramento
                    # questo viene fatto per provare a sfuggire agli eventuali ottimi locali

                    """soluzione_precedente= soluzione_corrente
                    costo_soluzione_precedente= costo_soluzione_corrente
                    distanza_percorsa_precedente= distanza_percorsa_soluzione_corrente"""

                    soluzione_corrente= new_solution
                    costo_soluzione_corrente= costo_new_solution
                    distanza_percorsa_soluzione_corrente= distanza_percorsa_new_sol

            
            iteration += 1
            # !!!!!!!!!Valutare se togliere questa cosa o no, va contro all'idea di ammissibilità di soluzione peggiorativa per evitare gli ottimi locali!!!!!!!!!!
             
            # Uscito dal controllo sul deltaE, controllo se sono nel caso per verificare la correttezza della soluzione        
            # Per aver raggiunto l'equilibrio la soluzione corrente deve essere ammissibile, quindi devo fare un controllo sull'ammissibilità della soluzione, altrimenti continuo a rimanere nel ciclo
            """if iteration == numero_iterazioni - 1:
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
                iteration += 1"""
        
        # Finito While
        Temperature= Temperature * decreaseT
        print("\n ==================================================================")    
    
    end_esecuzione= time.time()

    dizionario_SA= {}

    dizionario_SA['Percorso'] = soluzione_migliore
    dizionario_SA['Distanza Totale']= distanza_percorsa_migliore
    dizionario_SA['Tempo Totale']= costo_soluzione_migliore
    dizionario_SA['Tempo Ricarica']= costo_soluzione_migliore - distanza_percorsa_migliore
    dizionario_SA['Tempo Esecuzione']= end_esecuzione - start_esecuzione

    return dizionario_SA, dizionario_sol_migliori


if __name__ == "__main__":

    k= 56
    dizionario_stazioni = {
                            1: [10, 10], 
                            2: [10, -10], 
                            3: [-10, -10],
                            4: [-10, 10]
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

    percorso= [0, 6, 7, 1, 5, 8, '3S', 4, 3, 2, 9, '1S', 0]


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



    # old: distanza_percorso: 122
    #      tempo_totale: 144.5   
    #      tempo_ricarica: 22.5  


    # new: distanza_percorso: 111
    #      tempo_totale: 141.25
    #      tempo_ricarica: 30.25


    # check: distanza_percorso: 117
    #        tempo_totale: 132.25
    #        tempo_ricarica: 15.25
import random
import os
from shutil import copyfile
from pathlib import Path
from Cliente import Cliente


def generateInstance(Max_Axis,N_CITIES):

    # Le città verranno sparse casualmente tra i quattro quadrati del piano cartesiano

    dizionario_citta= {}
    dizionario_stazioni= {}

    # Creo Stazioni, Ho una stazione per quadrante

    dizionario_stazioni[1]= [Max_Axis//2,Max_Axis//2]
    dizionario_stazioni[2]= [Max_Axis//2,-Max_Axis//2]
    dizionario_stazioni[3]= [-Max_Axis//2,-Max_Axis//2]
    dizionario_stazioni[4]= [-Max_Axis//2, Max_Axis//2]

    nodi_creati= [dizionario_stazioni[1],dizionario_stazioni[2],dizionario_stazioni[3],dizionario_stazioni[4],[0,0]]
    # Creo Città 
    for n in range(1,N_CITIES):
        x= 0
        y= 0
        while [x,y] in nodi_creati:
            x= random.randint(-Max_Axis,Max_Axis)
            y= random.randint(-Max_Axis,Max_Axis)

        nodi_creati.append([x,y])
        cliente= Cliente(x,y,dizionario_stazioni,n)

        dizionario_citta[n]= cliente

    deposito_list= [0,0]


    return dizionario_citta, dizionario_stazioni, deposito_list

def manualInstance(Max_Axis,N_CITIES):
    
    dizionario_citta= {}
    dizionario_stazioni= {}

    # Creo Stazioni, Ho una stazione per quadrante

    dizionario_stazioni[1]= [Max_Axis//2,Max_Axis//2]
    dizionario_stazioni[2]= [Max_Axis//2,-Max_Axis//2]
    dizionario_stazioni[3]= [-Max_Axis//2,-Max_Axis//2]
    dizionario_stazioni[4]= [-Max_Axis//2, Max_Axis//2]

    print("Tenendo conto della lunghezza massima degli assi cartesiani: " + str(Max_Axis) + "\nInserire le coordinate delle città dell'istanza che si vuole analizzare: \n")
    x= 0
    y= 0

    print("MaxAxis: " + str(Max_Axis))

    for n in range(1,N_CITIES):

        x= int(input("Inserire coordinata x per la " + str(n) + " citta: "))
        y= int(input("Inserire coordinata y per la " + str(n) + " citta: "))
        
        citta= Cliente(x,y,dizionario_stazioni,n)
        dizionario_citta[n]= citta
        print("--------Citta Inserita-------")
        print(str(n) + ": " + "[" + str(x) + ", " + str(y) + "]\n")


    deposito_list= [0,0]
    
    return dizionario_citta, dizionario_stazioni, deposito_list

def leggi_istanza():
    k= -1
    Max_Axis= -1
    APP_FOLDER= 'C:/Users/lucap/OneDrive/Desktop/GreenTSP/Istanze/'
    dizionario_citta= {}
    dizionario_stazioni= {}

    leggo_stazioni= 0
    leggo_citta= 0
    totalDir= -1

    file_list= os.listdir(APP_FOLDER)
    totalDir= len(file_list)

    entries= Path(APP_FOLDER)
   
    scelta_directory= -1
    while scelta_directory == -1 or scelta_directory > totalDir:
        i = 1
        if scelta_directory > totalDir:
            print("Scelta non valida")

        print("\nIstanze salvate disponibili: ")

        if totalDir == 0:
            print("\n\tNon sono presenti istanze salvate!")
            print("\n0- Exit\n")
        else:
            for entry in entries.iterdir():
                print("\n" + str(i) + "-" + entry.name)
                i += 1
        
            print("0- Exit")
        
         
        scelta_directory= int(input("Scelta: "))

        j= 1
        if scelta_directory != 0 and scelta_directory < totalDir + 1:

            for entry in entries.iterdir():

                if scelta_directory == j:
                    dir_name= entry.name
                j += 1
            break
    
    if scelta_directory != 0:
        name_file= APP_FOLDER + dir_name + '/dati_istanza_' + str(dir_name[-1:]) + '.txt'

        f= open(name_file,"r")

        for line in f:
            if line != '\n':
                if 'Stazioni' in str(line):
                    leggo_stazioni= 1
                elif 'Clienti' in str(line):
                    leggo_citta= 1
                    leggo_stazioni= 0
                elif 'Dizionario Distanze: ' in str(line):
                    break
                if leggo_stazioni == 0 and leggo_citta == 0:
                    if "Lunghezza" in str(line):
                        list_line= line.split(':')
                        Max_Axis= int(list_line[1][1:])
                    elif "Autonomia" in str(line):
                        list_line= line.split(':')
                        k= int(list_line[1][1:])

                elif leggo_stazioni == 1 and 'Stazioni' not in str(line):

                    list_line= line.split(':')

                    dentro_quadre= list_line[1].split('[')

                    divido_valori= dentro_quadre[1].split(',')

                    x= int(divido_valori[0])
                    y= int(divido_valori[1][1:-2])


                    dizionario_stazioni[int(list_line[0])]= [x,y]

                elif  leggo_citta == 1 and 'Clienti' not in str(line):
                    
                    list_line= line.split(':')
                    #print("list_line: " + str(list_line))
                    dentro_quadre= list_line[1].split('[')

                    divido_valori= dentro_quadre[1].split(',')


                    x= int(divido_valori[0])
                    y= int(divido_valori[1][1:-2])

                    cliente= Cliente(x,y,dizionario_stazioni, int(list_line[0]))

                    dizionario_citta[int(list_line[0])]= cliente

    N_Cities= len(dizionario_citta.keys())
    N_CITIES= N_Cities + 1
    return dizionario_citta, dizionario_stazioni, k , Max_Axis, N_CITIES, scelta_directory



# ---------------------------------------------------- Guida al recupero dei dati dei dizionari in Salva Risultati -------------------------------------------------------------------------------------------------
#
# In dizionario_SA_C (e reciproco NN) ho come chiavi il numero di esecuzione e come valore il dizionario rispettivo della soluzione di quell'esecuzione
#
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
#                                                                                                -C  -->   dizionario_SA_C   -Esecuzione --> [dizionario_SA_C_Esecuzione  (chiavi elencate sotto), dizionario_Evoluzione_Soluzioni_C]
#
#                                                                       -ILS --> dizionario_ILS: -NN -->   dizionario_ILS_C   -percorso
#                                                                                                                             -durata_tot
#                                                                                                                             -tempo di esecuzione
#                                                                                                
#                                                                                                -C -->    dizionario_ILS_NN  -percorso
#                                                                                                                             -durata_tot
#                                                                                                                             -tempo di esecuzione    
#
#                                       
# Sia in Costruttive che in SA , NN e C sono composti dalle seguenti chiavi:
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
# dizionario_dati: -Dati --> dizionario_istanza:   - lunghezza assi
#                                                  - Stazioni ricarica
#                                                  - clienti
#                                                  - Dizionario distanze
#                   
#                  - SA --> dizionario_param_SA:   -Parametri --> dizionario_parametri: - NCitta
#                                                                                       - Iterazioni
#                                                                                       - Temperatura
#                                                                                       - Tfrozen
#                                                                                       - Fattore Decrescita
#                  - ILS --> dizionario_param_ILS: {} ( per ora ancora vuoto )
#
#
#
#


def salva_risultati(dizionario_soluzioni, dizionario_dati):

    # --------------------------------------------------------- Recupero dati -----------------------------------------------------------
    
    # ------------------------------ Dizionario_Dati ------------------------------------------------------------------------------------
    # Flag che indicano la presenza o meno di dati da salvare
    flagSA= 0
    flagILS= 0

    # Recupero i dati principali d'Istanza
    dizionario_istanza= dizionario_dati['Dati']

    Max_Axis= dizionario_istanza['Lunghezza Assi']
    dizionario_stazioni= dizionario_istanza['Stazioni Ricarica']
    dizionario_citta= dizionario_istanza['Citta']
    k= dizionario_istanza['Autonomia']
    G= dizionario_istanza['Dizionario Distanze']

    # Recupero i parametri del SA
    dizionario_parametri_SA= dizionario_dati['SA']

    # Se sono presenti parametri del SA procedo allo scapsulamento dei parametri , altrimenti vado avanti 
    if len(dizionario_parametri_SA) > 0:
        flagSA = 1

        N_CITIES= dizionario_parametri_SA['NCitta']
        Iterazioni= dizionario_parametri_SA['Iterazioni']
        Temperatura= dizionario_parametri_SA['Temperatura']
        Tfrozen= dizionario_parametri_SA['Tfrozen']
        decreaseT= dizionario_parametri_SA['Fattore Decrescita']
    
    # Futura implementazione
    # Recupero i parametri dell' ILS
    """dizionario_parametri_ILS= dizionario_dati['ILS']
    
    
    if len(dizionario_parametri_ILS) > 0:
        flagILS = 1 """
        

    # ------------------------------ Dizionario_Soluzioni ------------------------------------------------------------------------------------
    # Il resto lo spacchetto dopo
    dizionario_Costruttive= dizionario_soluzioni['Costruttive']

    dizionario_MetaEuristiche= dizionario_soluzioni['Meta Euristiche']

    # ----------------------------------------------------------------------------------------------------------------------------------------

    directory= 'Istanze'

    APP_FOLDER= 'C:/Users/lucap/OneDrive/Desktop/GreenTSP/'
    APP_FOLDER= APP_FOLDER + directory + '/'
    
    file_list= os.listdir(APP_FOLDER)

    numero= 1
    name_dir= "Istanza_" + str(numero)
    while name_dir in file_list:
        numero += 1
        name_dir= "Istanza_" + str(numero)
    
    # Creo la cartella
    path_dir= APP_FOLDER + name_dir
    try:
        os.mkdir(path_dir)
        os.chmod(path_dir,777)
    except OSError:
        print("Errore nella creazione della directory: " + str(name_dir))
    else:
        print("Creazione della cartella %s avvenuta con successo!" % name_dir)

    # Salvo le immagini nella cartella
    name_Christofides= "Christofides_Map.jpg" 
    src_dir_Christofides= "C:/Users/lucap/OneDrive/Desktop/GreenTSP/img/Christofides/Christofides_Green_Map.jpg"

    name_Nearest_Neighbour= "NearestNeighbour_Map.jpg" 
    src_dir_Nearest_Neighbour= "C:/Users/lucap/OneDrive/Desktop/GreenTSP/img/NearestNeighbour/NearestNeighbour_GreenTSP.jpg"


    dst_dir= "C:/Users/lucap/OneDrive/Desktop/GreenTSP/Istanze/" + name_dir + "/"

    dst_dir_Christofides= dst_dir + name_Christofides
    dst_dir_Nearest_Neighbour= dst_dir + name_Nearest_Neighbour

    copyfile(src_dir_Christofides,dst_dir_Christofides)
    copyfile(src_dir_Nearest_Neighbour,dst_dir_Nearest_Neighbour)


    # Salvo i dati dell'istanza, quindi coordinate città e stazioni
    #------------------------------------------ DATI ISTANZA.TXT ---------------------------------------------------------
    name_file= path_dir + "/dati_istanza_" + str(name_dir[-1:]) + ".txt" 
    
    cities= list(dizionario_citta.keys())

    stazioni_ricarica= list(dizionario_stazioni.keys())

    f= open(name_file, "w+")

    f.write("Lunghezza Assi Cartesiani: " + str(Max_Axis))
    f.write("\nAutonomia: " + str(k))

    f.write("\nStazioni di ricarica: ")
    for stazione in stazioni_ricarica:
        f.write("\n" +str(stazione) + ": ")
        f.write( str(dizionario_stazioni[stazione]))
    f.write("\nClienti: ")
    for citta in cities:
        f.write("\n" +str(citta) + ": ")
        nodo= dizionario_citta[citta]
        f.write(str(nodo.coordinate))
    f.write("\n\nDizionario Distanze: ")
    cities.insert(0,'0')
    for citta in cities:
        f.write("\n" + str(citta) + ": ")
        f.write(str(G[int(citta)]))

    f.close()

    # Recupero i dati delle soluzioni costruttive NN e C

    dizionario_Nearest_Neighbour= dizionario_Costruttive['NN']
    dizionario_Christofides= dizionario_Costruttive['C']

    # Salvo i risultati di Euristiche Costruttive e Meta Euristiche (nello stesso file)
    if flagSA == 1:
        # Vuol dire che è stato eseguito l'algoritmo di SA e ne recupero il dizionario
        dizionario_SA= dizionario_MetaEuristiche['SA']

        flagSA_NN=0
        flagSA_C=0
        
        # Recupero i dati delle soluzioni NN e C del SA se presenti

        dizionario_SA_NN= dizionario_SA['NN']
        dizionario_SA_C= dizionario_SA['C']

        if len(dizionario_SA_NN) > 0:
            flagSA_NN= 1

        if len(dizionario_SA_C) > 0:
            flagSA_C= 1

        #------------------------------------------ RISULTATI_ALGORITMI.TXT ---------------------------------------------------------

        name_file= path_dir + "/risultati_SA.txt"
        f= open(name_file, "w+")

        f.write("------ Algoritmo Costruttivo Greedy Nearest_Neighbour ------")
        f.write("\nPercorso: " + str(dizionario_Nearest_Neighbour['percorso']))
        f.write("\nDistanza: " + str(dizionario_Nearest_Neighbour['distanza']))
        f.write("\nDurata Tour: " + str(dizionario_Nearest_Neighbour['tempo_tot']))
        f.write("\nTempo Ricarica: " + str(dizionario_Nearest_Neighbour['tempo_ricarica']))
        f.write("\nTempo Esecuzione Algoritmo: " + str(dizionario_Nearest_Neighbour['tempo_esec']))

        f.write("\n\n------ Algoritmo Costruttivo non Greedy Christofides ------")
        f.write("\nPercorso: " + str(dizionario_Christofides['percorso']))
        f.write("\nDistanza: " + str(dizionario_Christofides['distanza']))
        f.write("\nDurata Tour: " + str(dizionario_Christofides['tempo_tot']))
        f.write("\nTempo Ricarica: " + str(dizionario_Christofides['tempo_ricarica']))
        f.write("\nTempo Esecuzione Algoritmo: " + str(dizionario_Christofides['tempo_esec']))

        f.write("\n\n\n----------------------------------------------------------------------------------- SIMULATED ANNEALING --------------------------------------------------------------------------------------")
        
        f.write("\n\nNCitta: " + str(N_CITIES))
        f.write("\tIterazioni: " + str(Iterazioni))
        f.write("\tTemperatura: " + str(Temperatura))
        f.write("\tTFrozen: " + str(Tfrozen))
        f.write("\tFattore Decrescita: " +str(decreaseT))
        f.write("\n")
        f.write("-"*191)

        if flagSA_NN == 1:  # Stampa Soluzioni SA con Nearest Neighbour
            n_esecuzioni= list(dizionario_SA_NN.keys())
            f.write("\n")
            f.write("=" *191)
            f.write("\n\n\t\t\tSoluzione Iniziale: Nearest Neighbour")
            f.write("\n\n")
            f.write("=" *191)

            dizionario_evoluzione={}

            for esecuzione in n_esecuzioni:
                if esecuzione  != 'Tempo Esecuzione Totale':
                    dizionariNN = dizionario_SA_NN[int(esecuzione)]
                    dizionario_SA_NN_Esecuzione= dizionariNN[0]

                    dizionario_evoluzione[esecuzione]= dizionariNN[1]

                    f.write("\n--------------------------------------------------")
                    f.write("\n\nEsecuzione n: " + str(esecuzione))
                    f.write("\nPercorso: " + str(dizionario_SA_NN_Esecuzione['Percorso']))
                    f.write("\nDistanza: " + str(dizionario_SA_NN_Esecuzione['Distanza Totale']))
                    f.write("\nDurata Tour: " + str(dizionario_SA_NN_Esecuzione['Tempo Totale']))
                    f.write("\nTempo Ricarica: " + str(dizionario_SA_NN_Esecuzione['Tempo Ricarica']))
                    f.write("\nTempo Esecuzione: " + str(dizionario_SA_NN_Esecuzione['Tempo Esecuzione']))
            
            f.write("\n\nTempo Esecuzione Totale: " + str(dizionario_SA_NN['Tempo Esecuzione Totale']))

            n_esecuzioni= list(dizionario_evoluzione.keys())
            


            f.write("\n Soluzioni Migliori: ")
            for esecuzione in n_esecuzioni:
                dizionario_Evoluzione_Soluzioni_NN= dizionario_evoluzione[esecuzione]
                f.write("\n----------------------------------------------------------------------------")
                f.write("\nEsecuzione: " + str(esecuzione) + "\n")

                chiavi= list(dizionario_Evoluzione_Soluzioni_NN.keys())
                for chiave in chiavi:
                    valori= dizionario_Evoluzione_Soluzioni_NN[chiave]
                    f.write("\n" + str(chiave) + ") ")
                    f.write("\n Soluzione migliore precedente: " + str(valori[0]))
                    f.write("\n Costo Soluzione migliore precedente: " + str(valori[1]))
                    f.write("\n -------------------------------------------------------")
                    f.write("\n Soluzione Corrente: " + str(valori[4]))
                    f.write("\n Costo soluzione corrente: " + str(valori[5]))
                    f.write("\n archi_scelti: " + str(valori[8]))
                    f.write("\n Nuova soluzione migliore: " + str(valori[2]))
                    f.write("\n Costo nuova soluzione migliore: " + str(valori[3]))
                    f.write("\n Temperatura: " + str(valori[6]))
                    f.write("\n Iterazione: " + str(valori[7]))

                
                f.write("\n----------------------------------------------------------------------------")
        
        if flagSA_C == 1: # Stampa Soluzioni SA con Christofides
            n_esecuzioni= list(dizionario_SA_C.keys())
            f.write("\n")
            f.write("=" *191)
            f.write("\n\n\t\t\tSoluzione Iniziale: Christofides")
            f.write("\n\n")
            f.write("=" *191)

            dizionario_evoluzione={}

            for esecuzione in n_esecuzioni:
                if esecuzione  != 'Tempo Esecuzione Totale':
                    dizionariC= dizionario_SA_C[int(esecuzione)]
                    dizionario_SA_C_Esecuzione= dizionariC[0]

                    dizionario_evoluzione[esecuzione]= dizionariC[1]

                    f.write("\n--------------------------------------------------")
                    f.write("\n\nEsecuzione n: " + str(esecuzione))
                    f.write("\nPercorso: " + str(dizionario_SA_C_Esecuzione['Percorso']))
                    f.write("\nDistanza: " + str(dizionario_SA_C_Esecuzione['Distanza Totale']))
                    f.write("\nDurata Tour: " + str(dizionario_SA_C_Esecuzione['Tempo Totale']))
                    f.write("\nTempo Ricarica: " + str(dizionario_SA_C_Esecuzione['Tempo Ricarica']))
                    f.write("\nTempo Esecuzione: " + str(dizionario_SA_C_Esecuzione['Tempo Esecuzione']))

            f.write("\n\nTempo Esecuzione Totale: " + str(dizionario_SA_C['Tempo Esecuzione Totale']))


            n_esecuzioni= list(dizionario_evoluzione.keys())
            
            f.write("\n Soluzioni Migliori: ")
            for esecuzione in n_esecuzioni:
                dizionario_Evoluzione_Soluzioni_C= dizionario_evoluzione[esecuzione]
                
                f.write("\n----------------------------------------------------------------------------")
                f.write("\nEsecuzione: " + str(esecuzione) + "\n")

                chiavi= list(dizionario_Evoluzione_Soluzioni_C.keys())
                for chiave in chiavi:
                    valori= dizionario_Evoluzione_Soluzioni_C[chiave]
                    f.write("\n" + str(chiave) + ") ")
                    f.write("\n Soluzione precedente: " + str(valori[0]))
                    f.write("\n Costo Soluzione precedente: " + str(valori[1]))
                    f.write("\n Soluzione migliore: " + str(valori[2]))
                    f.write("\n Costo Soluzione migliore: " + str(valori[3]))
                    f.write("\n Temperatura: " + str(valori[4]))
                    f.write("\n Iterazione: " + str(valori[5]))
                    f.write("\n archi_scelti: " + str(valori[6]))
                f.write("\n----------------------------------------------------------------------------")

        f.close()


    # Controllo che nel dizionario passato ci siano anche i risultati dell'ILS
    dizionario_ILS= dizionario_MetaEuristiche['ILS']


    if len(dizionario_ILS) > 0:
        flag_ILS= 1
        flag_ILS_NN= 0
        flag_ILS_C= 0

        dizionario_ILS_NN= dizionario_ILS['NN']
        dizionario_ILS_C= dizionario_ILS['C']

        if len(dizionario_ILS_NN) > 0:
            flag_ILS_NN= 1
        if len(dizionario_ILS_C) > 0:
            flag_ILS_C= 1

        name_file= path_dir + "/risultati_ILS.txt"
        f= open(name_file,"w+")
        
        f.write("------ Algoritmo Costruttivo Greedy Nearest_Neighbour ------")
        f.write("\nPercorso: " + str(dizionario_Nearest_Neighbour['percorso']))
        f.write("\nDistanza: " + str(dizionario_Nearest_Neighbour['distanza']))
        f.write("\nDurata Tour: " + str(dizionario_Nearest_Neighbour['tempo_tot']))
        f.write("\nTempo Ricarica: " + str(dizionario_Nearest_Neighbour['tempo_ricarica']))
        f.write("\nTempo Esecuzione Algoritmo: " + str(dizionario_Nearest_Neighbour['tempo_esec']))

        f.write("\n\n------ Algoritmo Costruttivo non Greedy Christofides ------")
        f.write("\nPercorso: " + str(dizionario_Christofides['percorso']))
        f.write("\nDistanza: " + str(dizionario_Christofides['distanza']))
        f.write("\nDurata Tour: " + str(dizionario_Christofides['tempo_tot']))
        f.write("\nTempo Ricarica: " + str(dizionario_Christofides['tempo_ricarica']))
        f.write("\nTempo Esecuzione Algoritmo: " + str(dizionario_Christofides['tempo_esec']))


        f.write("\n\n\n----------------------------------------------------------------------------------- ITERATIVE LOCAL SEARCH --------------------------------------------------------------------------------------")

        f.write("\n Numero citta: " + str(N_CITIES))

        if flag_ILS_NN:
            f.write("\n")
            f.write("=" *191)
            f.write("\n\n\t\t\tSoluzione Iniziale: Nearest Neighbour")
            f.write("\n\n")
            f.write("=" *191)

            f.write("\n\n Percorso: " + str(dizionario_ILS_NN['percorso']))
            f.write("\nTempo Totale Percorrenza: " + str(dizionario_ILS_NN['tempo_tot']))
            f.write("\nTempo Esecuzione Algoritmo: " + str(dizionario_ILS_NN['execution_time']))

        else:
            f.write("\n\n Esecuzione ILS partendo dalla soluzione di una Nearest Neighbour non effettuata \n\n")

        if flag_ILS_C:
            f.write("\n")
            f.write("=" *191)
            f.write("\n\n\t\t\tSoluzione Iniziale: Christofides")
            f.write("\n\n")
            f.write("=" *191)

            f.write("\n\n Percorso: " + str(dizionario_ILS_C['percorso']))
            f.write("\nTempo Totale Percorrenza: " + str(dizionario_ILS_C['tempo_tot']))
            f.write("\nTempo Esecuzione Algoritmo: " + str(dizionario_ILS_C['execution_time']))

        else:
            f.write("\n\n Esecuzione ILS partendo dalla soluzione di Christofides non effettuata \n\n")


        f.close()
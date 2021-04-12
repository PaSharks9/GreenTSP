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
                    print("list_line: " + str(list_line))
                    dentro_quadre= list_line[1].split('[')

                    divido_valori= dentro_quadre[1].split(',')


                    x= int(divido_valori[0])
                    y= int(divido_valori[1][1:-2])

                    cliente= Cliente(x,y,dizionario_stazioni, int(list_line[0]))

                    dizionario_citta[int(list_line[0])]= cliente

    N_Cities= len(dizionario_citta.keys())
    N_CITIES= N_Cities + 1
    return dizionario_citta, dizionario_stazioni, k , Max_Axis, N_CITIES, scelta_directory



def salva_risultati(directory, dizionarioRisultati, dizionario_citta, dizionario_stazioni, G, Max_Axis, k):
    print("dentro salva_risultati")
    APP_FOLDER= 'C:/Users/lucap/OneDrive/Desktop/GreenTSP/'
    APP_FOLDER= APP_FOLDER + directory + '/'
    
    file_list= os.listdir(APP_FOLDER)
    # number_files= len(file_list)

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
    name_Christofides= "Christofides_Green_Map_" + str(name_dir[-1:]) + ".jpg" 
    src_dir_Christofides= "C:/Users/lucap/OneDrive/Desktop/GreenTSP/img/Christofides/Christofides_Green_Map.jpg"

    name_Nearest_Neighbour= "NearestNeighbour_GreenTSP_" + str(name_dir[-1:]) + ".jpg" 
    src_dir_Nearest_Neighbour= "C:/Users/lucap/OneDrive/Desktop/GreenTSP/img/NearestNeighbour/NearestNeighbour_GreenTSP.jpg"


    dst_dir= "C:/Users/lucap/OneDrive/Desktop/GreenTSP/Istanze/" + name_dir + "/"

    dst_dir_Christofides= dst_dir + name_Christofides
    dst_dir_Nearest_Neighbour= dst_dir + name_Nearest_Neighbour

    copyfile(src_dir_Christofides,dst_dir_Christofides)
    copyfile(src_dir_Nearest_Neighbour,dst_dir_Nearest_Neighbour)


    # Salvo i dati dell'istanza, quindi coordinate città e stazioni
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

    # Salvo i risultati di Euristiche Costruttive e Meta Euristiche (nello stesso file)

    name_file= path_dir + "/risultati_algoritmi.txt"
    f= open(name_file, "w+")

    dizionario_costruttive= dizionarioRisultati['Costruttive']
    dizionario_NN= dizionario_costruttive['NearestNeighbour']
    dizionario_C= dizionario_costruttive['Christofides']

    dizionarioSA= dizionarioRisultati['SA']
    dizionarioSA_NN= dizionarioSA['NN']
    dizionarioSA_C= dizionarioSA['C']

    dizionario_sol_migliore_NN= dizionarioRisultati['sol_migl_NN']
    dizionario_sol_migliore_C= dizionarioRisultati['sol_migl_C']


    f.write("------ Algoritmo Costruttivo Greedy Nearest_Neighbour ------")
    f.write("\nPercorso: " + str(dizionario_NN['percorso']))
    f.write("\nDistanza: " + str(dizionario_NN['distanza']))
    f.write("\nDurata Tour: " + str(dizionario_NN['tempo_tot']))
    f.write("\nTempo Esecuzione Algoritmo: " + str(dizionario_NN['tempo_esec']))

    f.write("\n\n------ Algoritmo Costruttivo non Greedy Christofides ------")
    f.write("\nPercorso: " + str(dizionario_C['percorso']))
    f.write("\nDistanza: " + str(dizionario_C['distanza']))
    f.write("\nDurata Tour: " + str(dizionario_C['tempo_tot']))
    f.write("\nTempo Esecuzione Algoritmo: " + str(dizionario_C['tempo_esec']))

    f.write("\n\n\n----------------------------------------------------------------------------------- SIMULATED ANNEALING --------------------------------------------------------------------------------------")
    if len(dizionarioSA_NN) == 0 and len(dizionarioSA_C) == 0:
        f.write("\n Non ci sono dai da salvare per quanto riguarda il Simulated Annealing")
    else:
        f.write("\nNCitta: " + str(len(cities)))
        f.write("\tIterazioni: " + str(dizionarioSA['n_iterazioni']))
        f.write("\tTemperatura: " + str(dizionarioSA['Temperatura']))
        f.write("\tTFrozen: " + str(dizionarioSA['Tfrozen']))

    if len(dizionarioSA_NN) != 0:
        n_esecuzioni= list(dizionarioSA_NN.keys())
        f.write("\n==========================================================================")
        f.write("\n\n-Soluzione Iniziale: Nearest Neighbour")
        f.write("\n==========================================================================")
        for esecuzione in n_esecuzioni:
            if esecuzione  != 'tempo_esec':
                dizionarioSA_Esec_NN= dizionarioSA_NN[int(esecuzione)]
                f.write("\n--------------------------------------------------")
                f.write("\n\nEsecuzione n: " + str(esecuzione))
                f.write("\nPercorso: " + str(dizionarioSA_Esec_NN['soluzione_migliore']))
                f.write("\nDistanza: " + str(dizionarioSA_Esec_NN['distanza_percorsa_migliore']))
                f.write("\nDurata Tour: " + str(dizionarioSA_Esec_NN['costo_sol_migliore']))
                f.write("\nTempo Esecuzione: " + str(dizionarioSA_Esec_NN['tempo_esecuzione']))
        f.write("\n\nTempo Esecuzione Totale: " + str(dizionarioSA_NN['tempo_esec']))

        f.write("\n Soluzioni Migliori: ")
        chiavi= list(dizionario_sol_migliore_NN.keys())
        i = 0
        for chiave in chiavi:
            f.write("\nEsecuzione")
            f.write("\n" + str(i) + ") ")
            f.write("\n Soluzione precedente: " + str(chiave))
            f.write("\n Soluzione migliore: " + str(dizionario_sol_migliore_NN[chiave][0]))
            f.write("\n Temperatura: " + str(dizionario_sol_migliore_NN[chiave][1]))
            f.write("\n Iterazione: " + str(dizionario_sol_migliore_NN[chiave][2]))
            i += 1

    if len(dizionarioSA_C) != 0:
        n_esecuzioni= list(dizionarioSA_C.keys())
        f.write("\n==========================================================================")
        f.write("\n\n-Soluzione Iniziale:  Christofides")
        f.write("\n==========================================================================")
        for esecuzione in n_esecuzioni:
            if esecuzione  != 'tempo_esec':
                dizionarioSA_Esec_C= dizionarioSA_C[int(esecuzione)]
                f.write("\n--------------------------------------------------")
                f.write("\n\nEsecuzione n: " + str(esecuzione))
                f.write("\nPercorso: " + str(dizionarioSA_Esec_C['soluzione_migliore']))
                f.write("\nDistanza: " + str(dizionarioSA_Esec_C['distanza_percorsa_migliore']))
                f.write("\nDurata Tour: " + str(dizionarioSA_Esec_C['costo_sol_migliore']))
                f.write("\nTempo Esecuzione Algoritmo: " + str(dizionarioSA_Esec_C['tempo_esecuzione']))
        f.write("\n\nTempo Esecuzione Totale: " + str(dizionarioSA_C['tempo_esec']))

        f.write("\n Soluzioni Migliori: ")
        chiavi= list(dizionario_sol_migliore_C.keys())
        i= 0
        for chiave in chiavi:
            f.write("\n" + str(i) + ") ")
            f.write("\n Soluzione precedente: " + str(chiave))
            f.write("\n Soluzione migliore: " + str(dizionario_sol_migliore_C[chiave][0]))
            f.write("\n Temperatura: " + str(dizionario_sol_migliore_C[chiave][1]))
            f.write("\n Iterazione: " + str(dizionario_sol_migliore_C[chiave][2]))
            i += 1



    f.close()
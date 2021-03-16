import random
import os
from shutil import copyfile
from ConstructiveEuristic import euclidean_distance
from pathlib import Path


class Cliente:
    def __init__(self,x,y,dizionario_stazioni,n):
        # Fintanto che le stazioni le lascio in mezzo ai quadranti, le stazioni più vicine ad ogni cliente è la stazione del proprio quadrante
        self.numero= n

        self.coordinate= []
        self.coordinate.append(x)
        self.coordinate.append(y)

        if x >= 0 and y >= 0:
            coordinate_stazione= dizionario_stazioni.get(1) 
            self.distanza_stazione= euclidean_distance(coordinate_stazione,self.coordinate)
        elif x >= 0 and y < 0: 
            coordinate_stazione= dizionario_stazioni.get(2)
            self.distanza_stazione= euclidean_distance(coordinate_stazione,self.coordinate)
        elif x <= 0 and y <= 0: 
            coordinate_stazione= dizionario_stazioni.get(3)
            self.distanza_stazione= euclidean_distance(coordinate_stazione,self.coordinate)
        elif x <= 0 and y > 0:
            coordinate_stazione= dizionario_stazioni.get(4)
            self.distanza_stazione= euclidean_distance(coordinate_stazione,self.coordinate)

        self.distanza_deposito= euclidean_distance(self.coordinate, [0,0])


    def get_quadrant(self):
        if self.coordinate[0] >= 0 and self.coordinate[1] >= 0:
            return 1
        elif self.coordinate[0] >= 0 and self.coordinate[1] < 0:
            return 2
        elif self.coordinate[0] <= 0 and self.coordinate[1] < 0: 
            return 3
        elif self.coordinate[0] <= 0 and self.coordinate[1] > 0:
            return 4

def generateInstance(Max_Axis,N_CITIES):

    # Le città verranno sparse casualmente tra i quattro quadrati del piano cartesiano

    dizionario_citta= {}
    dizionario_stazioni= {}

    # Creo Stazioni, Ho una stazione per quadrante

    dizionario_stazioni[1]= [Max_Axis//2,Max_Axis//2]
    dizionario_stazioni[2]= [Max_Axis//2,-Max_Axis//2]
    dizionario_stazioni[3]= [-Max_Axis//2,-Max_Axis//2]
    dizionario_stazioni[4]= [-Max_Axis//2, Max_Axis//2]


    # Creo Città 
    for n in range(1,N_CITIES):

        x= random.randint(-Max_Axis,Max_Axis)
        y= random.randint(-Max_Axis,Max_Axis)

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

def salva_istanza(dizionario_Nearest_Neighbour, dizionario_Christofides, dizionario_citta, dizionario_stazioni, Max_Axis, k):
    APP_FOLDER= 'C:/Users/lucap/OneDrive/Desktop/GreenTSP/Istanze/'
    totalDir= -1

    for dirs in os.walk(APP_FOLDER):
        totalDir += 1
    
    # Creo la cartella
    name_dir= "Istanza_" + str(totalDir+1)
    path_dir= APP_FOLDER + name_dir
    try:
        os.mkdir(path_dir)
        os.chmod(path_dir,777)
    except OSError:
        print("Errore nella creazione della directory: " + str(name_dir))
    else:
        print("Creazione della cartella %s avvenuta con successo!" % name_dir)


    # Salvo le immagini nella cartella
    name_Christofides= "Christofides_Green_Map_" + str(totalDir+1) + ".jpg" 
    src_dir_Christofides= "C:/Users/lucap/OneDrive/Desktop/GreenTSP/img/Christofides/Christofides_Green_Map.jpg"

    name_Nearest_Neighbour= "NearestNeighbour_GreenTSP_" + str(totalDir+1) + ".jpg" 
    src_dir_Nearest_Neighbour= "C:/Users/lucap/OneDrive/Desktop/GreenTSP/img/NearestNeighbour/NearestNeighbour_GreenTSP.jpg"

    dst_dir= "C:/Users/lucap/OneDrive/Desktop/GreenTSP/Istanze/" + name_dir + "/"

    dst_dir_Christofides= dst_dir + name_Christofides
    dst_dir_Nearest_Neighbour= dst_dir + name_Nearest_Neighbour

    copyfile(src_dir_Christofides,dst_dir_Christofides)
    copyfile(src_dir_Nearest_Neighbour,dst_dir_Nearest_Neighbour)

    # Salvo i dati dell'istanza, quindi coordinate città e stazioni
    name_file= path_dir + "/dati_istanza_" + str(totalDir+1) + ".txt" 
    
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
    f.write("\n")
    f.close()

    # Salvo il file di Christofides
    path_file= path_dir + '/'
    name_file= path_file + "Christofides_Results_" + str(totalDir+1) + ".txt" 
    f= open(name_file, "w+")

    f.write("Percorso: " + str(dizionario_Christofides['percorso']))
    f.write("\nDistanza Percorsa: " + str(dizionario_Christofides['distanza']))
    f.write("\nTempo totale impiegato: "  + str(dizionario_Christofides['tempo_tot']))
    f.write("\nTempo ricarica: " + str(dizionario_Christofides['tempo_ricarica']))

    f.close()

    # Salvo il file della Nearest Neighbour
    path_file= path_dir + '/'
    name_file= path_file + "Nearest_Neighbour_" + str(totalDir+1) + ".txt" 
    f= open(name_file, "w+")



    f.write("Percorso: " + str(dizionario_Nearest_Neighbour['percorso']))
    f.write("\nDistanza Percorsa: " + str(dizionario_Nearest_Neighbour['distanza']))
    f.write("\nTempo totale impiegato: "  + str(dizionario_Nearest_Neighbour['tempo_tot']))
    f.write("\nTempo ricarica: " + str(dizionario_Nearest_Neighbour['tempo_ricarica']))

    f.close()

def leggi_istanza():
    k= -1
    Max_Axis= -1
    APP_FOLDER= 'C:/Users/lucap/OneDrive/Desktop/GreenTSP/Istanze/'
    dizionario_citta= {}
    dizionario_stazioni= {}

    leggo_stazioni= 0
    leggo_citta= 0
    totalDir= -1

    for dirs in os.walk(APP_FOLDER):
        totalDir += 1

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
        print("scelta_dir " + str(scelta_directory))
        if scelta_directory != 0 and scelta_directory < totalDir + 1:
            print("Dentro if")
            for entry in entries.iterdir():
                print("dentro for")
                if scelta_directory == j:
                    dir_name= entry.name
                j += 1
            break
    
    if scelta_directory != 0:
        name_file= APP_FOLDER + dir_name + '/dati_istanza.txt'
        f= open(name_file,"r")

        for line in f:
            if 'Stazioni' in str(line):
                leggo_stazioni= 1
            elif 'Clienti' in str(line):
                leggo_citta= 1
                leggo_stazioni= 0

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

                dentro_quadre= list_line[1].split('[')

                divido_valori= dentro_quadre[1].split(',')


                x= int(divido_valori[0])
                y= int(divido_valori[1][1:-2])

                cliente= Cliente(x,y,dizionario_stazioni, int(list_line[0]))

                dizionario_citta[int(list_line[0])]= cliente

    N_Cities= dizionario_citta.keys()
    return dizionario_citta, dizionario_stazioni, k , Max_Axis, len(N_Cities), scelta_directory
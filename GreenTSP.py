import math
from InstanceGenerator import generateInstance,Cliente,euclidean_distance
from  PlotGenerator import draw_map
from GreedyAlgorithms import NearestNeighbour


if __name__ == "__main__":

    Max_Axis= int(input("Inserire i valori degli assi cartesiani: "))

    N_CITIES= int(input("Inserire il numero di città che si vogliono avere: "))

    # Per avere garantita una soluzione avremo come autonomia minima la massima distanza percorribile, ovvero la diagonale del piano cartesiano
    autonomia_minima = round(euclidean_distance([-Max_Axis,-Max_Axis],[Max_Axis,Max_Axis]),0)
    k = 0
    while k < autonomia_minima:
        k= int(input("L'autonomia minima possibile è: " + str(autonomia_minima) + "\nInserire autonomia auto: "))

    dizionario_citta, dizionario_stazioni, coordinate_deposito= generateInstance(Max_Axis, N_CITIES) 

    deposito= 0

    percorso, distanza_percorsa, tempo_totale, tempo_ricarica= NearestNeighbour(dizionario_citta,dizionario_stazioni,deposito,k,N_CITIES)


    città= list(dizionario_citta.keys())
    stazioni= list(dizionario_stazioni.keys())
    
    print("------------------------Citta------------------------\n")
    for key in città:
        cliente= dizionario_citta.get(int(key))
        print("\nCittà: " + str(key))
        print("\nCoordinate: " + str(cliente.coordinate))
 
    print("------------------------Stazioni di Ricarica------------------------\n")
    for key in stazioni:
        stazione= dizionario_stazioni.get(int(key))
        print("\nStazione: " + str(key) + 'S')
        print("\nCoordinate: " + str(stazione))

    print("------------------------PERCORSO------------------------\n")
    print("Percorso: " + str(percorso) + "\n")
    print("Distanza Percorsa: " + str(distanza_percorsa) + "\n")
    print("Tempo totale di viaggio: " + str(tempo_totale) + "\t di cui tempo speso in ricarica: " + str(tempo_ricarica))


    draw_map(percorso, dizionario_citta, dizionario_stazioni, Max_Axis)


import math
from InstanceGenerator import generateInstance,Cliente,euclidean_distance
from  PlotGenerator import draw_map
from GreedyAlgorithms import NearestNeighbour


if __name__ == "__main__":

    Max_Axis= int(input("Inserire i valori degli assi cartesiani: "))

    N_CITIES= int(input("Inserire il numero di città che si vogliono avere: "))

    autonomia_minima = round(euclidean_distance([-Max_Axis,-Max_Axis],[Max_Axis,Max_Axis]),0)
    k = 0
    while k < autonomia_minima:
        k= int(input("L'autonomia minima possibile è: " + str(autonomia_minima) + "\nInserire autonomia auto: "))

    dizionario_citta, dizionario_stazioni, coordinate_deposito= generateInstance(Max_Axis, N_CITIES) 

    draw_map(dizionario_citta, dizionario_stazioni, Max_Axis)

    deposito= 0

    percorso, distanza_percorsa, tempo_totale, tempo_ricarica= NearestNeighbour(dizionario_citta,dizionario_stazioni,deposito,k,N_CITIES)

    print("------------------------PERCORSO------------------------\n")
    print("Percorso: " + str(percorso) + "\n")
    print("Distanza Percorsa: " + str(distanza_percorsa) + "\n")
    print("Tempo totale di viaggio: " + str(tempo_totale) + "\t di cui tempo speso in ricarica: " + str(tempo_ricarica))


import math
from InstanceGenerator import generateInstance
from  PlotGenerator import draw_map
# from GreedyAlgorithms import NearestNeighbour


if __name__ == "__main__":

    Max_Axis= int(input("Inserire i valori degli assi cartesiani: "))

    N_CITIES= int(input("Inserire il numero di città che si vogliono avere: "))

    k= int(input("Inserire autonomia auto: "))

    dizionario_citta, dizionario_stazioni, coordinate_deposito= generateInstance(Max_Axis, N_CITIES) 

    draw_map(dizionario_citta, dizionario_stazioni, Max_Axis)

    print(str(dizionario_citta))
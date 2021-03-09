from InstanceGenerator import generateInstance
from  PlotGenerator import draw_map
import math


def euclidean_distance(A,B):
    x_A= A[0]
    y_A= A[1]

    x_B= B[0]
    y_B= B[1]

    x= abs(x_A - x_B)
    y= abs(y_A - y_B)

    d= math.sqrt(x**2 + y**2)

    return d



if __name__ == "__main__":

    Max_Axis= int(input("Inserire i valori degli assi cartesiani: "))

    N_CITIES= int(input("Inserire il numero di città che si vogliono avere: "))

    dizionario_citta, dizionario_stazioni= generateInstance(Max_Axis, N_CITIES)
   

    draw_map(dizionario_citta, dizionario_stazioni, Max_Axis)

    A= dizionario_citta.get(1)
    B= dizionario_citta.get(2)

    res= euclidean_distance(A,B)
    intRes= int(res)
    print("A: " + str(A))
    print("B: " + str(B))
    print("Res: " + str(res))
    print("IntRes: " + str(intRes))
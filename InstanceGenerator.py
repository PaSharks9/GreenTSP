import random
from GreedyAlgorithms import euclidean_distance

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

    def get_quadrant(self):
        if self.coordinate[0] >= 0 and self.coordinate[1] >= 0:
            return 1
        elif self.coordinate[0] >= 0 and self.coordinate[1] >= 0:
            return 2
        elif self.coordinate[0] >= 0 and self.coordinate[1] >= 0: 
            return 3
        elif self.coordinate[0] >= 0 and self.coordinate[1] >= 0:
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




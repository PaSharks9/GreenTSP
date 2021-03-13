import random
from ConstructiveEuristic import euclidean_distance

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
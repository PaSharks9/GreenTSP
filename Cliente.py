import math
def euclidean_distance(A,B):
    x_A= A[0]
    y_A= A[1]

    x_B= B[0]
    y_B= B[1]

    x= abs(x_A - x_B)
    y= abs(y_A - y_B)

    d= math.sqrt(x**2 + y**2)

    return int(d)

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


if __name__ == "__main__":
    A= euclidean_distance([0, -9],[3, -16])
    print(A)
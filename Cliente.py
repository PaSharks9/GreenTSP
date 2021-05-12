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


def soluzione_accettabile(percorso, G, k, dizionario_citta, dizionario_stazioni):
    index= 0
    autonomia= k
    while index < len(percorso) - 1:
        """print("index/percorso: ")
        print(str(index) + "/" + str(len(percorso)))
        print("\nNodo1: " + str(percorso[index]))
        print("Nodo2: " + str(percorso[index + 1]))
        print("\nautonomia: " + str(autonomia))"""
        if 'S' not in str(percorso[index]) and 'S' not in str(percorso[index+1]):
            distanza_da_percorrere= G[percorso[index]][percorso[index+1]]
            #print("distanza_da_percorrere: " + str(distanza_da_percorrere))
            if autonomia - distanza_da_percorrere < 0:
                # Significa che non è una soluzione accettabile
                return False
            else:
                autonomia -= distanza_da_percorrere

        elif 'S' in str(percorso[index]) and 'S' not in str(percorso[index + 1]): # Tratta da una stazione 
            
            # Parto da una stazione, quindi avrò autonomia massima
            autonomia= k
            #print("Autonomia Ricaricata: " + str(autonomia))
            if percorso[index + 1] != 0:
                # Devo solo controllare di avere autonomia sufficiente per arrivare nella citta successiva
                nodo_stazione= int(percorso[index].replace('S',''))
                coordinate_stazione= dizionario_stazioni.get(nodo_stazione)
                #print("coordinate_stazione: " + str(coordinate_stazione))

                nodo_citta= dizionario_citta.get(int(percorso[index + 1]))
                coordinate_citta= nodo_citta.coordinate
                #print("coordinate_citta: " + str(coordinate_citta))

                distanza_da_percorrere= euclidean_distance(coordinate_stazione, coordinate_citta)
                #print("distanza_da_percorrere: " + str(distanza_da_percorrere))
                if autonomia - distanza_da_percorrere < 0:
                    # Significa che non è una soluzione accettabile
                    return False
                else:
                    autonomia -= distanza_da_percorrere

        elif 'S' not in str(percorso[index]) and 'S' in str(percorso[index + 1]): # Tratta da una citta ad una stazione  (TEORICAMENTE QUESTO if non dovrebbe andare in false perchè i due if precedenti controllano se una volta arrivati nella città successiva si ha autonomia a sufficienza per andare in una stazione)
            
            # Considerare caso in cui si parta dal deposito e si vada in una stazione di ricarica (Mossa legale)

            if percorso[index] == 0:
                coordinate_citta= [0,0]
            else:
                nodo_citta= dizionario_citta.get(int(percorso[index]))
                coordinate_citta= nodo_citta.coordinate
            #print("coordinate_citta: " + str(coordinate_citta))

            nodo_stazione= int(percorso[index + 1].replace('S',''))
            coordinate_stazione= dizionario_stazioni.get(nodo_stazione)
            #print("coordinate_stazione: " + str(coordinate_stazione))


            distanza_da_percorrere= euclidean_distance(coordinate_stazione, coordinate_citta)
            #print("distanza_da_percorrere: " + str(distanza_da_percorrere))
            if autonomia - distanza_da_percorrere < 0:
                # Significa che non è una soluzione accettabile
                return False
            else:
                autonomia -= distanza_da_percorrere

        index += 1

    # Se sono arrivato fino a qui significa che tutto è regolare quindi ritorno True

    return True




def soluzione_accettabile_debug(percorso, G, k, dizionario_citta, dizionario_stazioni):
    index= 0
    autonomia= k
    while index < len(percorso) - 1:
        """print("index/percorso: ")
        print(str(index) + "/" + str(len(percorso)))
        print("\nNodo1: " + str(percorso[index]))
        print("Nodo2: " + str(percorso[index + 1]))
        print("\nautonomia: " + str(autonomia))"""
        if 'S' not in str(percorso[index]) and 'S' not in str(percorso[index+1]):
            distanza_da_percorrere= G[percorso[index]][percorso[index+1]]
            #print("distanza_da_percorrere: " + str(distanza_da_percorrere))
            if autonomia - distanza_da_percorrere < 0:
                # Significa che non è una soluzione accettabile
                return False, autonomia,distanza_da_percorrere, (percorso[index],percorso[index+1])
            else:
                autonomia -= distanza_da_percorrere

        elif 'S' in str(percorso[index]) and 'S' not in str(percorso[index + 1]): # Tratta da una stazione 
            
            # Parto da una stazione, quindi avrò autonomia massima
            autonomia= k
            #print("Autonomia Ricaricata: " + str(autonomia))
            if percorso[index + 1] != 0:
                # Devo solo controllare di avere autonomia sufficiente per arrivare nella citta successiva
                nodo_stazione= int(percorso[index].replace('S',''))
                coordinate_stazione= dizionario_stazioni.get(nodo_stazione)
                #print("coordinate_stazione: " + str(coordinate_stazione))

                nodo_citta= dizionario_citta.get(int(percorso[index + 1]))
                coordinate_citta= nodo_citta.coordinate
                #print("coordinate_citta: " + str(coordinate_citta))

                distanza_da_percorrere= euclidean_distance(coordinate_stazione, coordinate_citta)
                #print("distanza_da_percorrere: " + str(distanza_da_percorrere))
                if autonomia - distanza_da_percorrere < 0:
                    # Significa che non è una soluzione accettabile
                    return False, autonomia, distanza_da_percorrere, (percorso[index],percorso[index+1])
                else:
                    autonomia -= distanza_da_percorrere

        elif 'S' not in str(percorso[index]) and 'S' in str(percorso[index + 1]): # Tratta da una citta ad una stazione  (TEORICAMENTE QUESTO if non dovrebbe andare in false perchè i due if precedenti controllano se una volta arrivati nella città successiva si ha autonomia a sufficienza per andare in una stazione)
            
            # Considerare caso in cui si parta dal deposito e si vada in una stazione di ricarica (Mossa legale)

            if percorso[index] == 0:
                coordinate_citta= [0,0]
            else:
                nodo_citta= dizionario_citta.get(int(percorso[index]))
                coordinate_citta= nodo_citta.coordinate
            #print("coordinate_citta: " + str(coordinate_citta))

            nodo_stazione= int(percorso[index + 1].replace('S',''))
            coordinate_stazione= dizionario_stazioni.get(nodo_stazione)
            #print("coordinate_stazione: " + str(coordinate_stazione))


            distanza_da_percorrere= euclidean_distance(coordinate_stazione, coordinate_citta)
            #print("distanza_da_percorrere: " + str(distanza_da_percorrere))
            if autonomia - distanza_da_percorrere < 0:
                # Significa che non è una soluzione accettabile
                return False, autonomia,distanza_da_percorrere, (percorso[index],percorso[index+1])
            else:
                autonomia -= distanza_da_percorrere

        index += 1

    # Se sono arrivato fino a qui significa che tutto è regolare quindi ritorno True

    return True





def calcola_costo(G, k, dizionario_citta, dizionario_stazioni, percorso):
    distanza_percorsa= 0
    autonomia= k
    tempo_tot= 0

    index= 0

    while index < len(percorso) - 1:
        """print("\nindex/percorso: ")
        print(str(index) + "/" + str(len(percorso)))
        print("\nNodo1: " + str(percorso[index]))
        print("Nodo2: " + str(percorso[index + 1]))
        print("\nautonomia: " + str(autonomia))"""
        if 'S' not in str(percorso[index]) and 'S' not in str(percorso[index+1]):  # Significa che è una tratta tra due città e non tra due stazioni o tra una città e stazione
            
            #print("\npercorso[index]: " + str(percorso[index]))
            #print("percorso[index+1]: " + str(percorso[index+1]))
            distanza_percorsa += G[percorso[index]][percorso[index+1]]
            #print("distanza: " + str(G[percorso[index]][percorso[index+1]]))
            #print("distanza_percorsa: " + str(distanza_percorsa))
            autonomia -= G[percorso[index]][percorso[index+1]]

        elif 'S' in str(percorso[index]) and 'S' not in str(percorso[index + 1]): # Tratta da una stazione ad una citta, la distanza percorsa la devo ricavare dai dizionari citta e stazione
            
            #print("\npercorso[index]: " + str(percorso[index]))
            #print("percorso[index+1]: " + str(percorso[index+1]))

            station= percorso[index]
            station= station.replace('S','')
            coordinate_stazione= dizionario_stazioni.get(int(station))

            if percorso[index + 1] == 0:  # caso in cui sia una tratta da stazione a deposito ( ultimo arco del tour )
                coordinate_citta= [0,0]
            
            else:
                citta= dizionario_citta.get(int(percorso[index + 1]))
                coordinate_citta= citta.coordinate

            distanza_percorsa += euclidean_distance(coordinate_stazione, coordinate_citta)

            #print("distanza: " + str(euclidean_distance(coordinate_stazione, coordinate_citta)))
            #print("distanza_percorsa: " + str(distanza_percorsa))

            autonomia -= euclidean_distance(coordinate_stazione, coordinate_citta)
            #print("autonomia futura: " + str(autonomia))
        elif 'S' not in str(percorso[index]) and 'S' in str(percorso[index + 1]): # Tratta da una citta ad una stazione, in questa tratta devo considerare anche il tempo di ricarica dato che il costo è il tempo del tour
            
            #print("\npercorso[index]: " + str(percorso[index]))
            #print("percorso[index+1]: " + str(percorso[index+1]))
            
            station= percorso[index + 1]
            station= station.replace('S','')
            coordinate_stazione= dizionario_stazioni.get(int(station))

            if percorso[index] == 0:  # caso in cui sia una tratta da deposito a stazione ( primo arco del tour )
                coordinate_citta= [0,0]
            else:
                citta= dizionario_citta.get(int(percorso[index]))
                coordinate_citta= citta.coordinate

            distanza_percorsa += euclidean_distance(coordinate_stazione, coordinate_citta)

            #print("distanza: " + str(euclidean_distance(coordinate_stazione, coordinate_citta)))
            #print("distanza_percorsa: " + str(distanza_percorsa))
            
            autonomia -= euclidean_distance(coordinate_stazione, coordinate_citta)

            # Caso in cui prima di tornare al deposito sono in una stazione, in questo caso la ricarica sarà precisa per tornare al deposito, non carico di più
            if index + 1 == len(percorso) - 2:  # index+1 è l'indice della stazione , len(percorso) - 2 è l'indice della penultima tappa del percorso
                distanza_stazione_deposito= euclidean_distance(coordinate_stazione, [0,0])
                delta_ricarica= distanza_stazione_deposito - autonomia
            else:
                delta_ricarica=  k - autonomia
            
            #print("delta_ricarica: " + str(delta_ricarica))

            #print("Tempo_ricarica: " + str(0.25*delta_ricarica))
            tempo_tot +=  0.25*delta_ricarica
            #print("tempo_tot: " + str(tempo_tot))
            autonomia= k

            
        elif 'S' in str(percorso[index]) and 'S' in str(percorso[index + 1]): # Caso in cui da una stazione di rifornimento si vada all'altra         
            
            #print("\npercorso[index]: " + str(percorso[index]))
            #print("percorso[index+1]: " + str(percorso[index+1]))

            station1= percorso[index]
            station1= station1.replace('S','')

            coordinate_stazione1= dizionario_stazioni.get(int(station1))

            station2= percorso[index + 1]
            
            station2= station2.replace('S','')

            coordinate_stazione2= dizionario_stazioni.get(int(station2))
            

            distanza_percorsa += euclidean_distance(coordinate_stazione1, coordinate_stazione2)

            #print("distanza: " + str(euclidean_distance(coordinate_stazione1, coordinate_stazione2)) )
            #print("distanza_percorsa: " + str(distanza_percorsa))

            autonomia -= euclidean_distance(coordinate_stazione1, coordinate_stazione2)
            
            # Essendo partiti ed arrivati in una stazione si ricarica
            delta_ricarica=  k - autonomia

            tempo_tot +=  0.25*delta_ricarica
            #print("tempo_tot: " + str(tempo_tot))
            autonomia= k

        index += 1
    
    tempo_tot += distanza_percorsa

    return tempo_tot, distanza_percorsa
    


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
    k= 56
    dizionario_stazioni = {1: [10, 10], 2: [10, -10], 3: [-10, -10], 4: [-10, 10]}

    lista_citta=[
        [2, -1],
        [-13, -2],
        [-11, 3],
        [8, 7],
        [12, 20],
        [-6, 1],
        [11, -13],
        [-17, -13],
        [1, -1]
    ]

    G={ 
        0: {1: 2, 2: 13, 3: 11, 4: 10, 5: 23, 6: 6, 7: 17, 8: 21, 9: 1},
        1: {0: 2, 2: 15, 3: 13, 4: 10, 5: 23, 6: 8, 7: 15, 8: 22, 9: 1},
        2: {0: 13, 1: 15, 3: 5, 4: 22, 5: 33, 6: 7, 7: 26, 8: 11, 9: 14},
        3: {0: 11, 1: 13, 2: 5, 4: 19, 5: 28, 6: 5, 7: 27, 8: 17, 9: 12},
        4: {0: 10, 1: 10, 2: 22, 3: 19, 5: 13, 6: 15, 7: 20, 8: 32, 9: 10},
        5: {0: 23, 1: 23, 2: 33, 3: 28, 4: 13, 6: 26, 7: 33, 8: 43, 9: 23},
        6: {0: 6, 1: 8, 2: 7, 3: 5, 4: 15, 5: 26, 7: 22, 8: 17, 9: 7},
        7: {0: 17, 1: 15, 2: 26, 3: 27, 4: 20, 5: 33, 6: 22, 8: 28, 9: 15},
        8: {0: 21, 1: 22, 2: 11, 3: 17, 4: 32, 5: 43, 6: 17, 7: 28, 9: 21},
        9: {0: 1, 1: 1, 2: 14, 3: 12, 4: 10, 5: 23, 6: 7, 7: 15, 8: 21}
    }



    i = 1
    dizionario_citta= {}
    for element in lista_citta: 
        cliente= Cliente(element[0],element[1],dizionario_stazioni,i)
        dizionario_citta[i]= cliente
        i += 1
    
    percorso= [0, 9, 1, 5, '1S', 4, 7, '3S', 8, 2, 3, 6, 0]
    

    print("res: " + str(soluzione_accettabile_debug(percorso, G, k, dizionario_citta, dizionario_stazioni)))
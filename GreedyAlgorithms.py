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

def find_next_node(percorso,current_node,dizionario_citta,dizionario_stazioni,autonomia):
    min_dist= 10000000
    clients= list(dizionario_citta.keys())

    if current_node == 0:
        current_coordinate= [0,0]
    else:
        cliente= dizionario_citta.get(current_node) 
        current_coordinate= cliente.coordinate

    for client in clients:
        if client not in percorso:
            node= dizionario_citta.get(client)
            distance= euclidean_distance(node.coordinate,current_coordinate)

            if distance <= min_dist:
                min_dist= distance
                
    if min_dist 




def NearestNeighbour(dizionario_citta, dizionario_stazioni, deposito, k):
    autonomia= k
    percorso= []

    current_node= deposito

    # Il nodo 0 è il deposito
    percorso.append(0)

    next_node= find_next_node(percorso,current_node,dizionario_citta,dizionario_stazioni,autonomia)




"""
A= dizionario_citta.get(1)
B= dizionario_citta.get(2)

res= euclidean_distance(A,B)
intRes= int(res)
print("A: " + str(A))
print("B: " + str(B))
print("Res: " + str(res))
print("IntRes: " + str(intRes))"""
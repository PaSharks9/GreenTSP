import matplotlib.pyplot as plt

def draw_map(percorso, dizionario_citta, dizionario_stazioni, Max_Axis):
    
    plt.title('GreenTSP Map')
    plt.grid(True)

    pointsCity_List= list(dizionario_citta.keys())

    pointsStation_List= list(dizionario_stazioni.keys())

    # Do valori agli assi cartesiani
    plt.axis([-Max_Axis-1, Max_Axis+1, -Max_Axis-1, Max_Axis+1])

    plt.xticks([1*k for k in range(-Max_Axis,Max_Axis+1)])
    plt.yticks([1*k for k in range(-Max_Axis,Max_Axis+1)])
    # Creo i 4 quadranti disegnando semplicemente la retta verticale e la retta orizzontale
    plt.axvline(0,0,color='black')

    plt.axhline(0,0,color='black')

    x_city_coordinates=[]
    y_city_coordinates=[]

    x_stations_coordinates=[]
    y_stations_coordinates=[]


    # Disegno i punti
    for key in pointsCity_List:
        cliente= dizionario_citta.get(key)
        x_city_coordinates.append(cliente.coordinate[0])
        y_city_coordinates.append(cliente.coordinate[1])

    plt.scatter(x_city_coordinates, y_city_coordinates, s=20, edgecolors='none', c='green', label="Cliente")
    # Do i nomi ai punti
    for key in pointsCity_List:
        plt.annotate(str(key), (x_city_coordinates[key - 1],y_city_coordinates[key - 1]))


    for key in pointsStation_List:
        coordinate= dizionario_stazioni.get(key)
        x_stations_coordinates.append(coordinate[0])
        y_stations_coordinates.append(coordinate[1])
    
    plt.scatter(x_stations_coordinates, y_stations_coordinates, marker='x', s=50, edgecolors='none', c='red', label="Stazioni di Ricarica")
   
    #Do i nomi alle stazioni
    for key in pointsStation_List:
        name_station= str(key) + "S"
        plt.annotate(name_station, (x_stations_coordinates[key - 1],y_stations_coordinates[key - 1]))

    #Do il nome al deposito
    plt.annotate('D', (0,0))



    # Disegno il deposito che si trova in coordinate [0,0]
    plt.scatter(0,0,s=50, edgecolors='none', c='blue', label="Deposito")

    plt.savefig('img/TSPMap.jpg')

    
    # ------------------------- Disegno del Tour -------------------------
    current_index= 0
    next_index= 1
    i = 1
    lunghezza_percorso= len(percorso)


    while next_index < lunghezza_percorso:
        current_node= percorso[current_index]
        next_node= percorso[next_index]

        if 'S' not in str(current_node) and current_node != 0:
            current_client= dizionario_citta.get(current_node)
            current_coordinate= current_client.coordinate
        elif current_node == 0:
            current_coordinate= [0,0]
        else:
            current_node= int(current_node.replace('S',''))
            current_coordinate= dizionario_stazioni.get(current_node)

        if 'S' not in str(next_node) and next_node != 0:
            next_client= dizionario_citta.get(int(next_node))
            next_coordinate= next_client.coordinate
        elif next_node == 0:
            next_coordinate= [0,0]
        else:
            next_client= int(next_node.replace('S',''))
            next_coordinate= dizionario_stazioni.get(next_client)

        if 'S' in str(next_node):
            color= 'yellow'
        else:
            color= 'green'

        plt.plot([current_coordinate[0],next_coordinate[0]],[current_coordinate[1],next_coordinate[1]], color= color)
        current_index= next_index
        next_index += 1

        """file_name= 'img/TSPMap_Tour_' + str(i) + '.jpg'
        plt.savefig(file_name)"""
        i += 1


    plt.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left", ncol=3)

    plt.grid(True)

    plt.savefig('img/TSPMap_Tour')
    plt.show()


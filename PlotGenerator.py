import matplotlib.pyplot as plt

def draw_map(dizionario_citta, dizionario_stazioni, Max_Axis):

    pointsCity_List= list(dizionario_citta.keys())

    pointsStation_List= list(dizionario_stazioni.keys())

    # Do valori agli assi cartesiani
    plt.axis([-Max_Axis, Max_Axis, -Max_Axis, Max_Axis])

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

    for key in pointsStation_List:
        coordinate= dizionario_stazioni.get(key)
        x_stations_coordinates.append(coordinate[0])
        y_stations_coordinates.append(coordinate[1])

    plt.scatter(x_stations_coordinates, y_stations_coordinates, marker='x', s=50, edgecolors='none', c='red', label="Stazioni di Ricarica")


    # Disegno il deposito che si trova in coordinate [0,0]
    plt.scatter(0,0,s=50, edgecolors='none', c='blue', label="Deposito")


    plt.title('GreenTSP Map')

    plt.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left", ncol=3)
    plt.grid(True)

    # plt.savefig('TSPMap.jpg')

    plt.show()
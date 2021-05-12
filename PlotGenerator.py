import matplotlib.pyplot as plt


def draw_map(percorso, dizionario_citta, dizionario_stazioni, Max_Axis, dir):
    # -------------------- Creo SubPlot --------------------
    figNN= plt.figure() 
    # -------------------- INIZIALIZZO GRAFICO --------------------
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
    
    # ------------------------- Disegno del Tour -------------------------
    current_index= 0
    next_index= 1
    i = 1
    lunghezza_percorso= len(percorso)


    while next_index < lunghezza_percorso:
        current_node= percorso[current_index]
        next_node= percorso[next_index]
        #print("current_node: " + str(current_node))
        #print("next_node: " + str(next_node))
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


    plt.savefig('img/'+ str(dir))

    plt.close(figNN)


def draw_mst(dizionario_citta, Max_Axis, archi_usati):
    # -------------------- Creo SubPlot --------------------
    figMST= plt.figure()
    # -------------------- INIZIALIZZO GRAFICO --------------------
    plt.title('MST Cities-Map')
    plt.grid(True)

    pointsCity_List= list(dizionario_citta.keys())

    # Do valori agli assi cartesiani
    plt.axis([-Max_Axis-1, Max_Axis+1, -Max_Axis-1, Max_Axis+1])

    plt.xticks([1*k for k in range(-Max_Axis,Max_Axis+1)])
    plt.yticks([1*k for k in range(-Max_Axis,Max_Axis+1)])
    # Creo i 4 quadranti disegnando semplicemente la retta verticale e la retta orizzontale
    plt.axvline(0,0,color='black')

    plt.axhline(0,0,color='black')

    x_city_coordinates=[]
    y_city_coordinates=[]


    #-------------------- Disegno i punti --------------------
    for key in pointsCity_List:
        cliente= dizionario_citta.get(key)
        x_city_coordinates.append(cliente.coordinate[0])
        y_city_coordinates.append(cliente.coordinate[1])

    plt.scatter(x_city_coordinates, y_city_coordinates, s=20, edgecolors='none', c='green', label="Cliente")
    # Do i nomi ai punti
    for key in pointsCity_List:
        plt.annotate(str(key), (x_city_coordinates[key - 1],y_city_coordinates[key - 1]))

    #Do il nome al deposito
    plt.annotate('D', (0,0))

    # Disegno il deposito che si trova in coordinate [0,0]
    plt.scatter(0,0,s=50, edgecolors='none', c='blue', label="Deposito")

    plt.savefig('img/Christofides/MST/MST_CitiesMap.jpg')

    #-------------------- Disegno semirette --------------------
    #i = 0
    for edge in archi_usati:
        nodo1= edge[0]
        nodo2= edge[1]
        distanza= edge[2]

        if nodo1 != 0:
            nodo_1= dizionario_citta.get(int(nodo1))
            coordinate1= nodo_1.coordinate
        else:
            coordinate1= [0,0]

        if nodo2 != 0:
            nodo_2= dizionario_citta.get(int(nodo2))
            coordinate2= nodo_2.coordinate
        else:
            coordinate2= [0,0]
        
        
        plt.plot([coordinate1[0],coordinate2[0]],[coordinate1[1],coordinate2[1]], color='blue', label=distanza)
        
        
        """directory= "img/Christofides/MST/"
        filename= "MST_Map_" + str(i) + ".jpg"

        plt.savefig(directory+filename)
        i += 1"""
    
    plt.savefig('img/Christofides/MST/MST_Map.jpg')
    plt.close(figMST)

def draw_perfect_matching(dizionario_citta, Max_Axis, subgraph, archi_usati):

    # -------------------- Creo SubPlot --------------------
    figPM= plt.figure()

    # -------------------- INIZIALIZZO GRAFICO --------------------
    plt.title('PM Cities-Map')
    plt.grid(True)

    # Do valori agli assi cartesiani
    plt.axis([-Max_Axis-1, Max_Axis+1, -Max_Axis-1, Max_Axis+1])

    plt.xticks([1*k for k in range(-Max_Axis,Max_Axis+1)])
    plt.yticks([1*k for k in range(-Max_Axis,Max_Axis+1)])
    # Creo i 4 quadranti disegnando semplicemente la retta verticale e la retta orizzontale
    plt.axvline(0,0,color='black')

    plt.axhline(0,0,color='black')

    x_city_coordinates=[]
    y_city_coordinates=[]


    #-------------------- Disegno i punti --------------------
    for key in subgraph:
        if key == 0:
            x_city_coordinates.append(0)
            y_city_coordinates.append(0)
        else:
            cliente= dizionario_citta.get(key)
            x_city_coordinates.append(cliente.coordinate[0])
            y_city_coordinates.append(cliente.coordinate[1])

    plt.scatter(x_city_coordinates, y_city_coordinates, s=20, edgecolors='none', c='green', label="Cliente")
    # Do i nomi ai punti
    i = 0
    for key in subgraph:
        plt.annotate(str(key), (x_city_coordinates[i],y_city_coordinates[i]))
        i += 1

    plt.savefig('img/Christofides/Perfect_Matching/PM_CitiesMap.jpg')

    #-------------------- Disegno semirette --------------------
    i = 0
    for edge in archi_usati:
        nodo1= edge[0]
        nodo2= edge[1]
        distanza= edge[2]

        if nodo1 != 0:
            nodo_1= dizionario_citta.get(int(nodo1))
            coordinate1= nodo_1.coordinate
        else:
            coordinate1= [0,0]

        if nodo2 != 0:
            nodo_2= dizionario_citta.get(int(nodo2))
            coordinate2= nodo_2.coordinate
        else:
            coordinate2= [0,0]
        
        
        plt.plot([coordinate1[0],coordinate2[0]],[coordinate1[1],coordinate2[1]], color='blue', label=distanza)
        
        
        """directory= "img/Christofides/Perfect_Matching/"
        filename= "PM_Map_" + str(i) + ".jpg"

        plt.savefig(directory+filename)
        i += 1"""
    
    plt.savefig('img/Christofides/Perfect_Matching/MST_Map.jpg')
    plt.close(figPM)

def draw_Christofides(christofides_graph_no_recharge, dizionario_citta, Max_Axis):

    """keys= list(christofides_graph_no_recharge.keys())
    for key in keys:
        print(str(key) + ": " + str(christofides_graph_no_recharge.get(int(key))))"""

    # -------------------- Creo SubPlot --------------------
    figC= plt.figure()
    # -------------------- INIZIALIZZO GRAFICO --------------------

    plt.title('Christofides Cities-Map')
    plt.grid(True)

    # Do valori agli assi cartesiani
    plt.axis([-Max_Axis-1, Max_Axis+1, -Max_Axis-1, Max_Axis+1])

    plt.xticks([1*k for k in range(-Max_Axis,Max_Axis+1)])
    plt.yticks([1*k for k in range(-Max_Axis,Max_Axis+1)])
    # Creo i 4 quadranti disegnando semplicemente la retta verticale e la retta orizzontale
    plt.axvline(0,0,color='black')

    plt.axhline(0,0,color='black')

    x_city_coordinates=[]
    y_city_coordinates=[]

    #-------------------- Disegno i punti --------------------

    cities= list(dizionario_citta.keys())
    cities.append(0)

    for key in cities:
        if key == 0:
            x_city_coordinates.append(0)
            y_city_coordinates.append(0)
        else:
            cliente= dizionario_citta.get(key)
            x_city_coordinates.append(cliente.coordinate[0])
            y_city_coordinates.append(cliente.coordinate[1])

    plt.scatter(x_city_coordinates, y_city_coordinates, s=20, edgecolors='none', c='green', label="Cliente")
    # Do i nomi ai punti
    i = 0
    for key in cities:
        plt.annotate(str(key), (x_city_coordinates[i],y_city_coordinates[i]))
        i += 1

    plt.savefig('img/Christofides/Christofides_CitiesMap.jpg')


    #-------------------- Disegno semirette --------------------

    i = 0
    for vertex in cities:
        edge_v= christofides_graph_no_recharge.get(int(vertex))

        nodes_u= list(edge_v.keys())

        for u in nodes_u:
 
            if vertex != 0:
                nodo_1= dizionario_citta.get(int(vertex))
                coordinate1= nodo_1.coordinate
            else:
                coordinate1= [0,0]

            if u != 0:
                nodo_2= dizionario_citta.get(int(u))
                coordinate2= nodo_2.coordinate
            else:
                coordinate2= [0,0]
        
            plt.plot([coordinate1[0],coordinate2[0]],[coordinate1[1],coordinate2[1]], color='green')
        
            
        """directory= "img/Christofides/"
        filename= "Christofides_Map_" + str(i) + ".jpg"

        plt.savefig(directory+filename)
        i += 1"""
    directory= "img/Christofides/"
    filename= "Christofides_Map.jpg" 
    plt.savefig(directory+filename)
    plt.close(figC)

def draw_multigraph(christofides_graph_no_recharge, dizionario_citta, Max_Axis):
    """keys= list(christofides_graph_no_recharge.keys())
    for key in keys:
        print(str(key) + ": " + str(christofides_graph_no_recharge.get(int(key))))"""

    # -------------------- Creo SubPlot --------------------
    figC= plt.figure()
    # -------------------- INIZIALIZZO GRAFICO --------------------

    plt.title('MultiGraph Cities-Map')
    plt.grid(True)

    # Do valori agli assi cartesiani
    plt.axis([-Max_Axis-1, Max_Axis+1, -Max_Axis-1, Max_Axis+1])

    plt.xticks([1*k for k in range(-Max_Axis,Max_Axis+1)])
    plt.yticks([1*k for k in range(-Max_Axis,Max_Axis+1)])
    # Creo i 4 quadranti disegnando semplicemente la retta verticale e la retta orizzontale
    plt.axvline(0,0,color='black')

    plt.axhline(0,0,color='black')

    x_city_coordinates=[]
    y_city_coordinates=[]

    #-------------------- Disegno i punti --------------------

    cities= list(dizionario_citta.keys())
    cities.append(0)

    for key in cities:
        if key == 0:
            x_city_coordinates.append(0)
            y_city_coordinates.append(0)
        else:
            cliente= dizionario_citta.get(key)
            x_city_coordinates.append(cliente.coordinate[0])
            y_city_coordinates.append(cliente.coordinate[1])

    plt.scatter(x_city_coordinates, y_city_coordinates, s=20, edgecolors='none', c='green', label="Cliente")
    # Do i nomi ai punti
    i = 0
    for key in cities:
        plt.annotate(str(key), (x_city_coordinates[i],y_city_coordinates[i]))
        i += 1

    plt.savefig('img/Christofides/MultiGraph.jpg')


    #-------------------- Disegno semirette --------------------

    i = 0
    for vertex in cities:
        edge_v= christofides_graph_no_recharge.get(int(vertex))
        nodes_u= list(edge_v.keys())

        for u in nodes_u:
            if vertex != 0:
                nodo_1= dizionario_citta.get(int(vertex))
                coordinate1= nodo_1.coordinate
            else:
                coordinate1= [0,0]

            if u != 0:
                nodo_2= dizionario_citta.get(int(u))
                coordinate2= nodo_2.coordinate
            else:
                coordinate2= [0,0]
        
            plt.plot([coordinate1[0],coordinate2[0]],[coordinate1[1],coordinate2[1]], color='green')
        
            
        """directory= "img/Christofides/"
        filename= "Christofides_Map_" + str(i) + ".jpg"

        plt.savefig(directory+filename)
        i += 1"""
    directory= "img/Christofides/"
    filename= "MultiGraph.jpg" 
    plt.savefig(directory+filename)
    plt.close(figC)

def draw_Christofides_green(christofides_graph, dizionario_citta, dizionario_stazioni, Max_Axis):
    # -------------------- Creo SubPlot --------------------
    figCG= plt.figure() 
    # -------------------- INIZIALIZZO GRAFICO --------------------
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

    # --------------------- Disegno Righe ----------------------------------
    cities= list(dizionario_citta.keys())
    cities.append(0)

    # i = 0
    for vertex in cities:

        edge_v= christofides_graph.get(int(vertex))

        nodes_u= list(edge_v.keys())

        for u in nodes_u:
 
            if vertex != 0:
                nodo_1= dizionario_citta.get(int(vertex))
                coordinate1= nodo_1.coordinate
            else:
                coordinate1= [0,0]

            if u != 0:
                if 'S' in str(u):
                    #print("Dentro Plot Generator")
                    #print("u: " + str(u))
                    key = u.replace('S','')
                    coordinate2= dizionario_stazioni.get(int(key))
                else:
                    nodo_2= dizionario_citta.get(int(u))
                    coordinate2= nodo_2.coordinate
            else:
                coordinate2= [0,0]

            if 'S' in str(u):
                plt.plot([coordinate1[0],coordinate2[0]],[coordinate1[1],coordinate2[1]], color='blue')
            else:
                plt.plot([coordinate1[0],coordinate2[0]],[coordinate1[1],coordinate2[1]], color='green')

    

    directory= "img/Christofides/"
    filename= "Christofides_Green_Map.jpg" 
    plt.savefig(directory+filename)
    plt.close(figCG)




def print_2_opt_arc_selected(percorso, archi_selezionati, dizionario_citta, dizionario_stazioni, Max_Axis):
    # -------------------- Creo SubPlot --------------------
    figLSAS= plt.figure() 
    # -------------------- INIZIALIZZO GRAFICO --------------------
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

    
    # --------------------- Disegno Righe ----------------------------------
    i= 0
    lunghezza_percorso= len(percorso)
    while i < lunghezza_percorso - 1:
        vertex1= percorso[i]

        if 'S' in str(vertex1):
            coordinate_vertex1= dizionario_stazioni.get(int(vertex1.replace('S','')))        
        elif vertex1 == 0:
            coordinate_vertex1= [0,0]
        else:
            coordinate1= dizionario_citta.get(int(vertex1))
            coordinate_vertex1= coordinate1.coordinate

        vertex2= percorso[i+1]

        if 'S' in str(vertex2):
            coordinate_vertex2= dizionario_stazioni.get(int(vertex2.replace('S','')))
       
        elif vertex2 == 0:
            coordinate_vertex2= [0,0]
        else:
            coordinate2= dizionario_citta.get(int(vertex2))
            coordinate_vertex2= coordinate2.coordinate 

        if [vertex1,vertex2] in archi_selezionati:
            plt.plot([coordinate_vertex1[0],coordinate_vertex2[0]],[coordinate_vertex1[1],coordinate_vertex2[1]], color='red')
        else:
            plt.plot([coordinate_vertex1[0],coordinate_vertex2[0]],[coordinate_vertex1[1],coordinate_vertex2[1]], color='green')
        i += 1
    
    directory= "img/"
    filename= "LS_Archi_Selezionati.jpg" 
    plt.savefig(directory+filename)
    plt.close(figLSAS)


def print_2_opt(percorso, dizionario_citta, dizionario_stazioni, Max_Axis):
    # -------------------- Creo SubPlot --------------------
    figLS= plt.figure() 
    # -------------------- INIZIALIZZO GRAFICO --------------------
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

    
    # --------------------- Disegno Righe ----------------------------------
    i= 0
    lunghezza_percorso= len(percorso)
    while i < lunghezza_percorso - 1:
        vertex1= percorso[i]

        if 'S' in str(vertex1):
            coordinate_vertex1= dizionario_stazioni.get(int(vertex1.replace('S','')))           
        elif vertex1 == 0:
            coordinate_vertex1= [0,0]
        else:
            coordinate1= dizionario_citta.get(int(vertex1))
            coordinate_vertex1= coordinate1.coordinate

        vertex2= percorso[i+1]

        if 'S' in str(vertex2):
            coordinate_vertex2= dizionario_stazioni.get(int(vertex2.replace('S','')))
        elif vertex2 == 0:
            coordinate_vertex2= [0,0]
        else:
            coordinate2= dizionario_citta.get(int(vertex2))
            coordinate_vertex2= coordinate2.coordinate 

        plt.plot([coordinate_vertex1[0],coordinate_vertex2[0]],[coordinate_vertex1[1],coordinate_vertex2[1]], color='green')
        i += 1
    directory= "img/"
    filename= "LocalSearch.jpg" 
    plt.savefig(directory+filename)
    plt.close(figLS)
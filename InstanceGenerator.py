import random


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
        coordinate_citta= []

        x= random.randint(-Max_Axis,Max_Axis)
        y= random.randint(-Max_Axis,Max_Axis)

        coordinate_citta.append(x)
        coordinate_citta.append(y)

        dizionario_citta[n]= coordinate_citta

    return dizionario_citta, dizionario_stazioni




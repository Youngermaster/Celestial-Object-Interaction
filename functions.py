# Importamos las bibliotecas necesarias.
import numpy as np
import matplotlib.pyplot as plt
import random

# Guardamos las variables de un cuerpo en unas listas.
posiciones = []
velocidades = []
aceleraciones = []
masas = []

"""
    Este método pide los datos al usuario y retorna 
    la peticion dependiendo del tipo de dato que 
    nosotros necesitemos.
"""
def pedir_datos(texto, tipo):
    peticion = input(texto)
    if tipo == "string":
        return peticion
    elif tipo == "int":
        return int(peticion)
    elif tipo == "float":
        return float(peticion)
    else:
        return "Tipo no reconocido"

"""
    Este método retorna un valor aleatorio en el rango 
    que nosotros necesitemos.
"""
def valor_aleatorio(minimo, maximo):
    return random.uniform(minimo, maximo)


"""
    Este método genera y guarda valores (aleatorios) en 
    las diferentes listas de las variables de un Cuerpo.
"""
def generador_de_cuerpos(cantidadDeCuerpos):
    MINIMO = -100
    MAXIMO = 100

    for iterador in range(cantidadDeCuerpos):
        # Creamos los valores aleatorios
        posicion = np.array([valor_aleatorio(MINIMO, MAXIMO), valor_aleatorio(MINIMO, MAXIMO)])
        velocidad = np.array([valor_aleatorio(MINIMO, MAXIMO), valor_aleatorio(MINIMO, MAXIMO)])
        aceleracion = np.array([valor_aleatorio(MINIMO, MAXIMO), valor_aleatorio(MINIMO, MAXIMO)])
        # En el caso de la masa no usamos el valor mínimo debido a que
        # no debemos tener una masa negativa.
        masa = valor_aleatorio(0, MAXIMO)

        # Añadimos las variables a las diferentes listas
        posiciones.append(posicion)
        velocidades.append(velocidad)
        aceleraciones.append(aceleracion)
        masas.append(masa)


"""
    Retorna las posiciones de los diferentes cuerpos.
"""
def obtener_posicion_de_cuerpos():
    return posiciones


"""
    Esta función se encarga de varias tareas, entre ellas:

    - Pedir los datos necesarios para gráficar.
    - Crear los gráficos con la líbreria `matplotlib`.
    - Graficar los cuerpos en diferentes momentos de 'tiempo' (las iteraciones que deseemos).

    Nota: Por buenas prácticas de programación, en este caso, SOLID, la S se refiere a
          Single responsability, nos dice que una función debe tener una sola tarea,
          como lo hemos hecho con todas la demás funciones anteriores, sin embargo, por
          casos prácticos se han juntado estas tres tareas.
"""
def core():
    cantidadDeCuerpos = pedir_datos("¿Cuántos cuerpos deseas?\n", "int")
    LIMITE_DE_GRAFICACION = pedir_datos("Dame una escala de graficación, por favor\n", "float")
    generador_de_cuerpos(cantidadDeCuerpos)
    
    CONSTANTE_G = 0.4  # 0.4<CONSTANTE_G<0.5
    DELTA_T = 0.01
    posi = np.array(obtener_posicion_de_cuerpos())
    iteraciones = 0 

    # Instante inicial 
    plt.close()
    fig, ax= plt.subplots()  

    # Modificamos las etiquetas de los ejes X y Y.
    plt.xlabel("Eje X", fontsize=10)
    plt.ylabel("Eje Y", fontsize=10)

    # Mi grafica tendra un eje coordenado que se define como 'ax' y
    # grafica los cuerpos mostrándolos todos en la posicion X con [:,0]
    # y en la posicion Y [:,1]
    cuerpo, = ax.plot(np.array(posi)[:, 0], np.array(posi)[:, 1], 'go')
    
    # Definimos el tamaño del recuadro en el que queremos que aparezcan
    # nuestros Cuerpos cogiendo nuestra posición más lejana y
    # restándole la más cercana al punto (0, 0)
    inx = max(np.array(posi)[:,0])-min(np.array(posi)[:,0])
    iny = max(np.array(posi)[:,1])-min(np.array(posi)[:,1])  


    # Definimos los limites de graficacion.
    
    ax.set_xlim(min(np.array(posi)[:,0])-inx*LIMITE_DE_GRAFICACION,max(np.array(posi)[:,0])+inx*LIMITE_DE_GRAFICACION)
    ax.set_ylim(min(np.array(posi)[:,1])-iny*LIMITE_DE_GRAFICACION, max(np.array(posi)[:,1])+iny*LIMITE_DE_GRAFICACION)

    masas[0] = 5000000
    while iteraciones < 400:
        # En el siguiente código lo que hacemos es comparar cada cuerpo
        # con todos los demás.
        for i in range(len(posiciones)):
            posicionesAuxiliar = posiciones.copy()
            aceleracionesAuxiliar = aceleraciones.copy()
            masasAuxiliar = masas.copy()

            posicionesAuxiliar.pop(i)
            aceleracionesAuxiliar.pop(i)
            masasAuxiliar.pop(i)

            for otro_cuerpo in range(len(posicionesAuxiliar)):
                dj = posicionesAuxiliar[otro_cuerpo] - posiciones[i]
                ndj = np.linalg.norm(dj) #Norma del vector entre la interaccion con cada cuerpo"""

                term = CONSTANTE_G * masasAuxiliar[otro_cuerpo] * dj / ((ndj)**3.0)
                aceleraciones[i] = aceleraciones[i] + term

        # Actualizamos las posiciones de todos los cuerpos
        # dependiendo de su interacción.
        for cuerpo_actual in range(len(posiciones)):
            posiciones[cuerpo_actual] = posiciones[cuerpo_actual] + velocidades[cuerpo_actual] * DELTA_T + 0.5 *aceleraciones[cuerpo_actual]*DELTA_T**2
        
        # Actualizamos la variable posi, con los nuevos valores de las posiciones.
        posi = np.array(obtener_posicion_de_cuerpos())

        # Gráficamos los cuerpos y su trayectoria
        trayectoria, = ax.plot(np.array(posi)[:, 0], np.array(posi)[:, 1], 'bo')#, markersize = 20)
        cuerpo.set_data(posi[:,0],posi[:,1])
        cuerpo, = ax.plot(np.array(posi)[:,0], np.array(posi)[:,1], 'ro')#, markersize = )

        titulo = "N-bodysim\nTiempo:" + str(iteraciones)
        plt.title(titulo, fontsize=19)
        plt.pause(0.01)
        iteraciones += 1

    plt.show()

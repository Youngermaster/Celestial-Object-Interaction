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
    Una prueba 
def movimiento_uniformemente_acelerado(velocidadFinal, velocidadInicial, aceleracion, tiempo):
    velocidadFinal = velocidadInicial + (aceleracion * tiempo)
"""

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
def core(logger, trayectoria):
    cantidadDeCuerpos = pedir_datos("¿Cuántos cuerpos deseas?\n", "int")
    LIMITE_DE_GRAFICACION = pedir_datos("Dame una escala de graficación, por favor\n", "float")
    generador_de_cuerpos(cantidadDeCuerpos)
    
    CONSTANTE_GRAVITACIONAL = 0.4  # 0.4<CONSTANTE_GRAVITACIONAL<0.5
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
    
    # Definimos el tamaño del recuadro en el que queremos que aparezcan
    # nuestros Cuerpos cogiendo nuestra posición más lejana y
    # restándole la más cercana al punto (0, 0)
    inx = max(np.array(posi)[:,0])-min(np.array(posi)[:,0])
    iny = max(np.array(posi)[:,1])-min(np.array(posi)[:,1])  

    cuerpo, = ax.plot(np.array(posi)[:,0], np.array(posi)[:,1], 'mo')
    # Definimos los limites de graficacion.
    
    ax.set_xlim(min(np.array(posi)[:,0])-inx*LIMITE_DE_GRAFICACION,max(np.array(posi)[:,0])+inx*LIMITE_DE_GRAFICACION)
    ax.set_ylim(min(np.array(posi)[:,1])-iny*LIMITE_DE_GRAFICACION, max(np.array(posi)[:,1])+iny*LIMITE_DE_GRAFICACION)

    if logger:
        print("Posiciones inicial:\n")
        print(posiciones)
        print("Velocidades inicial:\n")
        print(velocidades)

    masas[0] = 500
    while iteraciones < 100:
        # En el siguiente código lo que hacemos es comparar cada cuerpo
        # con todos los demás.
        for i in range(len(posiciones)):
            posicionesAuxiliar = posiciones.copy()
            aceleracionesAuxiliar = aceleraciones.copy()
            masasAuxiliar = masas.copy()

            posicionesAuxiliar.pop(i)# [1, 2, 3, 4]
            aceleracionesAuxiliar.pop(i)
            masasAuxiliar.pop(i)

            for otro_cuerpo in range(len(posicionesAuxiliar)):
                distancia = posicionesAuxiliar[otro_cuerpo] - posiciones[i]
                normaDeDistancia = np.linalg.norm(distancia) # Norma del vector entre la interaccion con cada cuerpo

                term = CONSTANTE_GRAVITACIONAL * masasAuxiliar[otro_cuerpo] * masas[i] * distancia / ((normaDeDistancia)**3.0)
                aceleraciones[i] += term
                if logger:
                    print("\nFuerzas Cuerpo ", otro_cuerpo, ": ")
                    print(term, "\n")

        # Actualizamos las posiciones de todos los cuerpos
        # dependiendo de su interacción.
        for cuerpo_actual in range(len(posiciones)):
            posiciones[cuerpo_actual] += velocidades[cuerpo_actual] * DELTA_T + 0.5 *aceleraciones[cuerpo_actual]*DELTA_T**2
            velocidades[cuerpo_actual] += (aceleraciones[cuerpo_actual] * DELTA_T)

        # Actualizamos la variable posi, con los nuevos valores de las posiciones.
        posi = np.array(obtener_posicion_de_cuerpos())
        # Gráficamos los cuerpos y su trayectoria

        # Trayectoria
        if trayectoria:
            trayectoria, = ax.plot(np.array(posi)[:, 0], np.array(posi)[:, 1], 'co')
            cuerpo.set_data(posi[:,0],posi[:,1])
            cuerpo, = ax.plot(np.array(posi)[:,0], np.array(posi)[:,1], 'mo')
        else:
            cuerpo.set_data(posi[:,0],posi[:,1])

        titulo = "N-bodysim\nTiempo:" + str(iteraciones)
        plt.title(titulo, fontsize=19)
        plt.pause(0.01)
        iteraciones += 1

    if logger:
        print("\nPosiciones final:\n")
        print(posiciones)
        print("\nVelocidades final:\n")
        print(velocidades)
        
    plt.show()

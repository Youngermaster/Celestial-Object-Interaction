# importamos bibliotecas
import numpy as np
import matplotlib.pyplot as plt
import random

# definicion clases de cuerpos

class cuerpo:    
    def __init__(self, pos, vel, acel, masa):
        self.pos = np.array(pos)
        self.vel = np.array(vel)
        self.acel = np.array(acel)
        self.masa = np.array(masa)

posiciones = []
velocidades = []
aceleraciones = []
masas = []

"""
    Este método pide los datos al usuario y retorna la cantidad.
"""
def pedir_datos(texto):
    peticion = input(texto)
    return int(peticion)


"""
    Este método retorna un valor aleatorio en el rango que nosotros deseemos
"""
def valor_aleatorio(minimo, maximo):
    return random.uniform(minimo, maximo)


"""
    Este método genera y retorna una lista de objetos tipo Cuerpo
"""
def generador_de_cuerpos(cantidadDeCuerpos):
    minimo = -100
    maximo = 100
    listaDeCuerpos = []

    for iterador in range(cantidadDeCuerpos):
        posicion = np.array([valor_aleatorio(minimo, maximo), valor_aleatorio(minimo, maximo)])
        velocidad = np.array([valor_aleatorio(minimo, maximo), valor_aleatorio(minimo, maximo)])
        aceleracion = np.array([valor_aleatorio(minimo, maximo), valor_aleatorio(minimo, maximo)])
        masa = valor_aleatorio(0, 30)
        cuerpo(posicion, velocidad, aceleracion, masa)

        posiciones.append(posicion)
        velocidades.append(velocidad)
        aceleraciones.append(aceleracion)
        masas.append(masa)
        listaDeCuerpos.append(cuerpo)
    return listaDeCuerpos


"""
    Retorna las posiciones de los diferentes cuerpos.
"""
def obtener_posicion_de_cuerpos():
    return posiciones


"""
    Ejecuta todo.
"""
def core():
    cantidadDeCuerpos = pedir_datos("¿Cuántos cuerpos deseas?\n")
    LIMITE_DE_GRAFICACION = float(pedir_datos("Dame una escala de graficación, por favor\n"))
    cuerpos = generador_de_cuerpos(cantidadDeCuerpos)

    G=0.4  #0.4<G<0.5
    Dt=0.01
    
    posi = np.array(obtener_posicion_de_cuerpos())

    t=0 
    #Instante inicial 
    plt.close()
    fig, ax= plt.subplots()  

    # Set x axis label.
    plt.xlabel("Eje X", fontsize=10)

    # Set y axis label.
    plt.ylabel("Eje Y", fontsize=10)

    """Mi grafica tendra un eje coordenado que se define como ax""" 

    pl1,= ax.plot(np.array(posi)[:,0], np.array(posi)[:,1],'go')

    """con este codigo lo que quiero decir es: que en mi eje coordonado me
    grafique mis planetas mostrandomelos todos en la posicion x con [:,0]
    y en la posicion y [:,1]"""
    
    """definimos el recuadro en el que queremos que aparezcan nuestros planetas cogiendo nuestra posicion mas lejana y
    restandole la mas cercana al punto (0,0)"""                                                              
    inx = max(np.array(posi)[:,0])-min(np.array(posi)[:,0])
    iny = max(np.array(posi)[:,1])-min(np.array(posi)[:,1])  


    """Definimos limites de graficacion utilizando lo anterior planteado"""
    
    ax.set_xlim(min(np.array(posi)[:,0])-inx*LIMITE_DE_GRAFICACION,max(np.array(posi)[:,0])+inx*LIMITE_DE_GRAFICACION)   
    ax.set_ylim(min(np.array(posi)[:,1])-iny*LIMITE_DE_GRAFICACION, max(np.array(posi)[:,1])+iny*LIMITE_DE_GRAFICACION)                                                               
    masas[0] = 5000000
    while t<400:
        for i in range(len(cuerpos)):
            posicionesAuxiliar = posiciones.copy()
            aceleracionesAuxiliar = aceleraciones.copy()
            masasAuxiliar = masas.copy()

            posicionesAuxiliar.pop(i)
            aceleracionesAuxiliar.pop(i)
            masasAuxiliar.pop(i)

            for otro_cuerpo in range(len(posicionesAuxiliar)):
                dj = posicionesAuxiliar[otro_cuerpo] - posiciones[i]
                ndj = np.linalg.norm(dj) #Norma del vector entre la interaccion con cada cuerpo"""

                term = G * masasAuxiliar[otro_cuerpo] * dj / ((ndj)**3.0)
                aceleraciones[i] = aceleraciones[i] + term
              
        for cuerpo_actual in range(len(cuerpos)):
            posiciones[cuerpo_actual] = posiciones[cuerpo_actual] + velocidades[cuerpo_actual] * Dt + 0.5 *aceleraciones[cuerpo_actual]*Dt**2
            
        posi = np.array(obtener_posicion_de_cuerpos()) #necesario de modificar +1
        pl2,= ax.plot(np.array(posi)[:,0], np.array(posi)[:,1],'bo')
        pl1.set_data(posi[:,0],posi[:,1])
        pl1,= ax.plot(np.array(posi)[:,0], np.array(posi)[:,1],'ro')
        #Para cada cuerpo me mostrara una "linea"
        string = "N-bodysim\nTiempo:" + str(t)
        plt.title(string, fontsize=19)
        plt.pause(0.01)
        t += 1

    plt.show()

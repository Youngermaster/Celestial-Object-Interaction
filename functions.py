import numpy as np
import matplotlib.pyplot as plt
import random

positions = []
velocities = []
acelerations = []
masses = []

def get_data(text, type):
    request = input(text)
    if type == "string":
        return request
    elif type == "int":
        return int(request)
    elif type == "float":
        return float(request)
    else:
        return "[ERROR] Type not recognized."


def get_random_number(MIN, MAX):
    return random.uniform(MIN, MAX)


def body_generator(bodyQuantity):
    MIN = -100
    MAX = 100

    for iterator in range(bodyQuantity):
        # Creamos los valores aleatorios
        position = np.array([get_random_number(MIN, MAX), get_random_number(MIN, MAX)])
        velocity = np.array([get_random_number(MIN, MAX), get_random_number(MIN, MAX)])
        aceleration = np.array([get_random_number(MIN, MAX), get_random_number(MIN, MAX)])
        # ! In the mass case we don't use `MIN` value because we can't
        # ! have a negative mass.
        mass = get_random_number(0, MAX)

        positions.append(position)
        velocities.append(velocity)
        acelerations.append(aceleration)
        masses.append(mass)


def get_body_position():
    return positions


def core(logger, trayectory):
    bodyQuantity = get_data("How many bodies do you want?\n", "int")
    GRAPHICATION_LIMIT = get_data("Give me a graphication scale, please\n", "float")
    body_generator(bodyQuantity)
    
    GRAVITATIONAL_CONSTANT = 0.4
    DELTA_T = 0.01
    posi = np.array(get_body_position())
    iterations = 0 

    plt.close()
    fig, ax = plt.subplots()  

    plt.xlabel("X axis", fontsize=10)
    plt.ylabel("Y axis", fontsize=10)

    inx = max(np.array(posi)[:,0])-min(np.array(posi)[:,0])
    iny = max(np.array(posi)[:,1])-min(np.array(posi)[:,1])  

    body, = ax.plot(np.array(posi)[:,0], np.array(posi)[:,1], 'mo')
    
    ax.set_xlim(min(np.array(posi)[:,0])-inx*GRAPHICATION_LIMIT,max(np.array(posi)[:,0])+inx*GRAPHICATION_LIMIT)
    ax.set_ylim(min(np.array(posi)[:,1])-iny*GRAPHICATION_LIMIT, max(np.array(posi)[:,1])+iny*GRAPHICATION_LIMIT)

    if logger:
        print("Initial positions:\n")
        print(positions)
        print("Initial velocity:\n")
        print(velocities)

    masses[0] = 500
    positions[0] = np.array([0.0, 0.0])
    while iterations < 100:
        for i in range(len(positions)):
            positionsAuxiliary = positions.copy()
            acelerationsAuxiliary = acelerations.copy()
            massesAuxiliary = masses.copy()

            positionsAuxiliary.pop(i)
            acelerationsAuxiliary.pop(i)
            massesAuxiliary.pop(i)

            for anotherBody in range(len(positionsAuxiliary)):
                distance = positionsAuxiliary[anotherBody] - positions[i]
                distanceNorm = np.linalg.norm(distance)

                term = GRAVITATIONAL_CONSTANT * massesAuxiliary[anotherBody] * masses[i] * distance / ((distanceNorm)**3.0)
                acelerations[i] += term
                if logger:
                    print("\nBody force ", anotherBody, ": ")
                    print(term, "\n")

        for body_actual in range(len(positions)):
            positions[body_actual] += velocities[body_actual] * DELTA_T + 0.5 *acelerations[body_actual]*DELTA_T**2
            velocities[body_actual] += (acelerations[body_actual] * DELTA_T)

        posi = np.array(get_body_position())
        
        if trayectory:
            trayectory, = ax.plot(np.array(posi)[:, 0], np.array(posi)[:, 1], 'co')
            body.set_data(posi[:,0],posi[:,1])
            body, = ax.plot(np.array(posi)[:,0], np.array(posi)[:,1], 'mo')
        else:
            body.set_data(posi[:,0],posi[:,1])

        title = "N-bodies simulator\nTime:" + str(iterations)
        plt.title(title, fontsize=19)
        plt.pause(0.01)
        iterations += 1

    if logger:
        print("\nFinal positions:\n")
        print(positions)
        print("\nFinal velocities:\n")
        print(velocities)
        
    plt.show()

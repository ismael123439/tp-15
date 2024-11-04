import py5
import random
import time

# Configuración inicial de datos y variables
data = []
delay = 0.1  # Velocidad de animación en segundos
sorting = False
current_alg = 'bubble'  # Algoritmo a usar ('bubble' o 'quick')

def setup():
    py5.size(800, 400)
    reset_data()
    py5.no_loop()

def draw():
    py5.background(240)
    # Dibujamos cada valor como un rectángulo
    for i, value in enumerate(data):
        x = i * (py5.width / len(data))
        # Color basado en el valor
        py5.fill(100, 100, 250 - value)
        py5.rect(x, py5.height - value, py5.width / len(data) - 2, value)

def reset_data():
    global data, sorting
    data = [random.randint(10, py5.height - 10) for _ in range(50)]
    sorting = False
    py5.redraw()

def bubble_sort_step():
    # Implementación paso a paso de Bubble Sort
    for i in range(len(data) - 1):
        for j in range(len(data) - 1 - i):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                highlight(j, j + 1)
                yield True  # Pausa para la animación
    yield False  # Señal de que terminó la ordenación

def quick_sort_step(low, high):
    # Implementación de Quick Sort con paso a paso
    if low < high:
        pi = partition(low, high)
        yield from quick_sort_step(low, pi - 1)
        yield from quick_sort_step(pi + 1, high)
    yield False  # Terminó la ordenación

def partition(low, high):
    pivot = data[high]
    i = low - 1
    for j in range(low, high):
        if data[j] <= pivot:
            i += 1
            data[i], data[j] = data[j], data[i]
            highlight(i, j)
            yield True
    data[i + 1], data[high] = data[high], data[i + 1]
    highlight(i + 1, high)
    yield True
    return i + 1

def highlight(idx1, idx2):
    # Destacar los elementos que están siendo comparados
    py5.fill(255, 0, 0)
    py5.rect(idx1 * (py5.width / len(data)), py5.height - data[idx1], py5.width / len(data) - 2, data[idx1])
    py5.rect(idx2 * (py5.width / len(data)), py5.height - data[idx2], py5.width / len(data) - 2, data[idx2])
    py5.redraw()
    time.sleep(delay)

def start_sorting():
    global sorting, current_algorithm
    sorting = True
    if current_alg == 'bubble':
        py5.thread(bubble_sort_step())
    elif current_alg == 'quick':
        py5.thread(quick_sort_step(0, len(data) - 1))

def stop_sorting():
    global sorting
    sorting = False
    py5.no_loop()

def set_algorithm(alg):
    global current_alg
    current_alg = alg
    reset_data()

def increase_speed():
    global delay
    delay = max(0.01, delay - 0.01)  # Incrementa la velocidad

def decrease_speed():
    global delay
    delay += 0.01  # Disminuye la velocidad

# Controles interactivos en Py5
def key_pressed():
    if py5.key == 'r':  # Reiniciar
        reset_data()
    elif py5.key == 's':  # Iniciar
        start_sorting()
    elif py5.key == 'p':  # Pausar
        stop_sorting()
    elif py5.key == '+':  # Aumentar velocidad
        increase_speed()
    elif py5.key == '-':  # Disminuir velocidad
        decrease_speed()
    elif py5.key == 'b':  # Bubble Sort
        set_algorithm('bubble')
    elif py5.key == 'q':  # Quick Sort
        set_algorithm('quick')

py5.run_sketch()

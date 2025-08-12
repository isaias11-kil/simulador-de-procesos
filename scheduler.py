# version 1
import time


class Proceso:
    """Clase para representar un proceso simple."""
    def __init__(self, pid, nombre, duracion):
        self.pid = pid
        self.nombre = nombre
        self.duracion = duracion
        self.tiempo_restante = duracion
    
    def __repr__(self):
        return f"Proceso(PID: {self.pid}, Nombre: {self.nombre}, Duración: {self.duracion})"

def agregar_proceso_a_cola(cola_procesos, proceso):
    """
    Agrega un nuevo proceso a la lista de procesos listos.
    """
    print(f"[{time.strftime('%H:%M:%S')}] Agregando {proceso.nombre} (Duración: {proceso.duracion}s) a la cola.")
    cola_procesos.append(proceso)

def planificar_proceso_sjf(cola_procesos):
    """
    Implementa la lógica del planificador SJF (Shortest Job First)
    utilizando una lista.
    """
    if not cola_procesos:
        print(f"[{time.strftime('%H:%M:%S')}] Cola de procesos vacía. El planificador está inactivo.")
        return None

    # Encontramos el índice del proceso con la duración más corta
    indice_sjf = 0
    duracion_minima = cola_procesos[0].duracion
    for i in range(1, len(cola_procesos)):
        if cola_procesos[i].duracion < duracion_minima:
            duracion_minima = cola_procesos[i].duracion
            indice_sjf = i

    # Ahora esto funciona porque `list.pop()` acepta un índice
    proceso_a_ejecutar = cola_procesos.pop(indice_sjf)
    print(f"[{time.strftime('%H:%M:%S')}] Planificador SJF seleccionó a {proceso_a_ejecutar.nombre}.")
    return proceso_a_ejecutar

def ejecutar_proceso(proceso):
    """
    Simula la ejecución de un proceso hasta que termina.
    """
    if proceso:
        print(f"[{time.strftime('%H:%M:%S')}] Ejecutando {proceso.nombre} (PID: {proceso.pid}).")
        
        while proceso.tiempo_restante > 0:
            print(f"[{time.strftime('%H:%M:%S')}] {proceso.nombre} - Tiempo restante: {proceso.tiempo_restante}s.")
            time.sleep(1)
            proceso.tiempo_restante -= 1
        
        print(f"[{time.strftime('%H:%M:%S')}] {proceso.nombre} ha terminado su ejecución.")
    return None

def main():
    """
    Función principal que simula el ciclo del planificador SJF.
    """
    # Usamos una lista en lugar de deque
    cola_procesos_listos = []
    
    print("--- Simulador de Planificador SJF Iniciado ---")
    
    agregar_proceso_a_cola(cola_procesos_listos, Proceso(1, "Proceso_A", 5))
    agregar_proceso_a_cola(cola_procesos_listos, Proceso(2, "Proceso_B", 2))
    agregar_proceso_a_cola(cola_procesos_listos, Proceso(3, "Proceso_C", 8))
    
    
    time.sleep(2)
    print("-" * 40)

    while cola_procesos_listos:
        proceso_a_ejecutar = planificar_proceso_sjf(cola_procesos_listos)
        
        if proceso_a_ejecutar:
            ejecutar_proceso(proceso_a_ejecutar)
            print("-" * 40)
            
    print("--- Todos los procesos han sido completados. Saliendo. ---")

if __name__ == "__main__":
    main()

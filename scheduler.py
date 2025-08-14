# version 1.1
import time
import threading
from queue import Queue

class Proceso:
    def __init__(self, pid, nombre, memoria, duracion):
        self.pid = pid
        self.nombre = nombre
        self.memoria = memoria
        self.duracion = duracion
        self.tiempo_restante = duracion

    def __repr__(self):
        return f"Proceso(PID: {self.pid}, Nombre: {self.nombre}, Memoria: {self.memoria}MB, Duración: {self.duracion}s)"


class Scheduler:
    def __init__(self, gestor_memoria):
        self.gestor_memoria = gestor_memoria
        self.cola = Queue()
        self.procesos_activos = []
        self.ejecutando = False

    def agregar_proceso(self, proceso):
        self.cola.put(proceso)
        print(f"Proceso agregado: {proceso}")

    def planificar_sjf(self):
        if self.cola.empty():
            return None
        procesos = list(self.cola.queue)
        procesos.sort(key=lambda p: p.duracion)
        self.cola.queue.clear()
        for p in procesos[1:]:
            self.cola.put(p)
        return procesos[0]

    def ejecutar_proceso(self, proceso):
        self.procesos_activos.append(proceso)
        while proceso.tiempo_restante > 0 and self.ejecutando:
            time.sleep(1)
            proceso.tiempo_restante -= 1
        self.procesos_activos.remove(proceso)
        self.gestor_memoria.liberar(proceso.memoria)

    def iniciar(self):
        if not self.ejecutando:
            self.ejecutando = True
            threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        while self.ejecutando and not self.cola.empty():
            proceso = self.planificar_sjf()
            if proceso:
                self.ejecutar_proceso(proceso)

    def detener(self):
        self.ejecutando = False


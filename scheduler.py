# scheduler.py esto es un ejemplo solo para probar 
class Scheduler:
    def __init__(self, gestor_memoria):
        self.gestor_memoria = gestor_memoria
        self.procesos_activos = []
        self.procesos_espera = []

    def agregar_proceso(self, proceso):
        self.procesos_activos.append(proceso)

    def finalizar_proceso(self, proceso):
        self.procesos_activos.remove(proceso)

import time
from datetime import datetime
from enum import Enum

class EstadoProceso(Enum):
    No_iniciado = "no iniciado"
    Ejecutando = "ejecutando"
    EN_ESPERA = "pausado"
    Terminado = "terminado"
    Error = "error"

class Proceso:
    contador_ids = 0

    def __init__(self, nombre, descripcion="", pasos=None, memoria=0, duracion=0):
        Proceso.contador_ids += 1
        self.id = Proceso.contador_ids
        self.nombre = nombre
        self.descripcion = descripcion
        self.memoria = int(memoria)
        self.duracion = int(duracion)
        self.estado = EstadoProceso.No_iniciado
        self.fecha_creacion = datetime.now()
        self.fecha_actualizacion = datetime.now()
        self.pasos = pasos if pasos else []
        self.paso_actual = 0
        self.resultado = None

    def ejecutar(self):
        self.estado = EstadoProceso.Ejecutando
        self._touch()
        try:
            time.sleep(self.duracion)
            self.estado = EstadoProceso.Terminado
            self.resultado = "proceso completado exitosamente"
        except Exception as e:
            self.estado = EstadoProceso.Error
            self.resultado = str(e)
        finally:
            self._touch()
            return self.resultado

    def pausar(self):
        if self.estado == EstadoProceso.Ejecutando:
            self.estado = EstadoProceso.EN_ESPERA
            self._touch()
            return True
        return False

    def reanudar(self):
        if self.estado == EstadoProceso.EN_ESPERA:
            self.estado = EstadoProceso.Ejecutando
            self._touch()
            return True
        return False

    def reiniciar(self):
        self.estado = EstadoProceso.No_iniciado
        self.paso_actual = 0
        self.resultado = None
        self._touch()

    def _touch(self):
        self.fecha_actualizacion = datetime.now()

    def __str__(self):
        return (f"Proceso {self.id}: {self.nombre} | {self.descripcion} | "
                f"Mem {self.memoria}MB | Dur {self.duracion}s | Estado {self.estado.value}")

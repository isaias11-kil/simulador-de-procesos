
import threading

class GestorMemoria:
    """Simula gestor de memoria RAM."""
    def __init__(self, total_memoria):
        self.total = int(total_memoria)
        self.usada = 0
        self._lock = threading.Lock()
        print(f"[GESTOR] Memoria total disponible: {self.total} MB.")

    def reservar(self, etiqueta_proceso, cantidad):
        """Intenta reservar 'cantidad' de MB. Retorna True/False."""
        cantidad = int(cantidad)
        with self._lock:
            if self.usada + cantidad <= self.total:
                self.usada += cantidad
                print(f"[GESTOR] +{cantidad}MB -> '{etiqueta_proceso}'. "
                      f"Uso: {self.usada}/{self.total} MB")
                return True
            else:
                print(f"[GESTOR] ❌ Sin memoria para '{etiqueta_proceso}' "
                      f"(pide {cantidad}MB, libres {self.total - self.usada}MB)")
                return False

    def liberar(self, cantidad):
        """Libera 'cantidad' de MB (con tope inferior 0)."""
        cantidad = int(cantidad)
        with self._lock:
            self.usada = max(0, self.usada - cantidad)
            print(f"[GESTOR] -{cantidad}MB liberados. "
                  f"Uso: {self.usada}/{self.total} MB")

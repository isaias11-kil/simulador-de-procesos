# gestor_memoria.py
# Ejemplo de gestión dinámica de memoria y liberación + clase GestorMemoria

import gc  # Módulo de recolección de basura

class GestorMemoria:
    """Simula un gestor de memoria manual."""
    def __init__(self, total_memoria):
        self.total = total_memoria
        self.usada = 0
        print(f"[GESTOR] Memoria total disponible: {self.total} unidades.")

    def reservar(self, proceso, cantidad):
        """Reserva memoria para un proceso si hay suficiente espacio."""
        if self.usada + cantidad <= self.total:
            self.usada += cantidad
            print(f"[GESTOR] Reservadas {cantidad} unidades para {proceso}. Memoria usada: {self.usada}/{self.total}")
            return True
        else:
            print(f"[GESTOR] Error: Memoria insuficiente para {proceso}.")
            return False

    def liberar(self, cantidad):
        """Libera memoria usada."""
        self.usada = max(0, self.usada - cantidad)
        print(f"[GESTOR] Liberadas {cantidad} unidades. Memoria usada: {self.usada}/{self.total}")

class Objeto:
    """Objeto que ocupa memoria simulada."""
    def __init__(self, nombre, memoria, gestor):
        self.nombre = nombre
        self.memoria = memoria
        self.gestor = gestor
        if self.gestor.reservar(nombre, memoria):
            print(f"[CREADO] Objeto '{self.nombre}' creado usando {self.memoria} unidades.")
        else:
            print(f"[ERROR] No se pudo crear el objeto '{self.nombre}' por falta de memoria.")

    def __del__(self):
        print(f"[ELIMINADO] Objeto '{self.nombre}' eliminado. Liberando {self.memoria} unidades.")
        self.gestor.liberar(self.memoria)

def crear_objetos(cantidad, gestor, memoria_por_objeto):
    """Crea una lista de objetos dinámicamente."""
    lista = []
    for i in range(1, cantidad + 1):
        lista.append(Objeto(f"Objeto-{i}", memoria_por_objeto, gestor))
    return lista

def liberar_memoria(lista):
    """Libera la memoria eliminando la lista y forzando el garbage collector."""
    print("\n[ACCION] Liberando memoria...")
    del lista
    gc.collect()
    print("[ACCION] Memoria liberada.\n")

if __name__ == "__main__":
    try:
        total_memoria = int(input("Ingrese la memoria total disponible: "))
        cantidad = int(input("Ingrese la cantidad de objetos a crear: "))
        memoria_por_objeto = int(input("Ingrese la memoria que ocupa cada objeto: "))
    except ValueError:
        print("⚠️ Debe ingresar valores numéricos enteros.")
        exit()

    # Crear gestor de memoria
    gestor = GestorMemoria(total_memoria)

    # Crear lista dinámica de objetos
    objetos = crear_objetos(cantidad, gestor, memoria_por_objeto)
    
    print("\n[INFO] Objetos creados en memoria.")
    input("Presione Enter para liberar memoria...")

    # Liberar memoria
    liberar_memoria(objetos)
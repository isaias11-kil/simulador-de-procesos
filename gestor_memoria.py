class GestorMemoria:
    def __init__(self, memoria_total):
        self.memoria_total = memoria_total
        self.memoria_disponible = memoria_total
        self.usada = 0  # memoria usada actualmente

    def reservar(self, proceso, memoria):
        if memoria <= self.memoria_disponible:
            self.memoria_disponible -= memoria
            self.usada += memoria
            print(f"[MEMORIA] Asignada {memoria} MB a {proceso.nombre}. Disponible: {self.memoria_disponible} MB")
            return True
        else:
            print(f"[MEMORIA] No hay suficiente memoria para {proceso.nombre}. Disponible: {self.memoria_disponible} MB")
            return False

    def liberar(self, memoria):
        self.memoria_disponible += memoria
        self.usada -= memoria
        print(f"[MEMORIA] Liberados {memoria} MB. Disponible: {self.memoria_disponible} MB")

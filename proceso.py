import random
import time
from datetime import datetime
from enum import Enum

class estadoProceso(Enum):
    No_iniciado = "no iniciado"
    Ejecutando = "ejecutando"
    EN_ESPERA = "pausado"
    Terminado = "terminado"
    Error = "error"

class Proceso:

    contador_ids = 0

    def __init__(self, nombre, descripcion="", pasos=None):
        Proceso.contador_ids +=1
        self.id = Proceso.contador_ids
        self.nombre = nombre
        self.descripcion = descripcion
        self.estado = estadoProceso.No_iniciado
        self.fecha_creacion = datetime.now()
        self.fecha_actualizacion = datetime.now()
        self.pasos = pasos if pasos else [] 
        self.paso_actual = 0
        self.resultado = None

    def agregar_paso(self, paso):
        self.pasos.append(paso)
        self.actualizar()

    def ejecutar(self):
        self.estado = estadoProceso.Ejecutando
        self.actualizar()

        try:
            for i, paso in enumerate(self.pasos):
                self.paso_actual = i + 1  # Actualiza el paso actual
                print(f"ejecutano paso {self.paso_actual}: {paso}")
                time.sleep(random.uniform(0.5,2)) 
                
                if random.random() < 0.1:
                    raise Exception(f"Error simulado en el paso {self.paso_actual}")
                
                self.estado = estadoProceso.Ejecutando
                self.resultado = "proceso completado exitosamente"

        except Exception as e:
            self.estado = estadoProceso.Error
            self.resultado = str(e)

        finally:
            self.actualizar()  # Corrige el nombre del método
            return self.resultado
        
    def pausar(self):
        if self.estado == estadoProceso.Ejecutando:
            self.estado = estadoProceso.EN_ESPERA
            self.actualizar()
            print(f"Proceso {self.nombre} pausado.")
            return True
        return False

    def reanudar(self):
        if self.estado == estadoProceso.EN_ESPERA:
            self.estado = estadoProceso.Ejecutando  
            self.actualizar()
            return True
        return False

    def reiniciar(self):
        self.estado = estadoProceso.No_iniciado
        self.paso_actual = 0
        self.resultado = None  # Corrige el nombre del atributo
        self.actualizar()

    def actualizar(self):
        self.fecha_actualizacion = datetime.now()

    def __str__ (self):
         return (f"Proceso {self.id}: {self.nombre}\n"
                f"Estado: {self.estado.value}\n"
                f"Pasos: {len(self.pasos)} | Paso actual: {self.paso_actual}\n"
                f"Creado: {self.fecha_creacion}\n"
                f"Actualizado: {self.fecha_actualizacion}\n"
                f"Resultado: {self.resultado or 'N/A'}")

class GENERADORPROCESOS:

    @staticmethod
    def generar_proceso():
        temas = ["Facturación", "Inventario", "Reportes", "Backup", "Sincronización"]
        acciones = ["Generar", "Validar", "Exportar", "Importar", "Procesar", "Analizar"]
        nombre_proceso = f"{random.choice(acciones)} de {random.choice(temas)}"
        num_pasos = random.randint(3, 8)
        
        pasos = []
        for i in range(num_pasos):
            pasos.append(f"Paso {i+1}: {random.choice(acciones)} {random.choice(['datos', 'archivos', 'registros'])}")
        
        return Proceso(nombre_proceso, f"Proceso generado automáticamente con {num_pasos} pasos", pasos)


if __name__ == "__main__":

    proceso_manual = Proceso("Proceso de Ejemplo", "Este es un proceso creado manualmente")
    proceso_manual.agregar_paso("Paso 1: Inicializar sistema")
    proceso_manual.agregar_paso("Paso 2: Cargar configuración")
    proceso_manual.agregar_paso("Paso 3: Ejecutar tarea principal")
    
    print("=== Proceso Manual ===")
    print(proceso_manual)
    print("\nEjecutando proceso manual...")
    resultado = proceso_manual.ejecutar()
    print(f"Resultado: {resultado}")
    print(proceso_manual)
    
    # Generar y ejecutar procesos automáticamente
    print("\n=== Procesos Automáticos ===")
    for _ in range(3):
        proceso_auto = GENERADORPROCESOS.generar_proceso()
        print("\n" + str(proceso_auto))
        print("\nEjecutando proceso automático...")
        resultado = proceso_auto.ejecutar()
        print(f"Resultado: {resultado}")
        print(proceso_auto)

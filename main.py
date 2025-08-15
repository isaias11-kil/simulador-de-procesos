
import tkinter as tk
from tkinter import ttk, messagebox
import threading

from gestor_memoria import GestorMemoria
from scheduler import Scheduler
from proceso import Proceso

# Inicializar componentes del sistema 
MEMORIA_TOTAL = 1024  # MB
gestor_memoria = GestorMemoria(MEMORIA_TOTAL)
planificador = Scheduler(gestor_memoria)
planificador.iniciar()

# Interfaz gráfica 
ventana = tk.Tk()
ventana.title("Simulador de Gestión de Procesos")
ventana.geometry("800x560")

#  Formulario de creación de procesos 
frame_form = tk.LabelFrame(ventana, text="Crear Proceso")
frame_form.pack(fill="x", padx=10, pady=8)

tk.Label(frame_form, text="Nombre:").grid(row=0, column=0, sticky="w", padx=4, pady=2)
entrada_nombre = tk.Entry(frame_form, width=28)
entrada_nombre.grid(row=0, column=1, padx=4, pady=2)

tk.Label(frame_form, text="Memoria (MB):").grid(row=1, column=0, sticky="w", padx=4, pady=2)
entrada_memoria = tk.Entry(frame_form, width=12)
entrada_memoria.grid(row=1, column=1, sticky="w", padx=4, pady=2)

tk.Label(frame_form, text="Duración (s):").grid(row=2, column=0, sticky="w", padx=4, pady=2)
entrada_duracion = tk.Entry(frame_form, width=12)
entrada_duracion.grid(row=2, column=1, sticky="w", padx=4, pady=2)

def crear_proceso():
    try:
        nombre = entrada_nombre.get().strip() or "Proceso sin nombre"
        memoria = int(entrada_memoria.get())
        duracion = int(entrada_duracion.get())

        if memoria <= 0 or duracion <= 0:
            raise ValueError

        descripcion = f"Memoria: {memoria}MB | Duración: {duracion}s"
        pasos = [f"Ejecutar {duracion}s", f"Consumir {memoria}MB"]
        proceso = Proceso(nombre, descripcion, pasos, memoria, duracion)

        planificador.agregar_proceso(proceso)
        actualizar_listas()

        entrada_nombre.delete(0, tk.END)
        entrada_memoria.delete(0, tk.END)
        entrada_duracion.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Datos inválidos", "Memoria y duración deben ser enteros positivos.")

tk.Button(frame_form, text="Agregar Proceso", command=crear_proceso)\
  .grid(row=3, column=0, columnspan=2, pady=6)

#  Estado de memoria 
frame_memoria = tk.Frame(ventana)
frame_memoria.pack(fill="x", padx=10, pady=8)

label_memoria = tk.Label(frame_memoria, text="Memoria usada: 0 / 1024 MB")
label_memoria.pack(side="left")

barra_memoria = ttk.Progressbar(frame_memoria, maximum=MEMORIA_TOTAL, length=360)
barra_memoria.pack(side="left", padx=10)

# Listados 
frame_listas = tk.Frame(ventana)
frame_listas.pack(fill="both", expand=True, padx=10, pady=8)

# Activos
frame_activos = tk.LabelFrame(frame_listas, text="Procesos en ejecución")
frame_activos.pack(side="left", fill="both", expand=True, padx=5)
lista_activos = tk.Listbox(frame_activos)
lista_activos.pack(fill="both", expand=True)

# Cola
frame_cola = tk.LabelFrame(frame_listas, text="Procesos en cola")
frame_cola.pack(side="right", fill="both", expand=True, padx=5)
lista_cola = tk.Listbox(frame_cola)
lista_cola.pack(fill="both", expand=True)

#  Actualizaciones GUI 
def actualizar_listas():
    lista_activos.delete(0, tk.END)
    for p in list(planificador.procesos_activos):
        lista_activos.insert(tk.END, f"{p.id} - {p.nombre} ({p.descripcion})")

    lista_cola.delete(0, tk.END)
    
    try:
        procesos_en_cola = list(planificador.cola.queue)
    except Exception:
        procesos_en_cola = []
    for p in procesos_en_cola:
        lista_cola.insert(tk.END, f"{p.id} - {p.nombre} ({p.descripcion})")

def actualizar_memoria_y_listas():
    barra_memoria["value"] = gestor_memoria.usada
    label_memoria.config(text=f"Memoria usada: {gestor_memoria.usada} / {gestor_memoria.total} MB")
    actualizar_listas()
    ventana.after(500, actualizar_memoria_y_listas)

actualizar_memoria_y_listas()

#  Salir 
def al_cerrar():
    planificador.detener()
    ventana.destroy()

ventana.protocol("WM_DELETE_WINDOW", al_cerrar)
ventana.mainloop()

from sched import scheduler
import tkinter as tk
from tkinter import ttk, messagebox
from proceso import Proceso
from gestor_memoria import GestorMemoria 
from scheduler import Scheduler
# inicializar componentes del sistema
memoria_total = 1024 # MB
gestor_memoria = GestorMemoria(memoria_total)
Scheduler = Scheduler(gestor_memoria)
# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Simulador de Gestión de Procesos")
ventana.geometry("700x500")
# Widgets UI
# Formulario de creación de procesos
frame_form = tk.LabelFrame(ventana, text="Crear Proceso")
frame_form.pack(fill="x", padx=10, pady=5)

tk.Label(frame_form, text="Nombre: ").grid(row=0, column=0)
entrada_nombre = tk.Entry(frame_form)
entrada_nombre.grid(row=0, column=1)

tk.Label(frame_form, text="Memoria (MB): ").grid(row=1, column=0)
entrada_memoria = tk.Entry(frame_form)
entrada_memoria.grid(row=1, column=1)

tk.Label(frame_form, text="Duración (segundos): ").grid(row=2, column=0)
entrada_duracion = tk.Entry(frame_form)
entrada_duracion.grid(row=2, column=1)

def crear_proceso():
    try:
        nombre = entrada_nombre.get()
        memoria = int(entrada_memoria.get())
        duracion = int(entrada_duracion.get())
        
        proceso = Proceso(nombre, memoria, duracion)
        
        scheduler.agregar_proceso(proceso)
        actualizar_listas()
        actualiza_barras()
        
        entrada_nombre.delete(0, tk.END)
        entrada_memoria.delete(0, tk.END)
        entrada_duracion.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Verifica que los campos numéricos estén correctos.")
        
tk.Button(frame_form, text="Agregar Proceso", command=crear_proceso).grid(row=3, columnspan=2, pady=5)
        
# Estado de memoria
frame_memoria = tk.Frame(ventana)
frame_memoria.pack(fill="x", padx=10, pady=5)
       
label_memoria = tk.Label(frame_memoria, text="Memoria usada: 0 MB")
label_memoria.pack(side="left")
        
barra_memoria = ttk.Progressbar(frame_memoria, maximum=memoria_total, length=300)
barra_memoria.pack(side="left", padx=10)
barra_memoria.pack(side="left", padx=10)
        
        # Listado de procesos activos y en cola 
frame_listas = tk.Frame(ventana)
frame_listas.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Procesos en ejecución
frame_activos = tk.LabelFrame(frame_listas, text="Procesos en ejecución")
frame_activos.pack(side="left",fill="both", expand=True, padx=5)
        
lista_activos = tk.Listbox(frame_activos)
lista_activos.pack(fill="both", expand=True)
        
        # Procesos en cola
frame_cola = tk.LabelFrame(frame_listas, text="Procesos en cola")
frame_cola.pack(side="right", fill="both", expand=True, padx=5)
        
lista_cola = tk.Listbox(frame_cola)
lista_cola.pack(fill="both", expand=True)
        
# Funciones para actualizar interfaz
        
def actualizar_listas():
    lista_activos.delete(0, tk.END)
    for p in scheduler.procesos_activos:
        lista_activos.insert(tk.END, f"{p.pid} - {p.nombre} ({p.memoria} MB)")

    lista_cola.delete(0, tk.END)
    for p in list(scheduler.cola.queue):
        lista_cola.insert(tk.END, f"{p.pid} - {p.nombre} ({p.memoria} MB)")
def actualiza_barras():
    usada = gestor_memoria.usada 
    barra_memoria["value"] = usada
    label_memoria.config(text=f"Memoria usada: {usada} MB")
    ventana.after(1000, actualiza_barras)
# iniciar interfaz y actualizaciones
actualiza_barras()
ventana.mainloop()
                        
        
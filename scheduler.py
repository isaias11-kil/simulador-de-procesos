
import time
import threading
from queue import Queue
from typing import List
from proceso import Proceso

class Scheduler:
    """
    Planificador con política SJF (Shortest Job First).
    Ejecuta múltiples procesos en paralelo si hay memoria suficiente.
    """
    def __init__(self, gestor_memoria):
        self.gestor_memoria = gestor_memoria
        self.cola = Queue()                # Cola de espera
        self.procesos_activos: List[Proceso] = []
        self._lock = threading.Lock()
        self._ejecutando = False
        self._hilo_loop = None

    def agregar_proceso(self, proceso: Proceso):
        """Encola un proceso y despierta el planificador."""
        self.cola.put(proceso)
        print(f"[SCHEDULER] Encolado: {proceso}")
        self._despertar()

    def iniciar(self):
        if not self._ejecutando:
            self._ejecutando = True
            self._hilo_loop = threading.Thread(target=self._loop, daemon=True)
            self._hilo_loop.start()
            print("[SCHEDULER] Iniciado.")

    def detener(self):
        self._ejecutando = False
        print("[SCHEDULER] Detenido.")

    def _despertar(self):
        # El loop se ejecuta continuamente
        pass

    def _loop(self):
        """Bucle principal: intenta despachar procesos cuando haya memoria."""
        while self._ejecutando:
            self._intentar_despachar()
            time.sleep(0.2)  # evita busy-wait intenso

    def _intentar_despachar(self):
        """Saca de la cola por SJF e intenta iniciar tantos como permita la RAM."""
        if self.cola.empty():
            return

        with self._lock:
            
            procesos = list(self.cola.queue)
            if not procesos:
                return

            # Ordenar por duración (SJF)
            procesos.sort(key=lambda p: p.duracion)

            # Limpiar la cola
            self.cola.queue.clear()

            pendientes = []
            for proc in procesos:
                # Si ya se está ejecutando, sáltalo 
                if proc in self.procesos_activos:
                    continue

                # Intentar reservar memoria
                if self.gestor_memoria.reservar(f"{proc.id}-{proc.nombre}", proc.memoria):
                    # Lanzar ejecución en un hilo
                    self.procesos_activos.append(proc)
                    hilo = threading.Thread(target=self._run_proceso, args=(proc,), daemon=True)
                    hilo.start()
                else:
                    # No alcanzó memoria: permanece pendiente
                    pendientes.append(proc)

            # Reencolar los que no pudieron iniciar
            for p in pendientes:
                self.cola.put(p)

    def _run_proceso(self, proceso: Proceso):
        """Ejecuta el proceso y libera recursos al terminar."""
        print(f"[SCHEDULER] ▶ Ejecutando: {proceso}")
        try:
            proceso.ejecutar()
        finally:
            # Al terminar, liberar memoria y retirar de activos
            self.gestor_memoria.liberar(proceso.memoria)
            with self._lock:
                if proceso in self.procesos_activos:
                    self.procesos_activos.remove(proceso)
            print(f"[SCHEDULER] ✅ Finalizado: {proceso}")
            # Intentar despachar otros que estaban esperando
            self._intentar_despachar()

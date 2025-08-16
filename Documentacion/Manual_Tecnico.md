# Manual Técnico

## Arquitectura
- **MemoryManager**: administra `total_mb`, `used_mb`, `allocate()`, `free()` con exclusión mutua (*lock*).
- **Scheduler (Round-Robin, 1 CPU)**:
  - Colas: `ready`, `waiting`, `finished`.
  - `quantum_sec = 1`. Toma el primero de `ready`, ejecuta 1s, decrementa `remaining`.
  - Si `remaining <= 0`: libera memoria y mueve procesos desde `waiting` si hay espacio.
- **Process (dataclass)**: `pid`, `name`, `mem_mb`, `total_seconds`, `remaining`.

## Concurrencia
- Hilo planificador (`daemon=True`), con `threading.Lock()` para consistencia.
- La GUI (Tkinter) refresca el estado con `on_update_callback` y timer `after(500ms)` para la gráfica.

## Decisiones de diseño
- Se simula **1 CPU** (no se ejecutan dos procesos a la vez).
- **Memoria dinámica**: si `allocate` falla, el proceso va a `waiting`.
- **Gráfica de RAM**: ventana temporal de 120s con `matplotlib` embebido en Tkinter.

## Extensiones futuras
- Prioridades, tamaños variables de quantum, IO-blocking, persistencia de procesos, exportar logs.

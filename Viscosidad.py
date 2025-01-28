import tkinter as tk

def calcular_aceleracion(f, m):
    """Calcula la aceleración dada la fuerza y la masa."""
    return [f[0] / m, f[1] / m]

def un_paso(v, f, t, m):
    """
    Realiza un paso de simulación para calcular el cambio en posición y velocidad.
    """
    # Calcular aceleración
    a = calcular_aceleracion(f, m)
    
    # Calcular velocidad final
    v_f = [v[0] + a[0] * t, v[1] + a[1] * t]
    
    # Calcular desplazamiento
    delta_pos = [
        v[0] * t + 0.5 * a[0] * t**2,
        v[1] * t + 0.5 * a[1] * t**2
    ]
    
    # Evitar que la velocidad sea demasiado pequeña
    v_f = [0 if abs(vel) < 1e-5 else vel for vel in v_f]
    
    return delta_pos, v_f

def acumula_pasos(pos_i, v_i, k_v, pasos, t, m, output_widget):
    """
    Simula varios pasos acumulando desplazamiento y actualizando posiciones.
    """
    pos = pos_i  # Posición inicial
    v = v_i  # Velocidad inicial
    
    for i in range(pasos):
        # Calcular fuerza de viscosidad
        f_visc = [-k_v * v[0], -k_v * v[1]]
        
        # Realizar un paso
        delta_pos, v = un_paso(v, f_visc, t, m)
        
        # Actualizar posición acumulada
        pos = [pos[0] + delta_pos[0], pos[1] + delta_pos[1]]
        
        # Mostrar resultados en la interfaz
        output_widget.insert(tk.END, f"Paso {i+1}: Posición = {pos}, Velocidad = {v}\n")
        output_widget.yview(tk.END)  # Scroll automático

# Crear ventana principal
window = tk.Tk()
window.title("Simulación de Viscosidad")

# Entradas para parámetros
tk.Label(window, text="Posición inicial (x, y):").grid(row=0, column=0, sticky="w")
pos_input = tk.Entry(window)
pos_input.insert(0, "0, 0")
pos_input.grid(row=0, column=1)

tk.Label(window, text="Velocidad inicial (vx, vy):").grid(row=1, column=0, sticky="w")
vel_input = tk.Entry(window)
vel_input.insert(0, "10, 5")
vel_input.grid(row=1, column=1)

tk.Label(window, text="Constante de viscosidad (k_v):").grid(row=2, column=0, sticky="w")
kv_input = tk.Entry(window)
kv_input.insert(0, "0.5")
kv_input.grid(row=2, column=1)

tk.Label(window, text="Masa (m):").grid(row=3, column=0, sticky="w")
m_input = tk.Entry(window)
m_input.insert(0, "1")
m_input.grid(row=3, column=1)

tk.Label(window, text="Tiempo por paso (t):").grid(row=4, column=0, sticky="w")
t_input = tk.Entry(window)
t_input.insert(0, "1")
t_input.grid(row=4, column=1)

tk.Label(window, text="Número de pasos:").grid(row=5, column=0, sticky="w")
steps_input = tk.Entry(window)
steps_input.insert(0, "10")
steps_input.grid(row=5, column=1)

# Área de salida
tk.Label(window, text="Resultados de la simulación:").grid(row=6, column=0, sticky="w")
output = tk.Text(window, height=10, width=50)
output.grid(row=7, column=0, columnspan=2, pady=10)

# Botón para iniciar simulación
def iniciar_simulacion():
    output.delete(1.0, tk.END)  # Limpiar resultados previos
    
    # Obtener valores de entrada
    pos_i = list(map(float, pos_input.get().split(",")))
    v_i = list(map(float, vel_input.get().split(",")))
    k_v = float(kv_input.get())
    m = float(m_input.get())
    t = float(t_input.get())
    pasos = int(steps_input.get())
    
    # Ejecutar simulación
    acumula_pasos(pos_i, v_i, k_v, pasos, t, m, output)

start_button = tk.Button(window, text="Iniciar Simulación", command=iniciar_simulacion)
start_button.grid(row=8, column=0, columnspan=2)

# Ejecutar ventana
window.mainloop()

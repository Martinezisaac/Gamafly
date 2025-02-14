import threading
import time
import random
import tkinter as tk

# Lista de asientos disponibles (True = disponible, False = ocupado)
asientos = [True] * 20  # 20 asientos en el avión
asientos_en_proceso = [False] * 20  # False = nadie está intentando comprarlo, True = en proceso
clientes_en_proceso = {}  # Guarda los clientes que están comprando un asiento (asiento -> cliente)

# Semáforo para la exclusión mutua
semaforo = threading.Semaphore(1)

def vender_boleto(cliente, asiento_preferido, botones):
    global asientos, asientos_en_proceso, clientes_en_proceso
    
    # Cambiar el botón a amarillo (en proceso de compra)
    botones[asiento_preferido].config(bg="yellow")
    
    # Simular operación de asignación con duración aleatoria
    tiempo_asignacion = random.uniform(4, 8)  # La operación toma entre 2 y 5 segundos
    print(f"Cliente {cliente} está intentando comprar el asiento {asiento_preferido + 1}...")
    print(f"Cliente {cliente} tomará {tiempo_asignacion:.2f} segundos para asignar el asiento {asiento_preferido + 1}.")
    time.sleep(tiempo_asignacion)

    with semaforo:  # Exclusión mutua con semáforo
        # Confirmar y ocupar el asiento
        if random.uniform(1,100) < 30:
                cancelar_compra(asiento_preferido,botones)
        elif asientos[asiento_preferido]:
            asientos[asiento_preferido] = False
            # Cambiar el botón a rojo (asiento comprado)
            botones[asiento_preferido].config(bg="red", state=tk.DISABLED)
            print(f"Cliente {cliente} ha comprado el asiento {asiento_preferido + 1}.")
        else:
            print(f"Cliente {cliente}: El asiento {asiento_preferido + 1} ya ha sido comprado por otro cliente.")
        
        # Liberar el asiento del estado "en proceso"
        asientos_en_proceso[asiento_preferido] = False
        clientes_en_proceso.pop(asiento_preferido, None)

def proceso_cliente(cliente, botones):
    global clientes_en_proceso

    # Tiempo aleatorio de espera antes de que el cliente intente comprar
    tiempo_espera = random.uniform(5, 60)
    print(f"Cliente {cliente} esperará {tiempo_espera:.2f} segundos antes de intentar comprar.")
    time.sleep(tiempo_espera)
    
    while True:
        with semaforo:
            # Elegir asiento aleatoriamente
            asientos_disponibles = [i for i, disponible in enumerate(asientos) if disponible and not asientos_en_proceso[i]]
            asientos_en_proceso_compra = [i for i, en_proceso in enumerate(asientos_en_proceso) if en_proceso]
            
            if asientos_disponibles:
                asiento_preferido = random.choice(asientos_disponibles)
                asientos_en_proceso[asiento_preferido] = True
                clientes_en_proceso[asiento_preferido] = cliente
                # Cambiar el botón a amarillo (en proceso de compra)
                botones[asiento_preferido].config(bg="yellow")
                # Iniciar un hilo para simular la compra del boleto
                hilo = threading.Thread(target=vender_boleto, args=(cliente, asiento_preferido, botones))
                hilo.start()
                break
            elif asientos_en_proceso_compra:
                # Si todos los asientos disponibles están en proceso, mostrar en consola que otro cliente ya está intentando comprar ese asiento
                asiento_preferido = random.choice(asientos_en_proceso_compra)
                print(f"Cliente {cliente}: El asiento {asiento_preferido + 1} ya está siendo comprado por otro cliente.")
                break

def cancelar_compra(asiento, botones):
    global asientos, asientos_en_proceso, clientes_en_proceso
    if asientos_en_proceso[asiento]:
        # Cancelar el proceso de compra
        print(f"El cliente {clientes_en_proceso[asiento]} ha cancelado la compra del asiento {asiento + 1}.")
        asientos_en_proceso[asiento] = False
        clientes_en_proceso.pop(asiento, None)
        # Cambiar el botón a verde (asiento disponible)
        botones[asiento].config(bg="green", state=tk.NORMAL)
    else:
        print(f"No hay ninguna compra en proceso para el asiento {asiento + 1}.")

def iniciar_venta_automatica(botones):
    clientes = 30  # Número de clientes intentando comprar boletos
    
    for cliente in range(1, clientes + 1):
        # Crear un hilo por cliente para que intenten comprar de manera concurrente
        hilo_cliente = threading.Thread(target=proceso_cliente, args=(cliente, botones))
        hilo_cliente.start()

# Crear la ventana de la interfaz gráfica
def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("Venta de Boletos de Avión")
    
    # Crear botones para cada asiento
    botones = []
    for i in range(20):
        boton = tk.Button(ventana, text=f"Asiento {i+1}", width=15, height=2, bg="green")  # Verde = disponible
        boton.grid(row=i // 5, column=i % 5, padx=10, pady=10)
        botones.append(boton)


    # Ejecutar la venta automática de boletos
    threading.Thread(target=iniciar_venta_automatica, args=(botones,)).start()

    # Ejecutar el bucle principal de la interfaz gráfica
    ventana.mainloop()

# Iniciar la interfaz gráfica
crear_interfaz()

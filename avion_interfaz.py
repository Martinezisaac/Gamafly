import tkinter as tk  # Libreria para interfaz visual
from tkinter import ttk  # Librería para usar las listas desplegables (combobox)
from tkinter import messagebox  # Importar modales
import threading

asientosReservados = {}
tiempo = 30
asientosComprados = []

#La clase vuelo contiene los datos generales del vuelo, los cuales el usuario ira generando dichos datos conforme llena los formularios
class Vuelo:
    def __init__(self, nombre, edad, aerolinea, horaVuelo, diaPartida, numeroAsientos, asientosSeleccionados, origen, destino, total, estatusVuelo):
        self.nombre = nombre
        self.edad = edad
        self.aerolinea = aerolinea
        self.horaVuelo = horaVuelo
        self.diaPartida = diaPartida
        self.numeroAsientos = numeroAsientos
        self.asientosSeleccionados = []
        self.origen = origen
        self.destino = destino
        self.total = total 
        self.estatusVuelo = estatusVuelo
        self.lock = threading.Lock()

        # Atributos del cronómetro
        self.tiempoRestante = tiempo
        self.contadorActivo = False

    # Mostrar los frames en la misma ventana
    def mostrarSeleccionVuelo(self):
        # Crear ventana principal
        ventana = tk.Tk() #Crear una nueva ventana
        ventana.title("GAMAfly") #Titulo de la ventana
        ventana.geometry("720x600") #Tamaño default de la ventana

        # Centrar la ventana en la pantalla
        ventana.update_idletasks()  # Actualizar las tareas de la ventana para obtener el tamaño correcto
        width = ventana.winfo_width() # Obtener el ancho de la ventana de windows
        height = ventana.winfo_height() # Obtener la altura de la ventana windows 
        x = (ventana.winfo_screenwidth() // 2) - (width // 2) # Obtener el centro del monitor 
        y = (ventana.winfo_screenheight() // 2) - (height // 2) # Obtener el centro del monitor 
        ventana.geometry(f"{width}x{height}+{x}+{y}")  # Aplicar la nueva geometría

        # Crear frame para la selección de asientos
        self.frameAsientos = tk.Frame(ventana) #Crear frame para la primera interfaz 
        self.frameAsientos.pack(fill="both", expand=True) 

        self.frameCompra = tk.Frame(ventana) # Crear frame para visualizar la compra del usuario (oculto inicialmente)
        
        self.seleccionAsientos() #Mostrar primera interfaz
        ventana.mainloop()

    #Mostrar la segunda interfaz para la selccion del vuelo
        #En la segunda interfaz el usuario debe de seleccionar los asientos de su vuelo, en esta interfaz se obtienen los datos: 
        # - numeroAsientos (incluido en la funcion: "cantidadAsientos")
        # - asientosSeleccionados
    def seleccionAsientos(self):
        self.ocultar_frames() # Limpiar ventana

        # Crear los asientos
        fila, columna = self.cantidadAsientos() #Obtener la cantidad de filas y columnas de acuerdo al numero de asientos de un avion
        
        tk.Label(self.frameAsientos, text="Selecciona tus asientos", font=("Helvetica", 24, "bold")).pack(pady=20) #Titulo principal de la ventana

        # Información del vuelo
        tk.Label(self.frameAsientos, text="Nombre del pasajero: " + self.nombre, font=("Helvetica, 14")).pack() #Día de partida del vuelo
        tk.Label(self.frameAsientos, text="Día de partida: " + self.diaPartida, font=("Helvetica, 14")).pack() #Día de partida del vuelo 
        tk.Label(self.frameAsientos, text="Origen: " + self.origen, font=("Helvetica", 14)).pack() #Origen del vuelo
        tk.Label(self.frameAsientos, text="Destino: " + self.destino, font=("Helvetica", 14)).pack() #Destino del vuelo 
        tk.Label(self.frameAsientos, text="Hora del vuelo: " + self.horaVuelo, font=("Helvetica", 14)).pack() #Hora del vuelo

        asientos_frame = tk.Frame(self.frameAsientos)
        asientos_frame.pack(pady=20)

        self.botones = [] #Lista auxiliar que contiene los botones que representan los asientos del vuelo
        for i in range(fila): #Cantidad de filas que tiene el avion para la seleccion de asientos 
            for j in range(columna): #Cantidad de columnas que tiene el avion para la seleccion de asientos
                numAsiento = f"{chr(65 + i)}{j + 1}" #Generar el numero de asiento
                btn = tk.Button(asientos_frame, text=numAsiento, width=5, height=2) #Generar boton con el contenido del numero de asiento
                btn.grid(row=i, column=j, padx=5, pady=5) #Acomodar los botones que se vayan generando
                btn.config(command=lambda numeroAsiento=numAsiento, btn=btn: self.clicAsiento(numeroAsiento, btn)) #Editar los botones mediante la funcion "clicAsiento"
                self.botones.append(btn) #Agregar los botones a la lista

        self.contadorLabel = tk.Label(self.frameAsientos, text="Asientos seleccionados: 0", font=("Helvetica", 14)) # Mostrar el contador de asientos seleccionados
        self.precioVuelo = tk.Label(self.frameAsientos, text="Precio total: 0", font=("Helvetica", 14)) # Mostrar el precio total del vuelo
        self.contadorTiempo = tk.Label(self.frameAsientos, text="Temporizador: Seleccione una asiento", font=("Helvetica", 14)) # Mostrar el contador restante 

        self.contadorLabel.pack() #Mostrar el vuelo 
        self.precioVuelo.pack() #Mostrar el precio 
        self.contadorTiempo.pack() # Mostrar el contador de tiempo 

        # Botón para confirmar la selección de asientos
        confirmarBoton = tk.Button(self.frameAsientos, text="Confirmar vuelos", command=self.confirmarCompra, font=("Helvetica", 14), bg="lightblue") #Generar boton para confirmar la compra del vuelo
        confirmarBoton.pack(pady=20) #Mostrar el boton

        self.frameAsientos.pack(fill="both", expand=True) # Mostrar el frame de selección de asientos

    #Mostrar la tercera interfaz para mostrar los datos del avion
        #En la tercera interfaz el usuario es capaz de visualizar los datos de su vuelo, por lo que al llegar a esta interfaz la compra de los vuelos ha sido realizada, datos que se muestran en la interfaz 
        # - origen (obtenido de "seleccionVuelo") 
        # - destino (obtenido de "seleccionVuelo") 
        # - horaVuelo (obtenido de "seleccionVuelo") 
        # - diaVuelo (obtenido de "seleccionVuelo")
        # - numeroAsientos (obtenido de "seleccionAsientos")
        # - aerolinea (generada por defecto: "AeroMexico")
        # - estatusVuelo 
    def detalleBoletos(self):
        self.ocultar_frames() # Limpiar ventana

        # Generar datos 
        self.aerolinea = "AEROMEXICO"
        self.estatusVuelo = True

        # Titulo principal de la ventana
        titulo = tk.Label(self.frameCompra, text="Detalles del vuelo", font=("Helvetica", 24, "bold")) #Titulo principal dentro de la ventana
        titulo.pack(pady=20) #Mostrar el titulo

        # Datos del usuario
        tk.Label(self.frameCompra, text="Datos del pasajero", font=("Helvetica", 18, "bold")).pack(pady=10) #Titulo para datos del usuario
        tk.Label(self.frameCompra, text="Nombre del pasajero: " + self.nombre, font=("Helvetica", 14)).pack() #Nombre del pasajero
        tk.Label(self.frameCompra, text=f"Edad: {self.edad} años", font=("Helvetica", 14)).pack()  #Edad del pasajero

        # Datos del vuelo
        tk.Label(self.frameCompra, text="Datos de la compra", font=("Helvetica", 18, "bold")).pack(pady=10) #Titulo para datos del usuario
        tk.Label(self.frameCompra, text="Aerolínea: " + self.aerolinea, font=("Helvetica", 14)).pack() #Origen del vuelo
        tk.Label(self.frameCompra, text="Origen: " + self.origen, font=("Helvetica", 14)).pack() #Origen del vuelo
        tk.Label(self.frameCompra, text="Destino: " + self.destino, font=("Helvetica", 14)).pack() #Destino del vuelo
        tk.Label(self.frameCompra, text="Hora del vuelo: " + self.horaVuelo, font=("Helvetica", 14)).pack() #Hora del vuelo
        tk.Label(self.frameCompra, text="Día del vuelo: " + self.diaPartida, font=("Helvetica", 14)).pack() #Dia de partida del vuelo
        tk.Label(self.frameCompra, text=f"Asientos: {', '.join(self.asientosSeleccionados)}", font=("Helvetica", 14)).pack() #Asientos seleccionados
        tk.Label(self.frameCompra, text=f"Total: {self.total}$ MX", font=("Helvetica", 14)).pack()  # Precio total del vuelo

        self.frameCompra.pack(fill="both", expand=True) # Mostrar el frame de selección de asientos

    # METODOS AUXILIARES PARA LOS METODOS PRINCIPALES

    # Ocultar los frames generados en una ventana 
    def ocultar_frames(self):
        self.frameAsientos.pack_forget()
        self.frameCompra.pack_forget()

    # Cambiar el color del asiento seleccionado y actualizar el precio por cada seleccion 
    def clicAsiento(self, asiento, botonPresionado):

        def actualizarDatos(): #Funcion para actualizar los datos cuando el usuario selecciona los asientos 
            print("ASIENTOS: ", len(self.asientosSeleccionados))
            print("ASIENTOS RESERVADOS: ", len(asientosReservados))
            precio = self.calcularPrecioVuelo() * len(self.asientosSeleccionados) #Calcular el precio con base a la cantidad de asientos seleccionados
            self.total = precio #Obtener el total del vuelo
            self.contadorLabel.config(text=f"Asientos seleccionados: {len(self.asientosSeleccionados)}") #Mostrar texto actualizado de los asientos seleccionados
            self.precioVuelo.config(text=f"Precio total: {precio} $") #Mostrar el texto actualizado del precio de los vuelos / asientos

        #Colores para la seleccion de los asientos
        colorSeleccion = "#A5D0D7" #Color de un asiento seleccionado por el usuario 
        colorAsiento = "SystemButtonFace" #Color default de un asiento no seleccionado

        with self.lock: #Generar un candado al momento de seleccionar asientos
            if asiento in asientosReservados: #Validar si ya hay asientos reservados
                if self.nombre == asientosReservados[asiento]:  # Si el usuario ya reservó este asiento
                    del asientosReservados[asiento]
                    self.asientosSeleccionados.remove(asiento)
                    botonPresionado.config(bg=colorAsiento)
                    print("ASIENTO", asiento, "DESELECCIONADO POR", self.nombre)
                    actualizarDatos()
                else:  # Si el asiento está reservado por otro pasajero
                    messagebox.showwarning("Asiento ocupado", f"El asiento {asiento} ya ha sido reservado por {asientosReservados[asiento]}.")
                    actualizarDatos() 
                return  # Salir, ya que el asiento está ocupado
            elif asiento in asientosComprados:
                messagebox.showwarning("Asiento ocupado", f"El asiento {asiento} ya ha sido reservado")
                actualizarDatos() 
            else:
                if asiento in self.asientosSeleccionados: #Si el asiento ya esta seleccionado y el usuario da un clic nuevamente
                    self.asientosSeleccionados.remove(asiento) #Eliminar el asiento de la lista de asientos seleccionados
                    botonPresionado.config(bg=colorAsiento) #Devolver el color de asiento default
                    actualizarDatos()
                else: #Si el asiento aun no ha sido seleccionado y el usuario le dio clic
                    self.asientosSeleccionados.append(asiento) #Agregar el asiento a la lista de asientos seleccionados
                    botonPresionado.config(bg=colorSeleccion) #Colorear el asiento
                    asientosReservados[asiento] = self.nombre #Agregar e lnombre y el asiento 
                    print("ASIENTO", asiento, "RESERVADO POR", self.nombre)
                    actualizarDatos()

        # Iniciar o detener cronómetro según la selección
        if len(self.asientosSeleccionados) >= 1  and not self.contadorActivo: #Si el usuario selecciono un asiento y el contador no esta activo
            self.iniciar_cronometro() #Iniciar el cronometro cuando existe un solo asiento
        elif len(self.asientosSeleccionados) == 0 and self.contadorActivo: #Entonces no hay asientos seleccionados
            self.contadorActivo = False
            self.tiempoRestante = tiempo
            self.detenerBorrarCronometro()

    # Iniciar el cronometro
    def iniciar_cronometro(self):
        self.contadorActivo = True #Activar el cronometro
        self.tiempoRestante = tiempo #Definir el tiempo restante para el cronometro
        self.actualizar_cronometro() #Al inicar el cronometro se debe de estar actualizando

    # Detener el cronometro y borrar todos los asientos seleccionados
    def detenerBorrarCronometro(self):
        self.contadorActivo = False #Desactivar el contador
        self.tiempoRestante = tiempo # Reiniciar el temporizador / cronometro
        self.contadorTiempo.config(text="Temporizador: Seleccione un asiento") # Reiniciar el temporizador / cronometro
        self.deseleccionarTodosAsientos() #Eliminar todos los asientos seleccionados

    # Detener el cronometro 
    def detenerCronometroSinBorrarAsientos(self):
        self.contadorActivo = False
        self.tiempoRestante = tiempo
        self.contadorTiempo.config(text="Temporizador: Seleccione un asiento")

    # Actualizar el cronometro y validar si existen asientos seleccionados 
    def actualizar_cronometro(self):
        if self.contadorActivo and self.tiempoRestante > 0: #Validar si el contador esta activado y si tiene tiempo restante
            self.tiempoRestante -= 1 #Restar de uno en uno 
            self.contadorTiempo.config(text=f"Temporizador: {self.tiempoRestante}s") #Mostrar el tiempo restante
            self.frameAsientos.after(1000, self.actualizar_cronometro) #Mandar a llamar el frame nuevamente despues de 1 seg, es decir, actualizar la pantalla
            if self.contadorActivo and self.tiempoRestante > 0 and len(self.asientosSeleccionados) == 0: #Validar si el usuario deselecciono todos los asientos por su cuenta
                self.detenerCronometroSinBorrarAsientos() #Detener el cronometro 
        elif self.tiempoRestante == 0: # Si el tiempo restante se ha terminado
            self.detenerBorrarCronometro() #Detener el cronometro y eliminar los asientos seleccionados

    # Deseleccionar de manera automatica todos los asientos seleccionados por el usuario, ademas de devolverles su color original
    def deseleccionarTodosAsientos(self):
        self.asientosSeleccionados.clear() #Eliminar todos los asientos
        asientosReservados.clear() #Eliminar todos los asientos

        for boton in self.botones: #Obtener todos los botones
            boton.config(bg="SystemButtonFace") #Todos los botones estaran deseleccionados
        self.contadorLabel.config(text=f"Asientos seleccionados: 0") # Reiniciar el contador
        self.precioVuelo.config(text=f"Precio total: 0 $") #Reiniciar el precio total

        messagebox.showwarning("tiempo agotado", "Su tiempo de reserva se ha agotado, seleccione sus asientos nuevamente") #Mensaje al usuario

    # Manejar la confirmacion de la compra de los vuelos / asientos
    def confirmarCompra(self):
        if len(self.asientosSeleccionados) == 0: #Existe mas de un asiento seleccionado?
            messagebox.showinfo("Seleccion de boletos incompleta", "Usted no ha seleccionado sus boletos de avion") #Entonces no se puede proceder a la compra del vuelo porque no hay asientos seleccionados
        else: #Entonces hay uno o mas asientos seleccionados 
            respuesta = messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas realizar la compra?") #Mostrar modal de confirmacion de la compra

            for asiento in self.asientosSeleccionados: #Agregar a una nueva lista los asientos comprados
                asientosComprados.append(asiento) #Asientos comprados

            if respuesta: #Si la respuesta es Aceptar / confirmar
                self.detalleBoletos() #Dirigirse al metodo de "detalleBoletos"
                self.detenerCronometroSinBorrarAsientos() #Detener el cronometro por que la compra ya se ha realizado
            else: # Si la respuesta es no
                # Cerrar el modal sin hacer ninguna accion
                pass

    # Calcular la cantidad de asientos que el avion tendra, la funcion devuelve el numero de filas y columnas que el avion tendra
    def cantidadAsientos(self):
        self.numeroAsientos = 30 #Numero de asientos del avion
        columna = 10
        fila = self.numeroAsientos // columna #Cantidad de filas (en esta caso la fila esta limitada por la cantidad de columnas)
        return fila, columna #Devolver la cantidad filas y columnas que se necesita para el avion

    # Calcular el precio de un vuelo
    def calcularPrecioVuelo(self):
        precio = 0
        TUA = 0
        if self.origen == "Mexico": #Precio de volar desde mexico 
            precio = 10300 #Precio definido 
            TUA = 1200 #Impuesto por uso de las instalaciones del aeropuerto 
        elif self.origen == "Brasil": #Precio por volar desde Brasil 
            precio = 8700 #Precio definido 
            TUA = 800 #Impuesto por uso de las instalaciones del aeropuerto
        elif self.origen == "Colombia": #Precio de volar desde colombia
            precio = 5600 #Precio definido 
            TUA = 650 #Impuesto por uso de las instalaciones del aeropuerto

        if self.destino == "Estados Unidos": #Precio de volar hacia Estados Unidos
            precio += 12100 #Precio definido 
        elif self.destino == "España": #Precio por volar hacia España
            precio += 16500 #Precio definido 

        return precio + TUA #Devolver el precio mas el impuesto por uso de instalaciones

if __name__ == "__main__":

    vuelo1 = Vuelo("Isaac", 21, None, "10:00am", "10 de noviembre de 2024", None, None, "Mexico", "Estados Unidos", None, None) #Creacion de un objeto
    vuelo2 = Vuelo("Erick", 21, None, "10:00am", "10 de noviembre de 2024", None, None, "Mexico", "Estados Unidos", None, None) #Creacion de un objeto
    #vuelo3 = Vuelo("Pedro", 21, None, "10:00am", "10 de noviembre de 2024", None, None, "Mexico", "Estados Unidos", None, None) #Creacion de un objeto

    # Crear hilos sin ejecutar inmediatamente
    hilo1 = threading.Thread(target=vuelo1.mostrarSeleccionVuelo)
    hilo1.start()
    
    hilo2 = threading.Thread(target=vuelo2.mostrarSeleccionVuelo)
    hilo2.start()

    #hilo3 = threading.Thread(target=vuelo3.mostrarSeleccionVuelo)
    #hilo3.start()
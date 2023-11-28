import tkinter as tk
from tkinter import filedialog
import subprocess
import os



def abrir_archivo():
    archivo = filedialog.askopenfilename(initialdir="./", title="Seleccionar archivo", filetypes=(("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")))
    
    etiqueta_ruta.config(text="Ruta del archivo: " + archivo)
    
    # Almacena la ruta del archivo para usarla al iniciar la simulación
    ventana.archivo_seleccionado = archivo
    
    # Habilita el botón de iniciar simulación
    boton_simulacion.config(state=tk.NORMAL)

def iniciar_simulacion():
    if hasattr(ventana, 'archivo_seleccionado') and ventana.archivo_seleccionado:
        subprocess.run(["python", "../code/main.py", ventana.archivo_seleccionado])
    else:
        print("Error: No se ha seleccionado un archivo.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Selector de Archivos")

# Agregar un título
titulo = tk.Label(ventana, text="Selecciona un archivo", font=("Arial", 14))
titulo.pack(pady=10)

# Agregar una imagen
imagen = tk.PhotoImage(file="../code/logo.png") 
imagen_label = tk.Label(ventana, image=imagen)
imagen_label.pack()

# Botón para abrir el cuadro de diálogo
boton_abrir = tk.Button(ventana, text="Seleccionar Archivo", command=abrir_archivo)
boton_abrir.pack(pady=20)

# Etiqueta para mostrar la ruta del archivo seleccionado
etiqueta_ruta = tk.Label(ventana, text="Ruta del archivo: ")
etiqueta_ruta.pack()

boton_simulacion = tk.Button(ventana, text="Iniciar Simulación", command=iniciar_simulacion, state=tk.DISABLED)
boton_simulacion.pack(pady=20)

ventana.mainloop()

import pandas as pd
import tkinter.filedialog as filedialog

# Atibutos de cada proceso
class Proceso:
    def __init__(self, id, tiempo_irrupcion, tiempo_arribo,tamanio):     
        self.id = id                            
        self.tiempo_irrupcion = tiempo_irrupcion                             
        self.tiempo_arribo = tiempo_arribo                            
        self.tamanio = tamanio                   
        
    def __str__(self):
        return f"{self.id} {self.tiempo_irrupcion} {self.tiempo_arribo} {self.tamanio}"

    def SetEstado(self, estado):
        self.estado = estado


class Particion:                          
    def __init__(self, id, tamanio, direccion):
        self.id = id                            
        self.tamanio = tamanio
        self.estado = "libre"   #inicia con la partición libre.
        self.direccion = direccion
        self.proceso = None     #inicia sin proceso asignado.
        self.fragmentacion_interna = 0 

    def __str__(self): 
        return f"Partición ID: {self.id} Tamaño: {self.tamanio} Estado: {self.estado} Proceso: {self.proceso} Fragmentación interna: {self.fragmentacion_interna}"
    
    def SetParticion(self, proceso, estado, fragmentacion_interna):
        self.proceso = proceso
        self.estado = estado
        self.fragmentacion_interna = fragmentacion_interna


class Procesador:
    def __init__(self):
        self.Particion = None
        self.proceso = None
        self.tiempo_restante = -1

    def __str__(self):
        return f"Partición: {self.Particion} Proceso: {self.proceso} Tiempo de irrupción: {self.tiempo_restante}"
    
    def SetProcesador(self, proceso, tiempo_restante, Particion):
        self.proceso = proceso
        self.tiempo_restante = tiempo_restante 
        self.Particion = Particion



class Memoria:
    def __init__(self):
        self.memoria = []
        self.procesos = [] 
        self.cola_nuevos = [] 
        self.cola_bloqueados = [] 
        self.cola_listos = [] 
        self.cola_suspendidos = [] 
        self.control_multiprogramacion = [] #Cola de control de multiprogramación (máximo 5 procesos).
        self.cola_terminados = [] 
        self.tiempo_transcurrido = 0
        self.procesador = Procesador()
        self.acumulador_tiempo_irrupcion = 0
        self.proceso_nuevo = False  #se establece a True si hay un nuevo proceso.
        self.proceso_listo = False  #se establece a True si hay un proceso listo para ejecutarse.
        self.proceso_fin = False    #se establece a True si hay un proceso que termino su ejecucion.

    def __str__(self):
        return f"Memoria: {self.memoria}"

    def SetParticiones(self): 
        #Se le pasa el id, el tamaño y luego la direccion que definirá los limites.
        self.memoria.append(Particion(1, 250, 100000)) #Partición 1 de 250 kb para procesos grandes.
        self.memoria.append(Particion(2, 120, 350000)) #Partición 2 de 120 kb para procesos medianos.
        self.memoria.append(Particion(3, 60, 410000)) #Partición 3 de 60 kb para procesos pequeños.
    
    def SetProcesos(self): #Carga del archivo csv.
        try:
            #El usuario podra elegir el archivo csv que desee con el explorador de archivos.
            archivo = filedialog.askopenfilename(initialdir = "./",title = "Seleccione el archivo csv",filetypes = (("csv files","*.csv"),("all files","*.*")))
            df = pd.read_csv(archivo,index_col=0,header=0)
            df=pd.DataFrame(df)
            if len(df) > 10: #Control de cantidad de procesos cargados por el usuario.
                print("\nAviso: El archivo .csv posee mas de 10 procesos, se tomaron en cuenta solo los primeros 10.")
                df=df.head(10)
            for i in range(len(df)):
                if df.iat[i,2] > 250:
                    print("\nAviso: El proceso",df.iat[i,0],"posee un tamaño mayor a 250 kb, por lo cual no se lo incluye.")
                else:
                    self.procesos.append(Proceso(df.index[i],df.iat[i,0],df.iat[i,1],df.iat[i,2]))
                
            print("\n  Simulador \n")
            print(df)
        except pd.errors.EmptyDataError:
            print("El archivo se encuentra vacio")
            input("\nPresione Enter para continuar.") 
            quit()
        except FileNotFoundError:
            print("No se selecciono ningun archivo")
            input("\nPresione Enter para continuar.")
            quit()

    
    #luego de importar cargo los nuevos
    def CargaNuevos(self):
        self.proceso_nuevo = False
        for i in range(len(self.procesos)):                   
                if (self.procesos[i].tiempo_arribo == self.tiempo_transcurrido):
                    if (self.procesos[i].tamanio <= 250):
                        self.cola_nuevos.append(self.procesos[i])
                        self.proceso_nuevo = True
                    else:
                        self.cola_bloqueados.append(self.procesos[i])


    def OrdenRoundRobin(self):
        if len(self.control_multiprogramacion) > 0:
            if self.procesador.proceso is None:
                # Si el procesador está inactivo, selecciona el primer proceso de la cola de control de multiprogramación.
                self.procesador.proceso = self.control_multiprogramacion.pop(0)
                self.procesador.tiempo_restante = 2  # Configura el tiempo restante en 2 (quantum).
            else:
                proceso_actual = self.procesador.proceso
                if self.procesador.tiempo_restante > 0:
                    # Si el proceso actual tiene tiempo restante se resta 1.
                    self.procesador.tiempo_restante -= 1 
                else:
                    # Si el proceso actual termino su quantum se lo coloca al final de la lista.
                    self.control_multiprogramacion.append(self.procesador.proceso)
                    self.procesador.proceso = None

                # Selecciona el próximo proceso de la cola para ejecutar.
                if len(self.control_multiprogramacion) > 0:
                    self.procesador.proceso = self.control_multiprogramacion.pop(0)
                    self.procesador.tiempo_restante = 2  # Configura el tiempo restante en 2 (quantum).
                else:
                    self.procesador.proceso = None


    def GetParticion(self, proceso):
        for i in range(len(self.memoria)):
            if (self.memoria[i].proceso == proceso):
                return i

    def CargaControlMultiprogramacion(self):
        self.proceso_listo = False
        for i in range(len(self.cola_nuevos)):
            if len(self.control_multiprogramacion) < 5:
                self.control_multiprogramacion.append(self.cola_nuevos.pop(0))
                self.proceso_listo = True
        self.OrdenRoundRobin()
    
    def EstadoMemoria(self):
        i=0
        for i in range(len(self.memoria)):
            if (self.memoria[i].estado == "libre"):
                i+=1
        return i
    #_______________________
    def CargaMemoria(self): # Best Fit
        if self.EstadoMemoria() != 0:  # Comprueba si hay particiones libres en la memoria.
            for i in range(len(self.control_multiprogramacion[:3])):  # Considera los primeros tres procesos que pueden ingresar, porque son 4 particiones y una es del sistema op.
                if self.control_multiprogramacion[i].id not in [Particion.proceso.id for Particion in self.memoria if Particion.proceso != None]:  # Si el proceso no está en memoria, si esta en memoria no es necesario asignarlo nuevamente,
                    best_fit_particion = None
                    best_fit_tamanio = float('inf') # Float('inf') es el infinito positivo, para que inicie con valor grande. 
                    
                    for j in range(len(self.memoria)):
                        if self.memoria[j].estado == "libre" and self.control_multiprogramacion[i].tamanio <= self.memoria[j].tamanio:
                            # Encuentra la partición más pequeña que sea lo suficientemente grande para el proceso y se ajuste mejor.
                            if self.memoria[j].tamanio < best_fit_tamanio:
                                best_fit_particion = j
                                best_fit_tamanio = self.memoria[j].tamanio
                    
                    if best_fit_particion is not None:
                        # Asigna el proceso a la partición que mejor se ajusta.
                        self.memoria[best_fit_particion].SetParticion(self.control_multiprogramacion[i], "ocupado", self.memoria[best_fit_particion].tamanio - self.control_multiprogramacion[i].tamanio) #La resta es la fragmentación interna.

    def CargaProcesador(self):
        if len(self.control_multiprogramacion) > 0:
            if (self.procesador.proceso == None and self.control_multiprogramacion[0].id in [Particion.proceso.id for Particion in self.memoria if Particion.proceso != None] ): #Si el procesador está libre y el proceso en la primera posición de la cola de control de multiprogramacion está en memoria.                                
                self.procesador.SetProcesador(self.control_multiprogramacion[0], self.control_multiprogramacion[0].ti, self.GetParticion(self.control_multiprogramacion[0]))  #Se carga el proceso en el procesador.
                                                                                                                                

    def CargaSuspendidos(self):
        for i in range(len(self.control_multiprogramacion)):
                if ((self.control_multiprogramacion[i].id not in [Particion.proceso.id for Particion in self.memoria if Particion.proceso != None]) and (self.control_multiprogramacion[i].id not in [proceso.id for proceso in self.cola_suspendidos])): #Se carga en la cola de suspendidos todos los procesos que no esten en memoria, sin tener en cuenta el orden de la CCM
                    self.cola_suspendidos.append(self.control_multiprogramacion[i])

    def ReordenarMemoria(self):
        #Tenemos que controlar que despues de ordenar todos los proceso a partir del segundo esten o en memoria o suspendidos 
        #Los primeros 3 pueden estar en memoria pero no es necesario que deban hacerlo
        #Excepto el primer proceso el resto puede estar suspendido 
        for i in range(len(self.memoria)):
            if (self.memoria[i].proceso != None):
                if (self.memoria[i].proceso.id not in [proceso.id for proceso in self.control_multiprogramacion[:3]])and (self.memoria[i].proceso != self.procesador.proceso):  
                    #[proceso.id for Particion in self.control_multiprogramacion[:3]]   
                    self.memoria[i].SetParticion(None,"libre",0)                                                                                            
       #Limpiamos la cola de suspendidos exceptuando las Particiones que no es necesario mover a la cola de listos

    def ReordenarSuspendidos(self):
        #Tenemos que controlar que despues de ordenada y cargada la memoria los procesos que no se encuentren en la misma se encuentren suspendidos 
       #Limpiamos la cola de suspendidos exceptuando las Particiones que no es necesario mover a la cola de listos
        for proceso in self.cola_suspendidos:
            if (proceso.id in [Particion.proceso.id for Particion in self.memoria if Particion.proceso != None]):
                self.cola_suspendidos.remove(proceso)

    def ControlProcesador(self): #Actualizamos el tiempo restante del proceso que se encuentra en el procesador y controlamos si ya terminó de ejecutarse
        self.proceso_fin = False
        if (self.procesador.proceso != None):
            self.procesador.tiempo_restante -= 1 
            if (self.procesador.tiempo_restante == 0):
                self.proceso_fin = True
                for i in range(len(self.memoria)):
                    if self.memoria[i].proceso == self.procesador.proceso:
                        self.memoria[i].SetParticion(None,"libre",0) #Eliminamos el proceso de la memoria
                self.control_multiprogramacion.remove(self.procesador.proceso) #Eliminamos el proceso de la cola de control de multiprogramacion
                self.cola_terminados.append(self.procesador.proceso.id) #Agregamos el id del proceso a la lista de terminados
                self.procesador.SetProcesador(None,-1,None) #Eliminamos el proceso del procesador
            
    def PrintMemoria(self):
        if (self.proceso_nuevo or self.proceso_listo or self.proceso_fin):
            if self.proceso_nuevo:
                print("\nNuevo proceso")
            elif self.proceso_listo:
                print("\nNuevo proceso listo")
            elif self.proceso_fin:
                print("\nFin proceso")
        
            print("\nTiempo actual: ", self.tiempo_transcurrido)
            if (self.procesador.proceso == None):
                print("Estado del procesador: NULL (libre)")
            else:
                print("Estado del procesador: Proceso ", self.procesador.proceso.id, " (tiempo restante: ", self.procesador.tiempo_restante, ")")
            
            print("Cola de listos: ", [Particion.proceso.id for Particion in self.memoria if (Particion.proceso != None) and (Particion.proceso != self.procesador.proceso)])  #[proceso.id for proceso in self.control_multiprogramacion]
            #print("Cola de multiprogramacion: ", [proceso.id for proceso in self.control_multiprogramacion ] )
            print("Cola de suspendidos: ", [proceso.id for proceso in self.cola_suspendidos])    #[proceso.id for proceso in self.cola_suspendidos]
            print("Cola de nuevos: ", [proceso.id for proceso in self.cola_nuevos])             #[proceso.id for proceso in self.cola_nuevos]
            print("Cola de terminados: ", self.cola_terminados)

            #Agregar un sleep o un input para que el usuario pueda ver el estado de la memoia
                      
            print("\nTabla de Particiones")
            # Imprimir la tabla de Particiones con tabulaciones para hacerla legible
            print ("| {:<15} | {:<15} | {:<15} | {:<15} | {:<21} |".format('Id Particion','Direccion Inicio','Tamaño','Id Proceso','Fragmentación Interna'))
            print ("| {:<15} | {:<16} | {:<15} | {:<15} | {:<21} |".format('0','0','100','SO','-'))
            for i in range(len(self.memoria)):
                if (self.memoria[i].proceso == None):
                    print ("| {:<15} | {:<16} | {:<15} | {:<15} | {:<21} |".format(self.memoria[i].id,self.memoria[i].direccion,self.memoria[i].tamanio,'NULL','NULL'))
                else:
                    print ("| {:<15} | {:<16} | {:<15} | {:<15} | {:<21} |".format(self.memoria[i].id, self.memoria[i].direccion, self.memoria[i].tamanio, self.memoria[i].proceso.id, self.memoria[i].fragmentacion_interna))
            
            input("\nPresione enter para continuar...")  


    def cicloprincipal(self):
        self.SetParticiones()
        self.SetProcesos() 
        self.CargaNuevos()
        self.CargaControlMultiprogramacion()
        # self.limpiar()  En el primer ciclo no seria necesario
        self.CargaMemoria()
        self.CargaProcesador()
        self.CargaSuspendidos()
        self.PrintMemoria()
        self.tiempo_transcurrido += 1
        while len(self.cola_terminados) != (len(self.procesos)):
            self.ControlProcesador()
            self.CargaNuevos()
            self.CargaControlMultiprogramacion()
            self.ReordenarMemoria() 
            self.CargaMemoria()
            self.CargaProcesador()
            self.ReordenarSuspendidos()
            self.CargaSuspendidos()
            self.ReordenarSuspendidos()
            self.PrintMemoria()
            self.tiempo_transcurrido += 1
        print("\nFin\n")
        input("\nPresione Enter para cerrar...")  

if __name__ == "__main__":
    Memoria= Memoria()
    Memoria.cicloprincipal()

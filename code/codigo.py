# importarciones
from lector import leer_datos
from pathlib import Path
from prettytable import PrettyTable
from copy import deepcopy



class BloqueParticion:
    def __init__(self, tamanio: int):
        self.tamanio = tamanio
        self.fragmentacion_interna = 0
        self.proceso: BloqueProceso | None = None


class BloqueProceso:
    def __init__(self, arreglo: list[int]):
        self.id = arreglo[0]
        self.tamanio = arreglo[1]
        self.tiempo_arribo = arreglo[2]
        self.tiempo_irrupcion = arreglo[3]
        self.tiempo_espera = 0
        self.instante_salida = 0
        self.resguardo_tiempo_irrupcion = arreglo[3]
        self.estado = "Nuevo"
        self.particion: BloqueParticion | None = None

    def lista_procesos(self) -> list:
        arreglo = []
        arreglo.append(self.id)
        arreglo.append(self.tamanio)
        arreglo.append(self.tiempo_arribo)
        arreglo.append(self.tiempo_irrupcion)
        arreglo.append(self.estado)
        return arreglo

class BloqueMemoria:
    def __init__(self, distribucion_memoria: list):
        self.particiones: list[BloqueParticion] = distribucion_memoria[1:]

def obtener_tiempo_arribo(proceso: BloqueProceso) -> int:
    return proceso.tiempo_arribo


def leer_archivo(origen: Path, tamano: int) -> list[BloqueProceso]:
    datos = leer_datos(origen)
    resultado = []

    for p in datos.values():
        proceso = BloqueProceso(p)
        if (
            proceso.tamanio <= 250
            and proceso.tiempo_arribo >= 0
            and proceso.tiempo_irrupcion >= 1
            and len(resultado) < tamano
        ):
            resultado.append(proceso)
        continue

    resultados_filtrados = []
    for proceso in resultado:
        if proceso.tiempo_irrupcion > 0:
            resultados_filtrados.append(proceso)

    resultados_filtrados.sort(key=obtener_tiempo_arribo)
    resultado = resultados_filtrados

    return resultado


def informe_estadistico(
    cola_finalizados: list[BloqueProceso],
):
    encabezado_informe = [
        "ID",
        "RESPUESTA",
        "ESPERA",
        "RETORNO",
    ]

    encabezado_promedios = [
        "RESPUESTA",
        "ESPERA",
        "RETORNO",
    ]

    tabla_estadisticas = PrettyTable()
    tabla_estadisticas.field_names = encabezado_informe
    for proceso in cola_finalizados:
        tiempo_respuesta = proceso.instante_salida - proceso.tiempo_arribo
        tiempo_retorno = proceso.resguardo_tiempo_irrupcion + proceso.tiempo_espera
        tiempo_espera = proceso.tiempo_espera

        tabla_estadisticas.add_row([
            str(proceso.id),
            str(tiempo_respuesta),
            str(tiempo_espera),
            str(tiempo_retorno),
        ])

    tabla_promedios = PrettyTable()
    tabla_promedios.field_names = encabezado_promedios

    acumulador_tiempo_respuesta = 0
    acumulador_tiempo_retorno = 0
    acumulador_tiempo_espera = 0

    for proceso in cola_finalizados:
        acumulador_tiempo_respuesta += proceso.instante_salida - proceso.tiempo_arribo
        acumulador_tiempo_retorno += proceso.resguardo_tiempo_irrupcion + proceso.tiempo_espera
        acumulador_tiempo_espera += proceso.tiempo_espera

    total= len(cola_finalizados)

    tabla_promedios.add_row([
        str(round((acumulador_tiempo_respuesta / total), 2)),
        str(round((acumulador_tiempo_espera / total), 2)),
        str(round((acumulador_tiempo_retorno / total), 2)),
    ])

    print(f"-->PROMEDIOS\n{tabla_promedios}\n")
    print(f"-->RESUMEN DE BLOQUES DE PROCESOS\n{tabla_estadisticas}\n")


def agregar_filas_memoria(tabla, particiones):
    memoria_encabezado = [
        "ID", "Dirección", "Tamaño Partición(KB)", "Tamaño Proceso(KB)", "Frag. Interna(KB)"]
    tabla.field_names = memoria_encabezado

    for particion in particiones:
        if particion and particion.proceso is not None:
            tabla.add_row([
                particion.proceso.id,
                hex(id(particion)),
                particion.tamanio,
                particion.proceso.tamanio,
                particion.fragmentacion_interna
            ])


def agregar_filas_procesos(tabla, procesos):
    procesos_encabezado = [
        "ID", "Tamaño Proceso(KB)", "Tiempo Arribo", "Tiempo Irrupción", "Estado"]
    tabla.field_names = procesos_encabezado

    for p in procesos:
        tabla.add_row([p.id, p.tamanio, p.tiempo_arribo,
                      p.tiempo_irrupcion, p.estado])


def tabla_inicio(title: str, datos: list[BloqueProceso], encabezados: list):
    tabla = PrettyTable()
    tabla.title = title
    tabla.header = True
    tabla.align = "c"
    tabla.field_names = encabezados
    for p in datos:
        tabla.add_row(p.lista_procesos())
    print(f"\n{tabla}\n")


def generar_tabla(datos, title):
    tabla = PrettyTable()
    tabla.title = title
    tabla.header = True
    tabla.align = "c"

    if isinstance(datos, BloqueMemoria):
        agregar_filas_memoria(tabla, datos.particiones)
    elif isinstance(datos, list):
        agregar_filas_procesos(tabla, datos)

    return tabla


def mostrar_estado(
    cola_nuevos: list[BloqueProceso],
    cola_listos: list[BloqueProceso],
    cola_finalizados: list[BloqueProceso],
    memoria: BloqueMemoria,
):
    tabla_memoria = generar_tabla(memoria, "Memoria")
    print(tabla_memoria, "\n")

    if len(cola_nuevos) != 0:
        tabla_nuevos = generar_tabla(cola_nuevos, "Cola de Nuevos")
        print(tabla_nuevos, "\n")
    else:
        print("»» La cola de Nuevos está vacía.")

    if len(cola_listos) != 0:
        tabla_listos = generar_tabla(cola_listos, "Cola de Listos")
        print(tabla_listos, "\n")
    else:
        print("»» La cola de Listos está vacía.\n")

    if len(cola_finalizados) != 0:
        tabla_finalizados = generar_tabla(cola_finalizados, "Procesos Finalizados")
        print(tabla_finalizados)

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")





def setear(proceso: BloqueProceso, particion: BloqueParticion):
    proceso.estado = "Listo"
    particion.proceso = proceso
    particion.fragmentacion_interna = particion.tamanio - proceso.tamanio
    proceso.particion = particion


def asignacion_a_memoria(
    cola_nuevos: list[BloqueProceso],
    cola_listos: list[BloqueProceso],
    cola_finalizados: list[BloqueProceso],
    memoria_principal: BloqueMemoria,
    reloj: int,
    quantum: int,
    ejecutar,
    interrumpir,
):
    aux_listos = []
    aux_suspendidos = []
    aux = []
    for p in cola_listos:
        if p.estado == "Suspendido" and p.tiempo_arribo <= reloj:
            aux.append(p)
        continue

    for p in aux:
        for particion in memoria_principal.particiones:
            if particion.proceso is None:
                if p.tamanio <= particion.tamanio:
                    setear(p, particion)
                    aux_suspendidos.append(p)
                    break

    while (
        (len(cola_nuevos) > 0)
        and (cola_nuevos[0].tiempo_arribo <= reloj)
        and (len(cola_listos) < 5)
    ):
        proceso = cola_nuevos.pop(0)
        for particion in memoria_principal.particiones:
            if particion.proceso is None:
                if proceso.tamanio <= particion.tamanio:
                    setear(proceso, particion)
                    aux_listos.append(proceso)
                    break

        if proceso.particion is None:
            proceso.estado = "Suspendido"

        cola_listos.append(proceso)

    if not ejecutar:
        if len(aux_listos) > 0 or len(aux_suspendidos) > 0:
            input(
                ">>>Presione Enter para continuar o CTRL+C para terminar la ejecución.\n"
            ) if not interrumpir else None
            print("\n#  Datos:")
            print(f"» Tiempo Transcurrido: {reloj}")
            print(f"» Quantum: {quantum}")
            print(
                f"» {', '.join(str(p.id) for p in aux_listos)} cambia de 'Nuevo' a 'Listo'"
            ) if len(aux_listos) > 0 else None
            print(
                f"» {', '.join(str(p.id) for p in aux_suspendidos)} cambia de 'Suspendido' a 'Listo'"
            ) if len(aux_suspendidos) > 0 else None

            mostrar_estado(
                cola_nuevos, cola_listos, cola_finalizados, memoria_principal
            )

    aux_listos = []
    aux_suspendidos = []


def Run(cola_nuevos: list[BloqueProceso], ejecutar, interrumpir):
    memoria_principal = BloqueMemoria(
        [BloqueParticion(100), BloqueParticion(
            60), BloqueParticion(120), BloqueParticion(250)]
    )
    reloj = 0
    aux = 0
    quantum = 2  # es el parametro
    cola_listos: list[BloqueProceso] = []
    cola_finalizados: list[BloqueProceso] = []
    procesador_libre = True

    print(f"\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<DATOS INGRESADOS>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n ")
    tabla_inicio(
        "Nuevos Procesos",
        cola_nuevos,
        ["ID", "Tamaño Proceso(KB)", "Tiempo Arribo",
         "Tiempo Irrupción", "Estado"],
    )
    print(f"\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    while reloj != cola_nuevos[0].tiempo_arribo:
        reloj += 1

    while True:
        asignacion_a_memoria(
            cola_nuevos,
            cola_listos,
            cola_finalizados,
            memoria_principal,
            reloj,
            quantum,
            ejecutar,
            interrumpir,
        )

        if procesador_libre:
            quantum = 2

        '''
            Esto debido a que si tengo procesos con tiempos de arribo con una diferencia más grande que quantum,
            la cola de listos estará vacía por un periodo largo e Indexar lista vacía es un error.
        '''
        if len(cola_listos) == 0:
            reloj += 1
            continue

        proceso = cola_listos[0]
        proceso.estado = "Ejecutando"

        if ejecutar:
            input(
                ">>>Presione Enter para continuar o CTRL+C para terminar la ejecución.\n"
            ) if not interrumpir else None
            print("\n#  Datos:")
            print(f"» Tiempo Transcurrido: {reloj}")
            print(f"» Quantum: {quantum}")
            mostrar_estado(
                cola_nuevos, cola_listos, cola_finalizados, memoria_principal
            )

        if not ejecutar:
            if proceso.id != aux:
                input(
                    ">>>Presione Enter para continuar o CTRL+C para terminar la ejecución.\n"
                ) if not interrumpir else None
                print("\n#  Datos:")
                print(f"» Tiempo Transcurrido: {reloj}")
                print(f"» Quantum: {quantum}")
                print(f"» Pasa a ejecución: {proceso.id}")
                mostrar_estado(
                    cola_nuevos, cola_listos, cola_finalizados, memoria_principal
                )

            aux = proceso.id

        reloj += 1
        proceso.tiempo_irrupcion -= 1

        for p in cola_listos[1:]:
            if p.estado == "Listo":
                p.tiempo_espera += 1

        procesador_libre = False

        if proceso.tiempo_irrupcion == 0:
            proceso.estado = "Finalizado"
            proceso.instante_salida = reloj

            if (particion := proceso.particion) is not None:
                particion.proceso = None
                particion = None

            proceso = deepcopy(proceso)
            proceso.tiempo_irrupcion = proceso.resguardo_tiempo_irrupcion
            cola_finalizados.append(proceso)
            procesador_libre = True
            cola_listos.pop(0)

            if not ejecutar:
                input(
                    ">>>Presione Enter para continuar o CTRL+C para terminar la ejecución.\n"
                ) if not interrumpir else None
                print("\n#  Datos:")
                print(f"» Tiempo Transcurrido: {reloj}")
                print(f"» Quantum: {quantum}")
                print(f"» Finalización del proceso: {proceso.id}")
                mostrar_estado(
                    cola_nuevos, cola_listos, cola_finalizados, memoria_principal
                )

            if len(cola_listos) == 0 and len(cola_nuevos) == 0:
                break
        else:
            quantum -= 1

            if quantum != 0:
                continue

            if len(cola_listos) != 1:
                proceso.estado = "Listo"
                cola_listos.append(cola_listos.pop(0))
                procesador_libre = True
            else:
                quantum = 2

        if len(cola_listos) > 0:
            resg_id = 0
            if cola_listos[0].estado == "Suspendido":
                proceso = cola_listos[0]
                min_frag = 999
                min_particion = memoria_principal.particiones[0]

                for particion in memoria_principal.particiones:
                    frag_generada = particion.tamanio - proceso.tamanio
                    if min_frag >= frag_generada and frag_generada >= 0:
                        min_frag = frag_generada
                        min_particion = particion

                if (p := min_particion.proceso) is not None:
                    p.estado = "Suspendido"
                    resg_id = p.id

                proceso.estado = "Listo"

                min_particion.proceso = proceso
                proceso.particion = min_particion

                min_particion.fragmentacion_interna = min_particion.tamanio - proceso.tamanio

                if not ejecutar:
                    input(
                        ">>>Presione Enter para continuar o CTRL+C para terminar la ejecución.\n"
                    ) if not interrumpir else None
                    print("\n#  Datos:")
                    print(f"» Tiempo Transcurrido: {reloj}")
                    print(f"» Quantum: {quantum}")
                    print(f"»  Swap-In: {proceso.id}") if resg_id == 0 else print(
                        f"  »  Swap-Out: {resg_id} y Swap-In: {proceso.id}")
                    mostrar_estado(
                        cola_nuevos, cola_listos, cola_finalizados, memoria_principal
                    )

        continue

    if ejecutar:
        input(
            ">>>Presione Enter para continuar o CTRL+C para terminar la ejecución.\n"
        ) if not interrumpir else None

        print("\n#  Datos:")
        print(f"» Tiempo Transcurrido: {reloj}")
        print(f"» Quantum: {quantum}")
        mostrar_estado(cola_nuevos, cola_listos,
                       cola_finalizados, memoria_principal)

    print(f"\n\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<INFORME ESTADÍSTICO>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n\n  ")
    informe_estadistico(cola_finalizados)
    print(
        f"\n\n*Tiempo utilizado: {reloj} unidades de tiempo\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>FIN DEL SIMULADOR>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

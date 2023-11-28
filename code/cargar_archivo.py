import inquirer, os
from inquirer import errors
from pathlib import Path, PurePath
from codigo import Run
from codigo import BloqueProceso, leer_archivo


def clear_screen():
    os.system("tput reset")

def validar_tamaño(answers, current):
    try:
        if int(current) >= 0 and int(current) <= 250:
            return True
    except:
        raise errors.ValidationError(
            "", reason="El tamaño de un proceso no puede ser mayor a 250KB."
        )



def validar_carga(answers, current):
    try:
        if int(current) <= 10 and int(current) > 0:
            return True
    except:
        raise errors.ValidationError(
            "", reason="La cantidad de procesos no debe ser mayor a 10."
        )
    

def validar_path(answers, current):
    file_path = Path(PurePath(current))

    if not Path.exists(file_path):
        raise errors.ValidationError(
            "",
            reason=f"El archivo '{file_path}', no existe o no ha podido ser encontrado.",
        )

    if Path.is_dir(file_path):
        raise errors.ValidationError("", reason=f"'{file_path}' es un directorio.")

    if file_path.suffix != ".csv" and file_path.suffix != ".json":
        raise errors.ValidationError(
            "", reason="El formato del archivo debe ser '.csv' o '.json'."
        )

    return True


def validar_positivo(answers, current):
    try:
        if int(current) >= 0:
            return True
    except:
        raise errors.ValidationError(
            "", reason="Algún valor no es un número positivo."
        )

def validar_mayor_a_cero(answers, current):
    try:
        if int(current) > 0:
            return True
    except:
        raise errors.ValidationError(
            "", reason="Algún valor es menor o igual a cero."
        )


def Prompt(ejecutar, interrumpir):
    preguntas = [
        inquirer.List(
            name="opción",
            message="Elija el modo de cargar el archivo",
            choices=["por Terminal", "por Archivo"],
        ),
    ]
    respuestas = inquirer.prompt(preguntas)
    if respuestas is not None:
        entrada = respuestas["opción"]
        if entrada is not None:
            if entrada == "por Archivo":
                respuesta = inquirer.prompt(
                    [
                        inquirer.Path(
                            "path",
                            message="Ingrese el directorio hacia el archivo",
                            path_type=inquirer.Path.FILE,
                            validate=validar_path,
                        ),
                    ]
                )
                if respuesta is not None:
                    file_path = Path(PurePath(respuesta["path"]))
                    cola_nuevos = leer_archivo(file_path, 10)
                    Run(cola_nuevos, ejecutar, interrumpir)
            else:
                preguntas = [
                    inquirer.Text(
                        name="pid",
                        message="ID",
                        validate=validar_mayor_a_cero,
                    ),
                    inquirer.Text(
                        name="tiempo_arribo",
                        message="Tiempo de arribo",
                        validate=validar_positivo,
                    ),
                    inquirer.Text(
                        name="tiempo_irrupcion",
                        message="Tiempo de irrupción",
                        validate=validar_mayor_a_cero,
                    ),
                    inquirer.Text(
                        name="tamaño",
                        message="Tamaño",
                        validate=validar_tamaño,
                    ),
                ]
                respuesta = inquirer.prompt(
                    [
                        inquirer.Text(
                            name="numero_procesos",
                            message="Ingrese el número de procesos que desea cargar (max.10)",
                            validate=validar_carga,
                        )
                    ]
                )
                if respuesta is not None:
                    numero = int(respuesta["numero_procesos"])
                    cola_nuevos = []
                    for i in range(1, numero + 1):
                        print("Progreso:", i, "/", numero)
                        respuestas = inquirer.prompt(preguntas)
                        if respuestas is not None:
                            datos = []
                            datos.append(int(respuestas["id"]))
                            datos.append(int(respuestas["tamanio"]))
                            datos.append(int(respuestas["tiempo_arribo"]))
                            datos.append(int(respuestas["tiempo_irrupcion"]))
                            cola_nuevos.append(BloqueProceso(datos))

                    clear_screen()
                    Run(cola_nuevos, ejecutar, interrumpir)

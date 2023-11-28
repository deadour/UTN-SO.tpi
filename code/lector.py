from pathlib import Path
import json
import csv


def leer_datos(file_path: Path) -> dict:
    """
    Devuelve un dictionary con el contenido del archivo.
    """
    file_extension = file_path.suffix.lower()

    if file_extension == ".csv":
        return csv_reader(file_path)
    elif file_extension == ".json":
        return json_reader(file_path)
    else:
        raise NotImplementedError(f"Tipo de archivo no compatible: {file_extension}")


def json_reader(file_path: Path) -> dict:
    data = {}

    with open(file_path, "r") as json_file:
        json_data = json.load(json_file)
        if isinstance(json_data, list):
            data = {i + 1: list(item.values()) for i, item in enumerate(json_data)}

    return data


def csv_reader(file_path: Path) -> dict:
    data = {}

    with open(file_path, newline="") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        data = {i + 1: [eval(cell) for cell in row] for i, row in enumerate(csv_reader)}

    return data
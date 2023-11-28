import sys, traceback, argparse
from pathlib import Path
from cargar_archivo import Prompt
from codigo import Run
from codigo import leer_archivo


def main() -> None:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage="%(prog)s [options] [filepath]",
    )
    parser.add_argument(
        "-f",
        "--full-run",
        action="store_true",
        help="Muestra la información en cada clock, esperando al usuario.",
    )
    parser.add_argument(
        "-i",
        "--ininterrumpido",
        action="store_true",
        help="Muestra la información sin esperar al usuario.",
    )
    parser.add_argument(
        "file_path",
        type=Path,
        nargs="?",
        default=None,
        help="Dirección del archivo con los procesos (opcional).",
    )
    args = parser.parse_args()

    try:
        if args.file_path is not None:
            cola_nuevos = leer_archivo(args.file_path, 10)
            Run(cola_nuevos, args.full_run, args.ininterrumpido)
        else:
            Prompt(args.full_run, args.ininterrumpido)

    except KeyboardInterrupt:
        print("\nFin.")
    except NotImplementedError:
        print("\nEl archivo de entrada debe ser '.csv' o '.json'.")
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)


if __name__ == "__main__":
    main()

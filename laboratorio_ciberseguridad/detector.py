
from collections import defaultdict
from datetime import datetime
from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "usuarios.db"
EVENTS_LOG = BASE_DIR / "eventos.log"

UMBRAL = 3
FORMATO = "%Y-%m-%d %H:%M:%S"


def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def leer_eventos():
    grupos = defaultdict(list)

    if not EVENTS_LOG.exists():
        return grupos

    with EVENTS_LOG.open("r", encoding="utf-8") as archivo:
        for linea in archivo:
            partes = linea.strip().split(",", 2)

            if len(partes) != 3:
                continue

            fecha, tipo, usuario = partes

            if tipo == "LOGIN_FALLIDO":
                try:
                    momento = datetime.strptime(fecha, FORMATO)
                    grupos[usuario].append(momento)
                except ValueError:
                    continue

    return grupos


def ejecutar_detector(mostrar=True):
    grupos = leer_eventos()

    if not grupos:
        if mostrar:
            print("No hay intentos fallidos registrados.")
        return 0

    nuevos = 0

    for usuario, intentos in grupos.items():

        if len(intentos) < UMBRAL:
            continue

        intentos.sort()

        primer_intento = intentos[0]
        deteccion = datetime.now()

        mttd = max(
            0.0,
            (deteccion - primer_intento).total_seconds()
        )

        clave = f"{usuario}|{primer_intento.strftime(FORMATO)}"

        with conectar() as conn:

            existente = conn.execute(
                "SELECT id FROM incidentes WHERE clave_evento = ?",
                (clave,)
            ).fetchone()

            if existente:
                continue

            cursor = conn.execute(
                """
                INSERT INTO incidentes
                (tipo, usuario, fecha_deteccion, estado,
                 severidad, mttd, clave_evento)
                VALUES (?, ?, ?, 'Detectado', 'Alta', ?, ?)
                """,
                (
                    "Intento de fuerza bruta",
                    usuario,
                    deteccion.strftime(FORMATO),
                    mttd,
                    clave
                )
            )

            incidente_id = cursor.lastrowid

            # Bloqueo simulado de la cuenta
            conn.execute(
                "UPDATE usuarios SET bloqueado = 1 WHERE usuario = ?",
                (usuario,)
            )

            # Registrar la detección sin resolver el incidente
            conn.execute(
                """
                INSERT INTO acciones
                (incidente_id, accion, evidencia, analista, fecha)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    incidente_id,
                    "Detección automática de fuerza bruta",
                    f"Se detectaron {len(intentos)} intentos fallidos.",
                    "detector.py",
                    deteccion.strftime(FORMATO)
                )
            )

        if mostrar:
            print("\n================================")
            print("       ALERTA DE SEGURIDAD")
            print("================================")
            print(f"Incidente: #{incidente_id}")
            print(f"Usuario: {usuario}")
            print(f"Intentos fallidos: {len(intentos)}")
            print(f"Primer intento: {primer_intento}")
            print(f"Detección: {deteccion}")
            print(f"MTTD: {mttd:.2f} segundos")
            print("Cuenta: bloqueada (simulación)")
            print("Estado: DETECTADO")
            print("Esperando atención del administrador...")
            print("================================")

        nuevos += 1

    if mostrar:
        if nuevos == 0:
            print("\nNo hay incidentes nuevos para procesar.")
        else:
            print(
                f"\nProceso terminado. Incidentes detectados: {nuevos}"
            )

    return nuevos


if __name__ == "__main__":
    ejecutar_detector()

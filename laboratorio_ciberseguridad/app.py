
from datetime import datetime
from functools import wraps
from pathlib import Path
import re
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

# Importar detector automático
from detector import ejecutar_detector


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "usuarios.db"
EVENTS_LOG = BASE_DIR / "eventos.log"

app = Flask(__name__)
app.secret_key = "cambia-esta-clave-por-una-clave-segura"


def conectar_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def ahora():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def registrar_evento(tipo, usuario):
    # Registrar eventos de inicio de sesión
    with open(EVENTS_LOG, "a", encoding="utf-8") as f:
        f.write(f"{ahora()},{tipo},{usuario}\n")


def inicializar_db():
    with conectar_db() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            correo TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            bloqueado INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS incidentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            usuario TEXT NOT NULL,
            fecha_deteccion TEXT NOT NULL,
            fecha_atencion TEXT,
            fecha_resolucion TEXT,
            estado TEXT NOT NULL DEFAULT 'Detectado',
            severidad TEXT NOT NULL DEFAULT 'Alta',
            analista TEXT,
            descripcion TEXT,
            mttd REAL,
            mttr REAL,
            clave_evento TEXT UNIQUE
        );

        CREATE TABLE IF NOT EXISTS acciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incidente_id INTEGER NOT NULL,
            accion TEXT NOT NULL,
            evidencia TEXT,
            analista TEXT NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY(incidente_id) REFERENCES incidentes(id)
        );
        """)

        # Migraciones para bases de datos anteriores
        columnas = {
            r["name"] for r in conn.execute(
                "PRAGMA table_info(usuarios)"
            )
        }

        if "bloqueado" not in columnas:
            conn.execute(
                "ALTER TABLE usuarios ADD COLUMN bloqueado INTEGER NOT NULL DEFAULT 0"
            )

        columnas = {
            r["name"] for r in conn.execute(
                "PRAGMA table_info(incidentes)"
            )
        }

        migraciones = {
            "severidad": "TEXT NOT NULL DEFAULT 'Alta'",
            "analista": "TEXT",
            "descripcion": "TEXT",
            "clave_evento": "TEXT"
        }

        for nombre, tipo in migraciones.items():
            if nombre not in columnas:
                conn.execute(
                    f"ALTER TABLE incidentes ADD COLUMN {nombre} {tipo}"
                )

        conn.commit()


def login_requerido(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "usuario" not in session:
            flash("Inicia sesión para acceder al panel.")
            return redirect(url_for("login"))

        return func(*args, **kwargs)

    return wrapper


def validar_usuario(usuario):
    return bool(
        re.fullmatch(r"[A-Za-z0-9_]{4,20}", usuario)
    )


def validar_correo(correo):
    return bool(
        re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo)
    )


def validar_password(password):
    return len(password) >= 8


@app.route("/")
def inicio():
    return redirect(
        url_for("incidentes")
        if "usuario" in session
        else url_for("login")
    )


@app.route("/registro", methods=["GET", "POST"])
def registro():

    if request.method == "POST":

        usuario = request.form.get("usuario", "").strip()
        correo = request.form.get("correo", "").strip().lower()
        password = request.form.get("password", "")

        if not validar_usuario(usuario):
            flash(
                "El usuario debe tener entre 4 y 20 caracteres: "
                "letras, números o guion bajo."
            )
            return render_template("registro.html")

        if not validar_correo(correo):
            flash("Ingresa un correo electrónico válido.")
            return render_template("registro.html")

        if not validar_password(password):
            flash("La contraseña debe tener al menos 8 caracteres.")
            return render_template("registro.html")

        try:
            with conectar_db() as conn:

                conn.execute(
                    """
                    INSERT INTO usuarios (usuario, correo, password)
                    VALUES (?, ?, ?)
                    """,
                    (
                        usuario,
                        correo,
                        generate_password_hash(password)
                    )
                )

            flash(
                "Usuario registrado correctamente. "
                "Ya puedes iniciar sesión."
            )

            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            flash("El usuario o correo ya está registrado.")

    return render_template("registro.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form.get("usuario", "").strip()
        password = request.form.get("password", "")

        with conectar_db() as conn:

            cuenta = conn.execute(
                """
                SELECT id, usuario, password, bloqueado
                FROM usuarios
                WHERE usuario = ?
                """,
                (usuario,)
            ).fetchone()

        if cuenta and cuenta["bloqueado"]:

            registrar_evento("LOGIN_BLOQUEADO", usuario)

            flash(
                "La cuenta está bloqueada por una alerta de seguridad. "
                "Contacta al administrador."
            )

            return render_template("login.html")

        if cuenta and check_password_hash(
            cuenta["password"], password
        ):

            session.clear()
            session["usuario"] = cuenta["usuario"]

            registrar_evento("LOGIN_CORRECTO", usuario)

            flash("Inicio de sesión correcto.")

            return redirect(url_for("incidentes"))

        registrar_evento(
            "LOGIN_FALLIDO",
            usuario if usuario else "desconocido"
        )

        flash("Credenciales incorrectas.")

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    flash("Sesión cerrada.")

    return redirect(url_for("login"))


@app.route("/incidentes")
@login_requerido
def incidentes():

    # Ejecutar detección automática antes de consultar los incidentes
    ejecutar_detector(mostrar=False)

    with conectar_db() as conn:

        registros = conn.execute(
            "SELECT * FROM incidentes ORDER BY id DESC"
        ).fetchall()

        total = conn.execute(
            "SELECT COUNT(*) FROM incidentes"
        ).fetchone()[0]

        detectados = conn.execute(
            "SELECT COUNT(*) FROM incidentes WHERE estado='Detectado'"
        ).fetchone()[0]

        atencion = conn.execute(
            "SELECT COUNT(*) FROM incidentes WHERE estado='En atención'"
        ).fetchone()[0]

        resueltos = conn.execute(
            "SELECT COUNT(*) FROM incidentes WHERE estado='Resuelto'"
        ).fetchone()[0]

        mttd = conn.execute(
            "SELECT AVG(mttd) FROM incidentes WHERE mttd IS NOT NULL"
        ).fetchone()[0]

        mttr = conn.execute(
            "SELECT AVG(mttr) FROM incidentes WHERE mttr IS NOT NULL"
        ).fetchone()[0]

    return render_template(
        "incidentes.html",
        incidentes=registros,
        total=total,
        detectados=detectados,
        atencion=atencion,
        resueltos=resueltos,
        mttd=mttd or 0,
        mttr=mttr or 0
    )


@app.route("/incidentes/<int:id>")
@login_requerido
def detalle_incidente(id):

    with conectar_db() as conn:

        incidente = conn.execute(
            "SELECT * FROM incidentes WHERE id=?",
            (id,)
        ).fetchone()

        if not incidente:
            flash("No se encontró el incidente.")
            return redirect(url_for("incidentes"))

        acciones = conn.execute(
            """
            SELECT * FROM acciones
            WHERE incidente_id=?
            ORDER BY id DESC
            """,
            (id,)
        ).fetchall()

    return render_template(
        "detalle_incidente.html",
        incidente=incidente,
        acciones=acciones
    )


@app.route("/incidentes/<int:id>/actualizar", methods=["POST"])
@login_requerido
def actualizar_incidente(id):

    severidad = request.form.get("severidad", "Media")
    analista = request.form.get("analista", "").strip()[:80]
    descripcion = request.form.get("descripcion", "").strip()[:2000]

    if severidad not in {"Crítica", "Alta", "Media", "Baja"}:

        flash("Severidad no válida.")

    else:

        with conectar_db() as conn:

            conn.execute(
                """
                UPDATE incidentes
                SET severidad=?, analista=?, descripcion=?
                WHERE id=?
                """,
                (severidad, analista, descripcion, id)
            )

        flash("Información del incidente actualizada.")

    return redirect(url_for("detalle_incidente", id=id))


@app.route("/incidentes/<int:id>/accion", methods=["POST"])
@login_requerido
def registrar_accion(id):

    accion = request.form.get("accion", "").strip()[:1000]
    evidencia = request.form.get("evidencia", "").strip()[:2000]

    if not accion:

        flash("Describe la acción realizada.")

    else:

        with conectar_db() as conn:

            existe = conn.execute(
                "SELECT id FROM incidentes WHERE id=?",
                (id,)
            ).fetchone()

            if existe:

                conn.execute(
                    """
                    INSERT INTO acciones
                    (incidente_id, accion, evidencia, analista, fecha)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        id,
                        accion,
                        evidencia,
                        session["usuario"],
                        ahora()
                    )
                )

                flash("Acción registrada en la bitácora.")

            else:

                flash("Incidente no encontrado.")

    return redirect(url_for("detalle_incidente", id=id))


@app.route("/incidentes/<int:id>/atender", methods=["POST"])
@login_requerido
def atender_incidente(id):

    with conectar_db() as conn:

        conn.execute(
            """
            UPDATE incidentes
            SET estado='En atención',
                fecha_atencion=COALESCE(fecha_atencion, ?),
                analista=COALESCE(NULLIF(analista,''), ?)
            WHERE id=? AND estado='Detectado'
            """,
            (ahora(), session["usuario"], id)
        )

    flash("El incidente pasó a estado En atención.")

    return redirect(
        request.referrer or url_for("incidentes")
    )


@app.route("/incidentes/<int:id>/resolver", methods=["POST"])
@login_requerido
def resolver_incidente(id):

    fecha = ahora()

    with conectar_db() as conn:

        row = conn.execute(
            """
            SELECT fecha_atencion, fecha_deteccion
            FROM incidentes
            WHERE id=?
            """,
            (id,)
        ).fetchone()

        if row:

            inicio = row["fecha_atencion"] or row["fecha_deteccion"]

            try:

                mttr = (
                    datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
                    - datetime.strptime(inicio, "%Y-%m-%d %H:%M:%S")
                ).total_seconds()

            except (TypeError, ValueError):

                mttr = None

            conn.execute(
                """
                UPDATE incidentes
                SET estado='Resuelto',
                    fecha_atencion=COALESCE(fecha_atencion, ?),
                    fecha_resolucion=?,
                    mttr=?
                WHERE id=?
                """,
                (fecha, fecha, mttr, id)
            )

    flash("Incidente marcado como resuelto.")

    return redirect(
        request.referrer or url_for("incidentes")
    )


if __name__ == "__main__":

    inicializar_db()

    app.run(debug=True)

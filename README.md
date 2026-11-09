# Laboratorio: Código Seguro y Modelo OWASP

## 1. Datos generales

- **Nombre completo:** Sara Yamileth Torres Henríquez
- **Carné:** TSU-C001
- **Correo electrónico:** sara.torres2710@gmail.com
- **Asignatura:** Lenguajes de Programación con Aspectos de Seguridad
- **Fecha:** 8 de noviembre de 2026

## 2. Descripción

Este laboratorio consiste en desarrollar una aplicación web utilizando Python y Flask, implementando controles básicos de seguridad basados en buenas prácticas y el modelo OWASP.

La aplicación incorpora mecanismos de validación de entradas, consultas parametrizadas a una base de datos SQLite, protección de contraseñas mediante funciones de hash, registro de eventos de autenticación y detección de incidentes de seguridad.

Además, permite identificar múltiples intentos fallidos de inicio de sesión, generar incidentes de seguridad, bloquear usuarios involucrados y registrar acciones de respuesta.

El sistema también permite calcular las métricas de seguridad MTTD y MTTR:

- **MTTD (Mean Time To Detect):** mide el tiempo transcurrido desde que ocurre un evento de seguridad hasta que es detectado.
- **MTTR (Mean Time To Respond/Resolve):** mide el tiempo transcurrido desde la detección o atención del incidente hasta su resolución.

### Tecnologías utilizadas

- Python
- Flask
- SQLite
- HTML5
- CSS3
- JavaScript
- Werkzeug

## 3. Estructura del proyecto

```text
laboratorio-ciberseguridad/
│
├── app.py
├── detector.py
├── crearDB.py
├── requirements.txt
├── README.md
├── eventos.log
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── registro.html
│   ├── incidentes.html
│   └── detalle_incidente.html
│
└── static/
    └── style.css
```

### Descripción de los archivos principales

| Archivo | Descripción |
|---|---|
| `app.py` | Aplicación principal desarrollada con Flask. Gestiona usuarios, autenticación e incidentes. |
| `detector.py` | Analiza los eventos registrados y detecta múltiples intentos fallidos de inicio de sesión. |
| `crearDB.py` | Inicializa la base de datos SQLite. |
| `requirements.txt` | Contiene las dependencias necesarias para ejecutar el proyecto. |
| `eventos.log` | Almacena los eventos de autenticación. |
| `templates/` | Contiene las plantillas HTML de la aplicación. |
| `static/` | Contiene los archivos de estilos CSS. |

## 4. Ejecución del proyecto

### Requisitos previos

Para ejecutar el proyecto se necesita:

- Python 3.10 o superior.
- Git.
- Un navegador web.
- Editor de código, como Visual Studio Code.

### Paso 1. Clonar el repositorio

Abrir una terminal y ejecutar:

```bash
git clone https://github.com/Saratorres17/laboratorio-ciberseguridad.git
```

### Paso 2. Ingresar a la carpeta del proyecto

```bash
cd laboratorio-ciberseguridad
```

### Paso 3. Crear un entorno virtual

```bash
python -m venv venv
```

### Paso 4. Activar el entorno virtual

En Windows:

```bash
venv\Scripts\activate
```

En Linux o macOS:

```bash
source venv/bin/activate
```

### Paso 5. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### Paso 6. Inicializar la base de datos

```bash
python crearDB.py
```

Este comando crea e inicializa la base de datos SQLite necesaria para el funcionamiento de la aplicación.

### Paso 7. Ejecutar la aplicación

```bash
python app.py
```

### Paso 8. Acceder al sistema

Abrir el navegador e ingresar a la siguiente dirección:

```text
http://127.0.0.1:5000
```

Desde esta dirección se podrá acceder al sistema, registrar usuarios e iniciar sesión.

## 5. Pruebas del laboratorio

Para comprobar el funcionamiento de la aplicación se deben realizar diferentes escenarios de prueba.

### Escenario 1. Registro e inicio de sesión exitoso

1. Ingresar a la aplicación.
2. Seleccionar la opción de registro.
3. Crear un usuario con sus datos correspondientes.
4. Iniciar sesión utilizando las credenciales correctas.
5. Comprobar que el acceso sea permitido.

**Resultado esperado:** el sistema permite registrar al usuario y acceder correctamente a la aplicación, almacenando la contraseña mediante un mecanismo de hash.

### Escenario 2. Detección de intentos fallidos

1. Registrar un usuario de prueba.
2. Intentar iniciar sesión utilizando una contraseña incorrecta.
3. Repetir el procedimiento hasta completar tres intentos fallidos.
4. Acceder al panel de incidentes.
5. Verificar que se haya generado un incidente de seguridad.

**Resultado esperado:** el sistema detecta los intentos fallidos, genera un incidente y bloquea al usuario correspondiente.

### Escenario 3. Atención y resolución del incidente

1. Ingresar al panel de incidentes.
2. Seleccionar el incidente generado.
3. Consultar los detalles del evento.
4. Registrar la información de atención y la acción realizada.
5. Completar la resolución del incidente.
6. Verificar el registro de la acción y el cálculo del MTTR.

**Resultado esperado:** el sistema almacena la acción de respuesta y calcula el tiempo de resolución del incidente.

### Métricas de seguridad

**MTTD – Tiempo medio de detección**

Permite medir cuánto tiempo tarda el sistema en identificar un evento de seguridad desde que ocurre.

**MTTR – Tiempo medio de resolución**

Permite medir cuánto tiempo transcurre desde la detección o atención del incidente hasta que se registra su resolución.

### Evidencias esperadas

- Registro de usuarios.
- Inicio de sesión exitoso.
- Registro de intentos fallidos en `eventos.log`.
- Detección y generación de incidentes.
- Bloqueo del usuario involucrado.
- Registro de acciones de respuesta.
- Cálculo de las métricas MTTD y MTTR.

---

## Repositorio del proyecto

**GitHub:** https://github.com/Saratorres17/laboratorio-ciberseguridad

**Estudiante:** Sara Yamileth Torres Henríquez

**Carné:** TSU-C001

# 🛡️ Laboratorio de Ciberseguridad — Flask, SQLite, MTTD y MTTR

Sistema web académico para la detección y respuesta ante incidentes de seguridad informática, desarrollado con Python, Flask y SQLite.

El laboratorio permite registrar usuarios, monitorear eventos de autenticación, detectar posibles ataques de fuerza bruta, simular el bloqueo de cuentas y gestionar incidentes de seguridad mediante indicadores MTTD y MTTR.

## 📋 Requisitos

- Python 3.10 o superior.
- Windows, macOS o Linux.
- Conexión a Internet para cargar Chart.js en el dashboard.
- Visual Studio Code (recomendado).

## ⚙️ Instalación en Windows PowerShell

Abre PowerShell dentro de la carpeta del proyecto y ejecuta los siguientes comandos:

**1. Crear el entorno virtual**

```powershell
py -m venv venv
```

**2. Activar el entorno virtual**

```powershell
.\venv\Scripts\Activate.ps1
```

**3. Instalar las dependencias**

```powershell
pip install -r requirements.txt
```

**4. Crear la base de datos**

```powershell
python crearDB.py
```

**5. Ejecutar la aplicación**

```powershell
python app.py
```

Abre el navegador en:

http://127.0.0.1:5000/registro

Registra un usuario y posteriormente inicia sesión.

### Solución a problemas de ejecución en PowerShell

Si PowerShell impide activar el entorno virtual, ejecuta:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Después vuelve a activar el entorno:

```powershell
.\venv\Scripts\Activate.ps1
```

## 🔍 Prueba de detección y respuesta

Para comprobar el funcionamiento del laboratorio, realiza el siguiente escenario:

1. Registra un usuario, por ejemplo `usuario_01`.
2. Inicia sesión correctamente para comprobar el registro `LOGIN_CORRECTO`.
3. Cierra sesión.
4. Intenta iniciar sesión tres veces con una contraseña incorrecta utilizando `usuario_01`.
5. Abre otra terminal dentro de la carpeta del proyecto y ejecuta:

```powershell
python detector.py
```

6. Comprueba la alerta generada, el cálculo del MTTD y la simulación del bloqueo.
7. Actualiza el dashboard para consultar el incidente registrado y su estado.
8. Repite el procedimiento con otros usuarios para generar escenarios adicionales.

## 📊 Indicadores de seguridad

**MTTD — Mean Time To Detect**

Representa el tiempo transcurrido desde el primer intento fallido registrado hasta la detección del incidente.

**MTTR — Mean Time To Respond**

Representa el tiempo transcurrido desde la detección hasta la acción de respuesta registrada.

Estos indicadores permiten evaluar los tiempos de detección y respuesta ante incidentes de seguridad.

## 📁 Archivos de registro

| Archivo | Descripción |
|---|---|
| `eventos.log` | Registra eventos LOGIN_CORRECTO, LOGIN_FALLIDO y LOGIN_BLOQUEADO. |
| `respuesta.log` | Almacena las acciones de bloqueo simulado. |
| `usuarios.db` | Base de datos con usuarios, incidentes y bitácora. |

## 🧪 Escenarios de prueba

Para obtener tres escenarios independientes:

- Utiliza tres cuentas diferentes.
- Realiza tres intentos fallidos por cada cuenta.
- Ejecuta el detector para procesar los eventos.
- Registra los resultados de MTTD y MTTR.
- Calcula los promedios de ambos indicadores.

## 🔐 Consideraciones académicas

- El bloqueo es una simulación local: el detector marca la cuenta como bloqueada en SQLite.
- El MTTD se calcula desde el primer intento fallido registrado hasta la ejecución del detector.
- El MTTR se calcula desde la detección hasta la acción de respuesta registrada.
- Para repetir pruebas, utiliza cuentas distintas o restablece el estado de prueba mediante una copia de seguridad de la base de datos.
- No publiques claves secretas de desarrollo ni utilices esta aplicación como sistema de producción.

## 🛠️ Tecnologías utilizadas

- Python
- Flask
- SQLite
- HTML5
- CSS3
- JavaScript
- Chart.js

## 👩‍💻 Autor

**Sara Torres**

Proyecto académico de laboratorio de ciberseguridad.

**Repositorio:**  
https://github.com/Saratorres17/laboratorio-ciberseguridad

---

*Laboratorio de Ciberseguridad — Detección y Respuesta ante Incidentes (MTTD / MTTR).*
<img width="662" height="191" alt="image" src="https://github.com/user-attachments/assets/f1a64312-a7b4-4c20-abe4-b537565ee880" />

# Laboratorio de Ciberseguridad — Flask, SQLite, MTTD y MTTR

## Requisitos
- Python 3.10 o superior
- Windows, macOS o Linux
- Conexión a Internet para cargar Chart.js en el dashboard (el resto funciona localmente)

## Instalación en Windows PowerShell
Abre PowerShell dentro de esta carpeta y ejecuta:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python crearDB.py
python app.py
```

Abre `http://127.0.0.1:5000/registro`, registra un usuario y luego inicia sesión.

Si PowerShell impide activar el entorno virtual, ejecuta:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

## Prueba de detección y respuesta
1. Registra un usuario, por ejemplo `usuario_01`.
2. Inicia sesión una vez correctamente para comprobar `LOGIN_CORRECTO`.
3. Cierra sesión.
4. Intenta iniciar sesión tres veces con una contraseña incorrecta usando `usuario_01`.
5. En otra terminal, dentro de la carpeta del proyecto, ejecuta:
   ```powershell
   python detector.py
   ```
6. El detector debe imprimir la alerta, MTTD, bloqueo simulado y MTTR.
7. Actualiza el dashboard. El incidente aparecerá registrado como resuelto por la respuesta simulada.
8. Repite con otro usuario para crear más escenarios.

## Archivos de registro
- `eventos.log`: eventos LOGIN_CORRECTO, LOGIN_FALLIDO y LOGIN_BLOQUEADO.
- `respuesta.log`: acciones de bloqueo simulado.
- `usuarios.db`: usuarios, incidentes y bitácora.

## Consideraciones académicas
- El bloqueo es una simulación local del laboratorio: el detector marca la cuenta como bloqueada en SQLite.
- MTTD se calcula desde el primer intento fallido registrado hasta la ejecución del detector.
- MTTR se calcula desde la detección hasta la acción de respuesta registrada.
- Para obtener tres escenarios independientes, utiliza tres cuentas distintas o restablece el estado de prueba con una copia de seguridad de la base de datos.
- No publiques la clave `secret_key` de desarrollo ni uses esta aplicación como sistema de producción.

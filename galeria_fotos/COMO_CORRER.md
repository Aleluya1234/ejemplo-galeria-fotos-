# Cómo correr la Galería Fotográfica — paso a paso

Guía para dejar la app funcionando en tu computador. Sirve para Windows,
macOS y Linux. Solo necesitas **Python 3.10 o superior** y un terminal.

> ¿No sabes qué Python tienes? Ejecuta `python --version` (Windows) o
> `python3 --version` (macOS/Linux). Si no está, descárgalo de
> https://www.python.org/downloads/ y en Windows marca **"Add Python to PATH"**.

---

## 1. Abrir un terminal en la carpeta del proyecto

La carpeta es la que contiene `manage.py`.

- **Windows:** abre la carpeta en el Explorador, haz clic en la barra de
  dirección, escribe `cmd` y Enter. También sirve *PowerShell* o el terminal
  de VS Code.
- **macOS:** en Finder, clic derecho sobre la carpeta → *Servicios* →
  *Nuevo terminal en la carpeta* (o arrastra la carpeta a la ventana de Terminal).
- **VS Code (cualquier sistema):** *Archivo → Abrir carpeta* → `galeria_fotos`,
  luego *Terminal → Nuevo terminal*.

Verifica que estás en el lugar correcto:

```bash
dir        # Windows      → debe aparecer manage.py
ls         # macOS/Linux  → debe aparecer manage.py
```

## 2. Crear y activar el entorno virtual

Un entorno virtual es una carpeta `.venv` con su propio Python y sus propias
librerías, para no mezclar las de este proyecto con las de otros.

**Windows (cmd o PowerShell):**
```bat
python -m venv .venv
.venv\Scripts\activate
```
Si PowerShell dice que "la ejecución de scripts está deshabilitada":
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
y vuelve a activar.

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Sabrás que está activo porque el prompt del terminal empieza con `(.venv)`.
**Cada vez que abras un terminal nuevo tienes que volver a activarlo.**

## 3. Instalar Django

```bash
pip install -r requirements.txt
```

Comprueba:
```bash
python -m django --version     # debe mostrar 5.x
```

## 4. Crear la base de datos

Django usa **SQLite**: un solo archivo `db.sqlite3` que se crea aquí mismo,
no hay que instalar ningún motor de base de datos.

```bash
python manage.py migrate
```

Esto ejecuta las *migraciones*: crea la tabla `galeria_foto` (nuestro modelo)
y las tablas de usuarios, sesiones y admin que Django trae.

## 5. Cargar datos de ejemplo (opcional pero recomendado)

```bash
python manage.py poblar
```

Crea:
- el usuario **`profe`** con contraseña **`inacap2026`** (es superusuario: entra al admin), y
- 8 fotos de ejemplo tomadas de https://picsum.photos.

Si prefieres crear tu propio superusuario:
```bash
python manage.py createsuperuser
```

## 6. Levantar el servidor de desarrollo

```bash
python manage.py runserver
```

Verás algo como `Starting development server at http://127.0.0.1:8000/`.
Deja ese terminal abierto; para detener el servidor presiona **Ctrl + C**.

Si el puerto 8000 está ocupado, usa otro: `python manage.py runserver 8080`.

## 7. Usar la app

| Qué | Dirección |
|---|---|
| Galería (lista de fotos) | http://127.0.0.1:8000/ |
| Ver una foto | http://127.0.0.1:8000/1/ |
| Nueva foto (pide login) | http://127.0.0.1:8000/nueva/ |
| Editar / borrar (piden login) | http://127.0.0.1:8000/1/editar/ · http://127.0.0.1:8000/1/borrar/ |
| Iniciar sesión | http://127.0.0.1:8000/accounts/login/ |
| Registrarse | http://127.0.0.1:8000/accounts/registro/ |
| Django Admin | http://127.0.0.1:8000/admin/ |

Flujo típico para probar el CRUD completo:

1. Entra a la galería: ves las 8 fotos sin iniciar sesión (READ).
2. Haz clic en **Nueva foto** → te redirige al login. Entra con `profe` /
   `inacap2026` (o regístrate) y vuelves solo al formulario.
3. Pega una URL de imagen, por ejemplo `https://picsum.photos/id/237/800/600`
   (cambia el número para otra foto), ponle título y **Guardar** (CREATE).
4. Abre la foto, **Editar**, cambia el título, guarda (UPDATE).
5. **Borrar** → confirma (DELETE).
6. Entra a `/admin/` y mira la misma tabla desde el panel de administración.

## 8. Ver el ORM en acción (Bloque 1 de la clase)

```bash
python manage.py shell < demo_orm.py
```

O abre el shell interactivo y ve pegando las líneas de `demo_orm.py`:
```bash
python manage.py shell
>>> from galeria.models import Foto
>>> Foto.objects.all()
```

## 9. Correr los tests

```bash
python manage.py test
```

Debe terminar en `OK` con 12 tests. Cada test corresponde a un tema de la
clase (ORM, ModelForm, vistas genéricas, login, CSRF, registro).

---

## Problemas frecuentes

| Síntoma | Causa y solución |
|---|---|
| `'python' no se reconoce como un comando` | Python no está en el PATH. Reinstala marcando *Add Python to PATH*, o usa `py` en vez de `python` en Windows. |
| `No module named django` | El entorno virtual no está activo (no ves `(.venv)`) o no instalaste requirements. Activa y repite el paso 3. |
| `no such table: galeria_foto` | Falta el paso 4: `python manage.py migrate`. |
| Página `403 Forbidden · CSRF verification failed` | Un formulario POST sin `{% csrf_token %}`. Revísalo en el template. |
| `Error: That port is already in use` | Otro `runserver` sigue abierto. Ciérralo con Ctrl+C o usa `runserver 8080`. |
| Las imágenes no cargan | La URL no es pública o no es `https://`. Prueba con `https://picsum.photos/id/10/800/600`. |
| Quiero empezar de cero | Detén el servidor, borra `db.sqlite3` y repite los pasos 4 y 5. |

## Estructura mínima que debes conocer

```
galeria_fotos/
├── manage.py            ← todos los comandos pasan por aquí
├── db.sqlite3           ← la base de datos (se crea con migrate)
├── galeria_fotos/       ← configuración: settings.py, urls.py
└── galeria/             ← la app: models.py, forms.py, views.py, urls.py, templates/
```

Para entender qué hace cada archivo y cómo se relaciona con la clase,
lee el [README.md](README.md).

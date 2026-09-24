# Galería Fotográfica — proyecto guía de la Semana 5

Proyecto Django que acompaña la presentación **"CRUD con Django ORM, Formularios y
Seguridad"** (Programación Back End · TI3V41). Es una galería donde cada *post*
es una **foto**: tiene un título, la **URL de la imagen** (no se suben archivos,
se pega el enlace), una descripción y un autor. Se puede crear, ver, editar y
borrar: el CRUD completo.

## Puesta en marcha

> Guía detallada paso a paso (Windows/macOS, entorno virtual, problemas
> frecuentes): **[COMO_CORRER.md](COMO_CORRER.md)**.

```bash
cd galeria_fotos
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate           # crea la base de datos (SQLite)
python manage.py poblar            # usuario profe/inacap2026 + 8 fotos de ejemplo
python manage.py runserver
```

- Galería: http://127.0.0.1:8000/
- Admin:   http://127.0.0.1:8000/admin/  (profe / inacap2026)
- Registro: http://127.0.0.1:8000/accounts/registro/  (cualquier alumno puede crear su cuenta)
- Tests:   `python manage.py test`  (12 tests, uno por cada idea de la clase)

Para probar URLs de fotos: `https://picsum.photos/id/<número>/800/600`
(cambia el número: 10, 237, 1025, 1043…).

## Mapa de la clase → archivos del proyecto

| Bloque | Slide | Tema | Dónde está en el proyecto |
|---|---|---|---|
| 1 | 4 | El modelo: una tabla, cada objeto una fila | [`galeria/models.py`](galeria/models.py) → `class Foto` |
| 1 | 5–7 | CREATE / READ / UPDATE / DELETE en el shell | [`demo_orm.py`](demo_orm.py) → `python manage.py shell < demo_orm.py` |
| 1 | 6 | QuerySet perezoso, `filter`, lookups | `FotoList.get_queryset()` en [`galeria/views.py`](galeria/views.py) |
| 2 | 9 | ModelForm: `class Meta`, `fields` | [`galeria/forms.py`](galeria/forms.py) → `FotoForm` (+ `clean_url_imagen`) |
| 2 | 10 | Vista de función, patrón GET/POST, `is_valid()` / `save()` | `crear_foto()` en [`galeria/views.py`](galeria/views.py) · ruta `/nueva/funcion/` |
| 2 | 11 | Template: `{% csrf_token %}` y `{{ form.as_p }}` | [`galeria/templates/galeria/foto_form.html`](galeria/templates/galeria/foto_form.html) |
| 3 | 13–14 | ListView, DetailView, CreateView, UpdateView, DeleteView | `FotoList`, `FotoDetail`, `FotoCreate`, `FotoUpdate`, `FotoDelete` en [`galeria/views.py`](galeria/views.py) |
| 3 | 14 | Convención de nombres de templates | [`galeria/templates/galeria/`](galeria/templates/galeria/) → `foto_list`, `foto_detail`, `foto_form`, `foto_confirm_delete` |
| 3 | 15 | `urls.py`, `.as_view()`, `<int:pk>` | [`galeria/urls.py`](galeria/urls.py) |
| 4 | 17 | `@login_required` (función) y `LoginRequiredMixin` (clase) | [`galeria/views.py`](galeria/views.py) · `LOGIN_URL` en [`settings.py`](galeria_fotos/settings.py) |
| 4 | 18 | Sesiones: `user.is_authenticated`, `user.username` | cabecera de [`galeria/templates/base.html`](galeria/templates/base.html) · login en [`registration/login.html`](galeria/templates/registration/login.html) |
| 4 | — | Registro con `UserCreationForm` (formulario propio de Django) | `registro()` en [`galeria/views.py`](galeria/views.py) · [`registration/registro.html`](galeria/templates/registration/registro.html) |
| 4 | 19 | CSRF: token en todo form POST, 403 sin él | todos los `<form method="post">` · test `test_post_sin_csrf_da_403` |
| Act. | 20 | Modelo registrado en Django Admin | [`galeria/admin.py`](galeria/admin.py) |

## Guion sugerido para la clase

1. **Bloque 1 · ORM.** Abrir `models.py`, explicar `Foto`. Luego en vivo:
   `python manage.py shell` e ir copiando `demo_orm.py` por secciones
   (crear con `save()` y con `create()`, `all()`, `filter()`, `get()`,
   `order_by()`, `exists()`, update y delete individual y masivo).
   Mostrar `qs.query` para que vean el SQL que genera Django.
2. **Bloque 2 · ModelForm.** `forms.py` y la vista `crear_foto`. Abrir
   `/nueva/funcion/` y crear una foto. Quitar `{% csrf_token %}` del template,
   volver a enviar y mostrar el **403** (adelanto del Bloque 4). Escribir una
   URL `http://` para ver la validación de `clean_url_imagen`.
3. **Bloque 3 · Vistas genéricas.** Comparar `crear_foto` (12 líneas) con
   `FotoCreate` (5 líneas). Recorrer las 5 clases y `urls.py`. Ejercicio:
   comentar `.as_view()` en una ruta y ver el error.
4. **Bloque 4 · Seguridad.** Cerrar sesión e intentar `/nueva/`: redirige a
   `/accounts/login/?next=/nueva/`. Entrar y ver que vuelve solo. Mostrar la
   cookie `sessionid` en las DevTools del navegador (Application → Cookies) y
   el `<input type="hidden" name="csrfmiddlewaretoken">` en el HTML del form.
5. Correr `python manage.py test` y leer los nombres de los tests: son el
   checklist de la actividad de entrega.

## Estructura

```
galeria_fotos/
├── manage.py
├── demo_orm.py                    ← Bloque 1: CRUD en el shell
├── requirements.txt
├── galeria_fotos/                 ← configuración del proyecto
│   ├── settings.py                  (LOGIN_URL, LOGIN_REDIRECT_URL)
│   └── urls.py                      (admin/, accounts/login, accounts/registro, galería)
└── galeria/                       ← la app
    ├── models.py                    Foto
    ├── forms.py                     FotoForm (ModelForm)
    ├── views.py                     crear_foto + 5 vistas genéricas + registro
    ├── urls.py
    ├── admin.py
    ├── tests.py                     12 tests, uno por bloque
    ├── management/commands/poblar.py
    └── templates/
        ├── base.html                header + navbar + footer, sesión (login / logout)
        ├── galeria/                 foto_list · foto_detail · foto_form · foto_confirm_delete
        └── registration/            login.html · registro.html
```

## Ideas para extender (para los alumnos)

- Que solo el **autor** pueda editar/borrar su foto (`UserPassesTestMixin`).
- Un campo `etiquetas` y un buscador con `filter(titulo__icontains=...)`.
- Perfil de usuario con avatar y listado "mis fotos" (`request.user.fotos.all()`).
- Reemplazar la URL por un `ImageField` y subir el archivo (requiere `MEDIA_ROOT`).

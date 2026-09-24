"""
Bloque 1 · ORM y CRUD en el shell de Django (slides 5, 6 y 7)

Es el mismo recorrido de la presentación (Producto) pero con nuestra Foto.
Se puede ejecutar completo:

    python manage.py shell < demo_orm.py

o ir copiando línea a línea dentro de `python manage.py shell` para mostrarlo
en vivo. Al final deja la base de datos como estaba.
"""
from galeria.models import Foto

print("\n── CREATE ──────────────────────────────────────────")
# Opción 1: crear y guardar en dos pasos
f = Foto(titulo="Demo · Montaña", url_imagen="https://picsum.photos/id/29/800/600")
f.save()                                    # sin save() vive solo en memoria
# Opción 2: crear y guardar en un solo paso
Foto.objects.create(titulo="Demo · Mar", url_imagen="https://picsum.photos/id/1011/800/600")
Foto.objects.create(titulo="Demo · Bosque", url_imagen="https://picsum.photos/id/28/800/600", publicada=False)
print("creadas:", f, "y dos más")

print("\n── READ ────────────────────────────────────────────")
qs = Foto.objects.all()                     # QuerySet perezoso: aún NO consulta
print("SQL que generará:", qs.query)
print("all():", list(qs))                   # recién aquí golpea la BD

print("filter(publicada=True):", Foto.objects.filter(publicada=True).count())
print("get(id=%d):" % f.id, Foto.objects.get(id=f.id))          # error si no existe
print("order_by('titulo'):", [x.titulo for x in Foto.objects.order_by("titulo")])
print("exists() 'Mar':", Foto.objects.filter(titulo__icontains="mar").exists())

# Lookups útiles: __gt / __lt, __icontains, __startswith
print("startswith 'Demo':", Foto.objects.filter(titulo__startswith="Demo").count())

print("\n── UPDATE ──────────────────────────────────────────")
# Un objeto: cambiar y save()
f.titulo = "Demo · Montaña (editada)"
f.save()
print("editada:", Foto.objects.get(id=f.id))
# Masivo: una sola consulta SQL, sin save() por objeto
n = Foto.objects.filter(publicada=False).update(publicada=True)
print("publicadas en masa:", n)

print("\n── DELETE ──────────────────────────────────────────")
f.delete()                                  # un objeto
print("borrada la editada; quedan demo:", Foto.objects.filter(titulo__startswith="Demo").count())
borradas, _ = Foto.objects.filter(titulo__startswith="Demo").delete()   # varias con filtro
print("borradas en masa:", borradas, "→ quedan demo:", Foto.objects.filter(titulo__startswith="Demo").count())

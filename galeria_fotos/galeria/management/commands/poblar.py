"""
Carga datos de ejemplo para tener algo que mostrar en clase:

    python manage.py poblar

Crea el usuario `profe` (clave `inacap2026`) si no existe y 8 fotos de
picsum.photos. Usa el ORM tal como se ve en el Bloque 1 (create / exists).
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from galeria.models import Foto

FOTOS = [
    ("Amanecer en la cordillera", 29,   "Primeras luces sobre los Andes."),
    ("Costa al atardecer",        1011, "Olas rompiendo al final del día."),
    ("Bosque húmedo",             28,   "Sendero entre helechos y musgo."),
    ("Ciudad de noche",           1031, "Luces largas en la avenida."),
    ("Desierto florido",          1043, "Norte de Chile después de la lluvia."),
    ("Lago en calma",             1015, "Reflejo perfecto de las montañas."),
    ("Puente de madera",          1039, "Camino sobre el estero."),
    ("Campo de lavanda",          1080, "Filas moradas hasta el horizonte."),
]


class Command(BaseCommand):
    help = "Crea un usuario de prueba y fotos de ejemplo"

    def handle(self, *args, **options):
        User = get_user_model()
        profe, creado = User.objects.get_or_create(username="profe")
        if creado:
            profe.set_password("inacap2026")
            profe.is_staff = True           # puede entrar a /admin/
            profe.is_superuser = True
            profe.save()
            self.stdout.write("Usuario creado: profe / inacap2026")

        nuevas = 0
        for titulo, id_picsum, descripcion in FOTOS:
            if Foto.objects.filter(titulo=titulo).exists():
                continue
            Foto.objects.create(
                titulo=titulo,
                url_imagen=f"https://picsum.photos/id/{id_picsum}/800/600",
                descripcion=descripcion,
                autor=profe,
            )
            nuevas += 1
        self.stdout.write(self.style.SUCCESS(f"{nuevas} fotos nuevas · {Foto.objects.count()} en total"))

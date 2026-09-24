"""
Bloque 1 · El modelo (slide 4: "¿Qué es el ORM de Django?")

Cada modelo es una TABLA y cada objeto es una FILA. Escribimos Python y
Django genera el SQL. En la presentación el ejemplo era `Producto`; aquí el
"post" de nuestra galería es una `Foto`, que en lugar de guardar el archivo
guarda la URL de la imagen (así no necesitamos subir archivos al servidor).
"""
from django.conf import settings
from django.db import models
from django.urls import reverse


class Foto(models.Model):
    titulo = models.CharField("título", max_length=100)
    url_imagen = models.URLField(
        "URL de la imagen",
        max_length=500,
        help_text="Dirección web de la imagen, ej: https://picsum.photos/id/10/800/600",
    )
    descripcion = models.TextField("descripción", blank=True)
    publicada = models.BooleanField(default=True)
    # Quién subió la foto. Se completa solo desde la vista (request.user),
    # por eso NO va en los `fields` del formulario.
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="fotos",
    )
    creada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creada"]          # las más nuevas primero
        verbose_name = "foto"
        verbose_name_plural = "fotos"

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        # CreateView y UpdateView redirigen aquí si no definimos success_url.
        return reverse("foto_detail", kwargs={"pk": self.pk})

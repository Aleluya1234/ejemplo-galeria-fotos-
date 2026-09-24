"""
URLs del proyecto.

  /admin/            Django Admin (actividad, paso 1)
  /                  la galería (galeria/urls.py)
  /accounts/login/   login y logout que Django trae listos (Bloque 4)
  /accounts/registro/  registro sencillo con UserCreationForm
"""
from django.contrib import admin
from django.urls import include, path

from galeria.views import registro

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("galeria.urls")),
    # django.contrib.auth.urls aporta: login/, logout/, password_change/, ...
    # Solo necesitamos el template registration/login.html.
    path("accounts/registro/", registro, name="registro"),
    path("accounts/", include("django.contrib.auth.urls")),
]

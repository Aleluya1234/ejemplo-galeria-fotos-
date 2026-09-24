"""
Bloque 3 · Conectar las vistas en urls.py (slide 15)

  · En vistas de clase se usa .as_view()  (error típico: olvidarlo)
  · <int:pk> captura el id del registro que Detail/Update/Delete necesitan
  · name=... permite usar {% url 'foto_list' %} y reverse_lazy('foto_list')
"""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.FotoList.as_view(), name="foto_list"),
    path("<int:pk>/", views.FotoDetail.as_view(), name="foto_detail"),
    path("nueva/", views.FotoCreate.as_view(), name="foto_create"),
    path("<int:pk>/editar/", views.FotoUpdate.as_view(), name="foto_update"),
    path("<int:pk>/borrar/", views.FotoDelete.as_view(), name="foto_delete"),

    # Bloque 2: la misma creación pero con vista de función, para comparar.
    path("nueva/funcion/", views.crear_foto, name="foto_create_funcion"),
]

"""
Vistas de la galería. Están en el mismo orden que la presentación:

  Bloque 2 · vista de FUNCIÓN con ModelForm y el patrón GET/POST (slide 10)
  Bloque 3 · las 5 vistas GENÉRICAS del CRUD (slides 13-15)
  Bloque 4 · seguridad: @login_required / LoginRequiredMixin (slide 17)

Las dos formas (función y clase) hacen lo mismo. La de función se deja para
comparar cuánto código ahorra la vista genérica; en la app "real" se usan
las de clase.
"""
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import FotoForm
from .models import Foto


# ── Bloque 2 · Vista de función con ModelForm ────────────────────────────────
# Patrón GET/POST:
#   GET  → muestra el formulario vacío
#   POST → valida y guarda si es correcto
#
# Bloque 4: @login_required → solo entra un usuario autenticado; si no,
# Django lo redirige a LOGIN_URL (settings.py).
@login_required
def crear_foto(request):
    if request.method == "POST":
        form = FotoForm(request.POST)
        if form.is_valid():                 # valida los datos
            foto = form.save(commit=False)  # objeto en memoria, aún sin INSERT
            foto.autor = request.user       # dato que NO viene del formulario
            foto.save()                     # ahora sí escribe en la BD
            return redirect("foto_list")
    else:
        form = FotoForm()                   # form vacío (GET)
    return render(request, "galeria/foto_form.html", {"form": form})


# ── Bloque 3 · Vistas genéricas ──────────────────────────────────────────────
# Convención de templates (si no se indica template_name):
#   ListView    → galeria/foto_list.html
#   DetailView  → galeria/foto_detail.html
#   CreateView  → galeria/foto_form.html
#   UpdateView  → galeria/foto_form.html
#   DeleteView  → galeria/foto_confirm_delete.html

class FotoList(ListView):
    """READ (varios). Solo fotos publicadas; ordenadas por Meta.ordering."""
    model = Foto
    paginate_by = 12

    def get_queryset(self):
        # QuerySet perezoso: se encadena filter() y recién se ejecuta al
        # recorrerlo en el template (Bloque 1, slide 6).
        return Foto.objects.filter(publicada=True)


class FotoDetail(DetailView):
    """READ (uno). <int:pk> en la URL indica qué registro mostrar."""
    model = Foto


# ── Bloque 4 · LoginRequiredMixin en vistas de clase ─────────────────────────
# Va SIEMPRE primero en la lista de herencia. Create/Update/Delete quedan
# protegidas; List/Detail siguen siendo públicas.

class FotoCreate(LoginRequiredMixin, CreateView):
    """CREATE. Usa el ModelForm del Bloque 2."""
    model = Foto
    form_class = FotoForm                   # o bien: fields = [...]
    success_url = reverse_lazy("foto_list")

    def form_valid(self, form):
        # Equivale al save(commit=False) de la vista de función.
        form.instance.autor = self.request.user
        return super().form_valid(form)


class FotoUpdate(LoginRequiredMixin, UpdateView):
    """UPDATE. Mismo template y form que Create; Django precarga el objeto."""
    model = Foto
    form_class = FotoForm
    # Sin success_url usa get_absolute_url() del modelo → volver al detalle.


class FotoDelete(LoginRequiredMixin, DeleteView):
    """DELETE. GET muestra la confirmación, POST borra."""
    model = Foto
    success_url = reverse_lazy("foto_list")


# ── Bloque 4 · Registro de usuarios ──────────────────────────────────────────
# Django ya trae el formulario (UserCreationForm: usuario + clave + confirmar,
# con validación de claves débiles) y el modelo User. Solo falta la vista, que
# sigue el mismo patrón GET/POST del Bloque 2. El login lo resuelve LoginView
# de django.contrib.auth.urls; aquí solo agregamos lo que Django no incluye.
def registro(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()           # crea el User con la clave hasheada
            login(request, usuario)         # inicia la sesión de inmediato
            return redirect("foto_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/registro.html", {"form": form})

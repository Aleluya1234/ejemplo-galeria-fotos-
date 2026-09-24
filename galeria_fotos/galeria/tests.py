"""
Tests que comprueban, uno por bloque, lo que se enseña en la Semana 5.

    python manage.py test
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import FotoForm
from .models import Foto

URL = "https://picsum.photos/id/10/800/600"


class Bloque1ORM(TestCase):
    def test_crud_con_el_orm(self):
        # CREATE (dos formas)
        f = Foto(titulo="Uno", url_imagen=URL); f.save()
        Foto.objects.create(titulo="Dos", url_imagen=URL, publicada=False)
        # READ
        self.assertEqual(Foto.objects.count(), 2)
        self.assertEqual(Foto.objects.get(id=f.id).titulo, "Uno")
        self.assertTrue(Foto.objects.filter(titulo__icontains="dos").exists())
        # UPDATE (uno y masivo)
        f.titulo = "Uno editado"; f.save()
        self.assertEqual(Foto.objects.get(id=f.id).titulo, "Uno editado")
        self.assertEqual(Foto.objects.filter(publicada=False).update(publicada=True), 1)
        # DELETE
        f.delete()
        self.assertEqual(Foto.objects.count(), 1)


class Bloque2ModelForm(TestCase):
    def test_valida_y_guarda(self):
        form = FotoForm({"titulo": "Ok", "url_imagen": URL, "publicada": True})
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(Foto.objects.count(), 1)

    def test_rechaza_url_no_https(self):
        form = FotoForm({"titulo": "Mal", "url_imagen": "http://inseguro.cl/f.jpg"})
        self.assertFalse(form.is_valid())
        self.assertIn("url_imagen", form.errors)


class Bloque3VistasGenericas(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("ana", password="clave123")
        self.foto = Foto.objects.create(titulo="Mar", url_imagen=URL, autor=self.user)
        Foto.objects.create(titulo="Oculta", url_imagen=URL, publicada=False)

    def test_list_muestra_solo_publicadas(self):
        r = self.client.get(reverse("foto_list"))
        self.assertContains(r, "Mar")
        self.assertNotContains(r, "Oculta")

    def test_detail(self):
        r = self.client.get(reverse("foto_detail", args=[self.foto.pk]))
        self.assertContains(r, URL)

    def test_create_update_delete_logueado(self):
        self.client.login(username="ana", password="clave123")
        r = self.client.post(reverse("foto_create"), {"titulo": "Nueva", "url_imagen": URL, "publicada": True})
        self.assertRedirects(r, reverse("foto_list"))
        nueva = Foto.objects.get(titulo="Nueva")
        self.assertEqual(nueva.autor, self.user)          # lo puso form_valid

        r = self.client.post(reverse("foto_update", args=[nueva.pk]), {"titulo": "Editada", "url_imagen": URL, "publicada": True})
        self.assertRedirects(r, reverse("foto_detail", args=[nueva.pk]))   # get_absolute_url
        self.assertEqual(Foto.objects.get(pk=nueva.pk).titulo, "Editada")

        r = self.client.post(reverse("foto_delete", args=[nueva.pk]))
        self.assertRedirects(r, reverse("foto_list"))
        self.assertFalse(Foto.objects.filter(pk=nueva.pk).exists())


class Bloque4Seguridad(TestCase):
    def setUp(self):
        self.foto = Foto.objects.create(titulo="Mar", url_imagen=URL)

    def test_sin_login_redirige_a_login(self):
        login = reverse("login")
        for nombre, args in [("foto_create", []), ("foto_create_funcion", []),
                             ("foto_update", [self.foto.pk]), ("foto_delete", [self.foto.pk])]:
            url = reverse(nombre, args=args)
            r = self.client.get(url)
            self.assertRedirects(r, f"{login}?next={url}", msg_prefix=nombre)
        self.assertEqual(Foto.objects.count(), 1)         # nadie borró nada

    def test_post_sin_csrf_da_403(self):
        cliente = self.client_class(enforce_csrf_checks=True)
        get_user_model().objects.create_user("ana", password="clave123")
        cliente.login(username="ana", password="clave123")
        r = cliente.post(reverse("foto_create"), {"titulo": "X", "url_imagen": URL})
        self.assertEqual(r.status_code, 403)

    def test_template_muestra_sesion(self):
        r = self.client.get(reverse("foto_list"))
        self.assertContains(r, "Iniciar sesión")
        get_user_model().objects.create_user("ana", password="clave123")
        self.client.login(username="ana", password="clave123")
        r = self.client.get(reverse("foto_list"))
        self.assertContains(r, "Hola, <strong>ana</strong>")


class Bloque4Registro(TestCase):
    def test_registro_crea_usuario_e_inicia_sesion(self):
        r = self.client.post(reverse("registro"), {
            "username": "nuevo", "password1": "ClaveSegura#2026", "password2": "ClaveSegura#2026",
        })
        self.assertRedirects(r, reverse("foto_list"))
        self.assertTrue(get_user_model().objects.filter(username="nuevo").exists())
        r = self.client.get(reverse("foto_list"))
        self.assertContains(r, "Hola, <strong>nuevo</strong>")   # quedó logueado

    def test_registro_rechaza_claves_distintas(self):
        r = self.client.post(reverse("registro"), {
            "username": "nuevo", "password1": "ClaveSegura#2026", "password2": "otra",
        })
        self.assertEqual(r.status_code, 200)                      # vuelve al form con errores
        self.assertFalse(get_user_model().objects.filter(username="nuevo").exists())


class TemplateBase(TestCase):
    def test_header_nav_y_footer(self):
        r = self.client.get(reverse("foto_list"))
        self.assertContains(r, "<header>")
        self.assertContains(r, "<nav>")
        self.assertContains(r, "<footer>")
        self.assertContains(r, reverse("registro"))
        self.assertContains(r, reverse("login"))

"""
Bloque 2 · ModelForm (slide 9: "¿Qué es un ModelForm?")

Un ModelForm genera el formulario HTML a partir del modelo, valida los datos
automáticamente y guarda directo en la BD con form.save().

`Meta` conecta el form con el modelo. En `fields` se listan los campos que
se muestran: mejor explicitarlos que usar '__all__' (así `autor` y `creada`
nunca llegan desde el navegador).
"""
from django import forms

from .models import Foto


class FotoForm(forms.ModelForm):
    class Meta:
        model = Foto
        fields = ["titulo", "url_imagen", "descripcion", "publicada"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
            "url_imagen": forms.URLInput(attrs={"placeholder": "https://..."}),
        }

    # Validación extra, además de la automática del URLField.
    # Se llama sola dentro de form.is_valid(); si lanza ValidationError,
    # el mensaje aparece junto al campo en el template.
    def clean_url_imagen(self):
        url = self.cleaned_data["url_imagen"]
        if not url.lower().startswith("https://"):
            raise forms.ValidationError("La URL de la imagen debe empezar con https://")
        return url

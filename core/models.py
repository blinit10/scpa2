import qrcode as qrcode
from django.db import models
from django.core.validators import RegexValidator
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.safestring import mark_safe
from select import error

SOLO_TEXTO_REGEX = RegexValidator(r'^[a-zA-Z]+$', 'Solo se admiten letras')
# Create your models here.
class Ficha(models.Model):
    SEXO_CHOICES = (
        ('m', 'Macho'),
        ('h', 'Hembra'),
    )
    nombre = models.CharField(max_length=255, validators=[SOLO_TEXTO_REGEX])
    identidad = models.CharField(max_length=255)
    color = models.CharField(max_length=255, validators=[SOLO_TEXTO_REGEX])
    raza = models.CharField(max_length=255, validators=[SOLO_TEXTO_REGEX])
    foto = models.ImageField(upload_to='fotos/')
    sexo = models.CharField(max_length=255, choices=SEXO_CHOICES)
    esterilizado = models.BooleanField(default=False)
    peso = models.FloatField()
    qr = models.CharField(max_length=900, blank=True, null=True)

    def __str__(self):
        return self.nombre

    def mostrar_foto(self):
        return mark_safe('<img src="'+self.foto.url+'"  width="150" height="150" >')
    mostrar_foto.short_description = 'Vista previa'
    mostrar_foto.allow_tags = True

    def mostrar_qr(self):
        imagen  = 'A'
        if self.qr is not None:
            imagen = self.qr
        return mark_safe('<img src="/media/'+ imagen +'"  width="300" height="300" >')
    mostrar_qr.short_description = 'Codigo QR'
    mostrar_qr.allow_tags = True

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.qr:
            qr = qrcode.make()
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=50,
                border=4,
            )
            esterilizado = 'No'
            if self.esterilizado == True:
                esterilizado = 'Si'
            qr.add_data({
                'nombre': str(self.nombre),
                'identidad': str(self.identidad),
                'color':str(self.color),
                'raza':str(self.raza),
                'sexo': str(self.sexo),
                'esterilizado': str(esterilizado),
                'peso': str(self.peso),
            })
            qr.make(fit=True)
            imagen = qr.make_image(fill_color="black", back_color="white").convert('RGB')
            self.qr = "/qr/" + str(self.pk) + '.png'
            self.save()
            imagen.save("media/qr/" + str(self.pk) + ".png")
        super(Ficha, self).save()

class Visitante(models.Model):
    nombre = models.CharField(max_length=255, validators=[SOLO_TEXTO_REGEX])
    apellido = models.CharField(max_length=255, validators=[SOLO_TEXTO_REGEX])
    edad = models.IntegerField(null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    veterinario = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Visita(models.Model):
    visitante = models.ForeignKey(Visitante, on_delete=models.SET_NULL, null=True)
    fecha = models.DateField()

    def __str__(self):
        return self.visitante.nombre + ' - ' + str(self.fecha)

class Evento(models.Model):
    nombre = models.CharField(max_length=255)
    foto = models.ImageField(upload_to='fotos/')
    tipo = models.CharField(max_length=255)
    fecha = models.DateTimeField()
    detalles = RichTextField()

    def __str__(self):
        return self.nombre

    def mostrar_foto(self):
        return mark_safe('<img src="'+self.foto.url+'"  width="150" height="150" >')
    mostrar_foto.short_description = 'Vista previa'
    mostrar_foto.allow_tags = True

class Informacion(models.Model):
    texto = RichTextUploadingField()

    def __str__(self):
        return mark_safe(self.texto[:25])

class Denuncia(models.Model):
    ficha = models.ForeignKey(Ficha, related_name='denuncias', on_delete=models.CASCADE)
    fecha = models.DateField()

    def __str__(self):
        return "Denuncia " + self.ficha.nombre
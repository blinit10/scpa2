from django.db import models
from django.core.validators import RegexValidator
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

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

    def __str__(self):
        return self.nombre

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

class Informacion(models.Model):
    texto = RichTextUploadingField()

    def __str__(self):
        return self.texto[:25]

class Denuncia(models.Model):
    ficha = models.ForeignKey(Ficha, related_name='denuncias', on_delete=models.CASCADE)
    fecha = models.DateField()

    def __str__(self):
        return "Denuncia " + self.ficha.nombre
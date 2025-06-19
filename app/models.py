from django.db import models
import uuid
from django.utils import timezone
from .utils import path_bases, path_cedula_identidad_internos, path_certificado_discapacidad_internos, path_certificado_laboral_internos, path_certificado_titulo_internos, path_curriculum_internos, path_cursos_capacitaciones
# Create your models here.




class PostulacionInternos(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    abreviatura = models.CharField(max_length=100)
    titulo = models.TextField()
    nombre_cargo = models.TextField()
    objetivo = models.TextField()
    grado = models.TextField()
    remuneracion = models.TextField()
    funciones_cargo = models.TextField()
    funciones_complementarias_cargo = models.TextField(null=True, blank=True)
    caracteristicas_entorno = models.TextField()
    requisitos = models.TextField()
    conocimientos_generales = models.TextField()
    conocimientos_especificos = models.TextField()

    importante = models.TextField()
    bases = models.FileField(upload_to=path_bases, blank=True, null=True)
    fecha_inicio = models.DateField(default=timezone.localdate)
    fecha_termino = models.DateField(default=timezone.localdate)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_cargo

    class Meta:
        db_table = "postulacion_internos"
class CompetenciaTransversal(models.Model):
    postulacion = models.ForeignKey(PostulacionInternos, on_delete=models.CASCADE, related_name="competencias_transversales")
    nombre = models.CharField(max_length=255, null=True, blank=True)
    nivel = models.IntegerField(choices=[(i, str(i)) for i in range(1, 5)], null=True, blank=True)

    def __str__(self):
        return f"[T] {self.nombre} (Nivel {self.nivel})"
    class Meta:
        db_table = "competencias_transversales_internos"

class CompetenciaEspecifica(models.Model):
    postulacion = models.ForeignKey(PostulacionInternos, on_delete=models.CASCADE, related_name="competencias_especificas")
    nombre = models.CharField(max_length=255, null=True, blank=True)
    nivel = models.IntegerField(choices=[(i, str(i)) for i in range(1, 5)], null=True, blank=True)

    def __str__(self):
        return f"[E] {self.nombre} (Nivel {self.nivel})"

    class Meta:
        db_table = "competencias_especificas_internos"



class PostulanteInterno(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    rut = models.CharField(max_length=12, blank=False, null=False)
    nombre_completo = models.CharField(max_length=255, blank=False)
    genero = models.CharField(max_length=255, blank=False)
    comuna_residencia = models.CharField(max_length=255, blank=False, null=False)
    telefono_contacto = models.CharField(max_length=12, blank=True, null=True)
    correo_electronico = models.EmailField(
        blank=False, null=False, max_length=50)
    posee_certificado_titulo = models.CharField(max_length=255, blank=True, null=True)
    posee_certificado_laboral= models.CharField(max_length=255, blank=True, null=True)
    presenta_certificado_cursos = models.CharField(max_length=255, blank=True, null=True)
    años_experiencia = models.CharField(max_length=255, blank=True, null=True)
    discapacidad = models.CharField(max_length=255, blank=True, null=True)
    
    postulacion = models.ForeignKey(
    PostulacionInternos,
    on_delete=models.CASCADE,
    related_name='postulantes'
    )
    fecha_creacion = models.DateTimeField(
        default=timezone.now,
        editable=False,
        verbose_name="Fecha de creación"
    )
    #DOCUMENTOS
    cedula_identidad     = models.FileField(
        upload_to=path_cedula_identidad_internos, blank=True, null=True, max_length=255)
    curriculum = models.FileField(
        upload_to=path_curriculum_internos, blank=True, null=True, max_length=255)
    certificado_titulo = models.FileField(
        upload_to=path_certificado_titulo_internos, blank=True, null=True, max_length=255)
    cursos_capacitaciones = models.FileField(
        upload_to=path_cursos_capacitaciones, blank=True, null=True, max_length=255)
    certificado_laboral = models.FileField(upload_to=path_certificado_laboral_internos,blank=True, null=True, max_length=255)
    

    certificado_discapacidad = models.FileField(upload_to=path_certificado_discapacidad_internos,blank=True, null=True, max_length=255)
    
    def __str__(self):
        return self.nombre_completo
    
    class Meta:
        db_table = "postulante_interno"


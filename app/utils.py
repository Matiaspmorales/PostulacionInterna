import os
from django import forms
from django.conf import settings
import shutil




genero = (
    ('', 'Seleccione una opción'),
    ('Masculino', 'Masculino'),
    ('Femenino', 'Femenino'),
    ('No binario', 'No binario'),
    ('Prefiero no responder', 'Prefiero no responder'),
    ('Otros', 'Otros')
)

opcion_si_no = (
    ('', 'Seleccione una opción'),
    ('Sí', 'Sí'),
    ('No', 'No')
)

años_experiencia = (
    ('', 'Seleccione una opción'),
    ('Menos de un año', 'Menos de un año'),
    ('Entre 1 año y menos de 2 años', 'Entre 1 año y menos de 2 años'),
    ('Entre 2 años y menos de 3 años', 'Entre 2 años y menos de 3 años'),
    ('Entre 3 años y menos de 4 años', 'Entre 3 años y menos de 4 años'),
    ('Entre 4 años y menos de 5 años', 'Entre 4 años y menos de 5 años'),
    ('Más de 5 años', 'Más de 5 años')
)


niveles = [(str(i), str(i)) for i in range(1, 5)]


def path_bases(instance, filename):
    extension = filename.split('.')[-1]
    nombre = "bases"
    nombre_tabla = instance.abreviatura.replace(" ", "_")
    nuevo_nombre = f'{nombre}.{extension}'
    return os.path.join("documentos/internos/", nombre_tabla, nombre, nuevo_nombre)


def path_bases(instance, filename):
    extension = filename.split('.')[-1]
    nombre = "bases"
    nombre_tabla = instance.abreviatura.replace(" ", "_")
    nuevo_nombre = f'{nombre}.{extension}'
    return os.path.join("documentos/internos/", nombre_tabla, nombre, nuevo_nombre)



def path_cedula_identidad_internos(instance, filename):
    extension = filename.split('.')[-1]
    rut = instance.rut
    
    nombre_tabla = instance.postulacion.abreviatura.replace(" ", "_")
    nuevo_nombre = f'cedula_identidad_{rut}.{extension}'
    return os.path.join("documentos/internos/", nombre_tabla, rut,'archivos', nuevo_nombre)


def path_curriculum_internos(instance, filename):
    extension = filename.split('.')[-1]
    rut = instance.rut
    nombre_tabla = instance.postulacion.abreviatura.replace(" ", "_")
    nuevo_nombre = f'curriculum_{rut}.{extension}'
    return os.path.join("documentos/internos/", nombre_tabla, rut,'archivos', nuevo_nombre)


def path_certificado_titulo_internos(instance, filename):
    extension = filename.split('.')[-1]
    rut = instance.rut
    
    nombre_tabla = instance.postulacion.abreviatura.replace(" ", "_")
    nuevo_nombre = f'certificado_titulo_{rut}.{extension}'
    return os.path.join("documentos/internos/", nombre_tabla, rut,'archivos', nuevo_nombre)


def path_cursos_capacitaciones(instance, filename):
    extension = filename.split('.')[-1]
    rut = instance.rut
    
    nombre_tabla = instance.postulacion.abreviatura.replace(" ", "_")
    nuevo_nombre = f'cursos_capacitaciones_{rut}.{extension}'
    return os.path.join("documentos/internos/", nombre_tabla, rut,'archivos', nuevo_nombre)

def path_certificado_laboral_internos(instance, filename):
    extension = filename.split('.')[-1]
    rut = instance.rut
    
    nombre_tabla = instance.postulacion.abreviatura.replace(" ", "_")
    nuevo_nombre = f'certificado_laboral_{rut}.{extension}'
    return os.path.join("documentos/internos/", nombre_tabla, rut,'archivos', nuevo_nombre)


def path_certificado_discapacidad_internos(instance, filename):
    extension = filename.split('.')[-1]
    rut = instance.rut
    
    nombre_tabla = instance.postulacion.abreviatura.replace(" ", "_")
    nuevo_nombre = f'certificado_discapacidad_{rut}.{extension}'
    return os.path.join("documentos/internos/", nombre_tabla, rut,'archivos', nuevo_nombre)





def validar_pdf(archivo, nombre_campo, requerido=False):
    if not archivo:
        if requerido:
            raise forms.ValidationError(f"Debe adjuntar su {nombre_campo}.")
        return None

    if archivo.size > 5 * 1024 * 1024:
        raise forms.ValidationError(
            f"El archivo '{nombre_campo}'no debe superar los 5MB.")

    if not archivo.name.endswith('.pdf'):
        raise forms.ValidationError(
            f"El archivo '{nombre_campo}' debe estar en formato PDF.")

    return archivo



def eliminar_archivos_existentes_internos(instancia):
    nombre = instancia.rut.replace(" ", "_")
    abreviatura = instancia.postulacion.abreviatura.replace(" ", "_")

    carpeta = os.path.join(
        settings.MEDIA_ROOT,
        "documentos", "internos", abreviatura, nombre
    )

    if os.path.isdir(carpeta):
        shutil.rmtree(carpeta)
        print(f"✅ Carpeta eliminada: {carpeta}")
    else:
        print(f"⚠️ No se encontró carpeta para eliminar: {carpeta}")
        


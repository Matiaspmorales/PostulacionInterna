from django import forms
from . import models
from .utils import genero, opcion_si_no, años_experiencia,  validar_pdf, niveles
from django.forms import ModelForm,  modelformset_factory
from django.core.exceptions import ValidationError
import re
from django.shortcuts import redirect

class PostulanteInternoForm(ModelForm):
    rut = forms.CharField(widget=forms.TextInput(attrs={
                          'class': 'form-control', 'placeholder': 'Su respuesta'}), label="Ingrese su rut (con puntos y guión) *", required=True)

    nombre_completo = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Su respuesta'}), label="Ingrese su nombre completo *")

    genero = forms.ChoiceField(choices=genero, widget=forms.Select(
        attrs={'class': 'form-control', 'id': 'id_genero'}), label="Indique su género *", required=True)

    otro_genero = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'id_otro_genero'}), label="Especifique su género *")

    comuna_residencia = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Su respuesta'}), label="Ingrese su Comuna de residencia *")
    telefono_contacto = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Su respuesta'}), label="Ingrese su número de teléfono *")

    correo_electronico = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Su respuesta'}), label="Ingrese su correo electrónico *")

    posee_certificado_titulo = forms.ChoiceField(choices=opcion_si_no, widget=forms.Select(
        attrs={'class': 'form-control'}), label="¿Posee certificado de Título relacionado al cargo al cúal postula otorgado por una universidad reconocida por el estado de Chile o aquellos validados en Chile de acuerdo con la legislación vigente? *", required=True)

    posee_certificado_laboral = forms.ChoiceField(choices=opcion_si_no, widget=forms.Select(
        attrs={'class': 'form-control'}), label="¿Posee certificado laboral que acredite su experiencia profesional, en las áreas requeridas de acuerdo al perfil? *", required=True)
    
    presenta_certificado_cursos = forms.ChoiceField(choices=opcion_si_no, widget=forms.Select(
        attrs={'class': 'form-control'}), label="¿Presenta certificado/s de cursos generales y/o específicos requeridos para el cargo? *", required=True)


    discapacidad = forms.ChoiceField(choices=opcion_si_no, widget=forms.Select(
        attrs={'class': 'form-control', 'id': 'id_discapacidad'}), label="¿Presenta alguna discapacidad? *", required=True)


    años_experiencia = forms.ChoiceField(
        choices=años_experiencia,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Indique años de experiencia laboral como profesional acreditable o demostrable con certificado laboral *",
        required=True,
        error_messages={'required': 'El campo es obligatorio.'}
    )


    cedula_identidad = forms.FileField(widget=forms.FileInput(
        attrs={'class': 'form-control'}), label="Cédula de identidad (AMBOS LADOS) *", required=False)

    certificado_laboral = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label="Certificado laboral que acredite experiencia (Certificado que indique: nombre completo, RUT, cargo, fecha de inicio y término, principales funciones, fecha de emisión y firma de quién lo emite)",
        required=False
    )

    certificado_titulo = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label="Certificado Título, licencia de enseñanza media o Certificado de inscripción en el Registro Nacional de Prestadores Individuales según corresponda *",
        required=False
    )
    certificado_discapacidad = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label="Certificado de Discapacidad *:",
        required=False
    )
    curriculum = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label="Curriculum Vitae (CV) *",
        required=False
    )

    cursos_capacitaciones= forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label="Cursos o capacitaciones acorde al cargo (subir un solo documento) *",
        required=False
    )
    

    def clean(self):
        cleaned_data = super().clean()

      

        genero = cleaned_data.get('genero')
        otro_genero = cleaned_data.get('otro_genero', '').strip()
        if genero == 'Otros':
            if not otro_genero:
                self.add_error('otro_genero', 'Debe especificar su género.')
            elif len(otro_genero) > 255:
                self.add_error(
                    'otro_genero', 'Debe tener máximo 255 caracteres.')
            else:
                cleaned_data['genero'] = otro_genero

      

        return cleaned_data


    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if rut:
            rut = rut.strip()
            regex = re.compile(r'^\d{1,2}\.\d{3}\.\d{3}-[0-9kK]$')
            if not regex.match(rut):
                raise forms.ValidationError(
                    "Ingrese un RUT válido, por ejemplo: 12.345.678-9")
        return rut
    
    def clean_telefono_contacto(self):
        telefono = self.cleaned_data['telefono_contacto']

        # Limpieza: elimina espacios, guiones y paréntesis
        telefono = re.sub(r'[^\d+]', '', telefono)

        # Si empieza con +56, remueve ese prefijo
        if telefono.startswith('+56'):
            telefono = telefono[3:]

        # Validar largo (Chile: 9 dígitos)
        if not re.fullmatch(r'\d{9}', telefono):
            raise ValidationError("El número debe tener 9 dígitos (celular: 912345678 o (+56) 9 1234 5678  fijo: 632123456 o (+56) 63 212 3456)")

        # Validar si es celular o fijo (celular empieza con 9, fijo con 2 a 9 excepto 9)
        if not (telefono.startswith('9') or telefono.startswith(('2', '3', '4', '5', '6', '7'))):
            raise ValidationError("Ingrese un número válido (celular: 912345678 o (+56) 9 1234 5678  fijo: 632123456 o (+56) 63 212 3456)")

        return telefono

    def clean_correo_electronico(self):
        correo = self.cleaned_data.get(
            'correo_electronico', '').strip().lower()
        pattern = r'^[\w\.-]+@[\w\.-]+\.(com|cl|org|edu)$'
        if not re.match(pattern, correo):
            raise forms.ValidationError(
                'Por favor ingrese un correo válido (ejemplo@dominio.cl, .com, .org, .edu).')
        return correo

    def clean_curriculum(self):
        return validar_pdf(self.cleaned_data.get('curriculum'), "Currículum", requerido=True)

    def clean_cedula_identidad(self):
        return validar_pdf(self.cleaned_data.get('cedula_identidad'), "Cédula de Identidad", requerido=True)

    def clean_certificado_discapacidad(self):
            valor = self.cleaned_data.get('discapacidad', '')
            archivo = self.cleaned_data.get('certificado_discapacidad')

            if valor == 'Sí':
                return validar_pdf(archivo, "Certificado de Discapacidad", requerido=True)
            return None
    def clean_certificado_titulo(self):
        certificado = self.cleaned_data.get("certificado_titulo")
        if not certificado:
            raise forms.ValidationError(
                "Debe adjuntar su Certificado de Título.")
        return validar_pdf(certificado, "Certificado de Título")
    
    def clean_certificado_laboral(self):
        certificado = self.cleaned_data.get("certificado_laboral")
        if not certificado:
            raise forms.ValidationError(
                "Debe adjuntar su Certificado laboral.")
        return validar_pdf(certificado, "Certificado laboral")

    def clean_cursos_capacitaciones(self):
        certificado = self.cleaned_data.get("cursos_capacitaciones")
        if not certificado:
            raise forms.ValidationError(
                "Debe adjuntar sus cursos o capacitaciones.")
        return validar_pdf(certificado, "Cursos o Capacitaciones")

    class Meta:
        model = models.PostulanteInterno
        fields = '__all__'
        exclude = ['postulacion']


        
class PostulacionInternosForm(forms.ModelForm):
    abreviatura = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: abreviatura_unica'}),
        label="Abreviatura *",
        required=True
    )
    titulo = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        label="Título de la Convocatoria *",
        required=True
    )
    nombre_cargo = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
        label="Nombre del Cargo *",
        required=True
    )
    objetivo = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label="Objetivo *",
        required=True
    )
    grado = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        label="Grado *",
        required=True
    )
    remuneracion = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
        label="Remuneración *",
        required=True
    )
    funciones_cargo = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        label="Funciones del Cargo *",
        required=True
    )
    funciones_complementarias_cargo = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label="Funciones Complementarias ",
        required=False
    )
    caracteristicas_entorno = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        label="Características del Entorno *",
        required=True
    )
    requisitos = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label="Requisitos *",
        required=True
    )
    conocimientos_generales = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label="Conocimientos Generales *",
        required=True
    )
    conocimientos_especificos = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label="Conocimientos Específicos *",
        required=True
    )
    importante = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        label="Información Importante *",
        required=True
    )
    bases = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label="Bases (PDF)",
        required=False
    )
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label="Fecha de Inicio *",
        required=True
    )
    fecha_termino = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label="Fecha de Término *",
        required=True
    )

    class Meta:
        model = models.PostulacionInternos
        fields = '__all__'
        exclude = ['id', 'estado']

    def clean(self):
        cleaned = super().clean()
        fi = cleaned.get('fecha_inicio')
        ft = cleaned.get('fecha_termino')
        if fi and ft and ft < fi:
            self.add_error('fecha_termino', 'La fecha de término no puede ser anterior a la fecha de inicio.')
        return cleaned

class CompetenciaTransversalForm(forms.ModelForm):
    class Meta:
        model = models.CompetenciaTransversal
        fields = ['nombre', 'nivel']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Trabajo en equipo'}),
            'nivel': forms.Select(choices=niveles, attrs={'class': 'form-control'})
        }

class CompetenciaEspecificaForm(forms.ModelForm):
    class Meta:
        model = models.CompetenciaEspecifica
        fields = ['nombre', 'nivel']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Liderazgo'}),
            'nivel': forms.Select(choices=niveles, attrs={'class': 'form-control'})
        }

CompetenciaTransversalFormSet = modelformset_factory(
    models.CompetenciaTransversal,
    form=CompetenciaTransversalForm,
    extra=1,  
    can_delete=True
)

CompetenciaEspecificaFormSet = modelformset_factory(
    models.CompetenciaEspecifica,
    form=CompetenciaEspecificaForm,
    extra=1,
    can_delete=True
)
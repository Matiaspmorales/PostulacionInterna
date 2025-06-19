from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "postulacion"
urlpatterns = [
     path('', views.index, name="index"),
     path('iniciar_sesion/', views.iniciarSesion, name="iniciar_sesion"),
     path('cerrar_sesion/', views.cerrarSesion, name="cerrar_sesion"),

     path("internos/", views.postulacion_internas, name="internos"),
     path('internos/crear-concurso-interno/', views.crear_postulacion_interna, name="crear_concurso"),
     path('internos/editar-concurso-interno/<uuid:postulacion_id>/', views.editar_postulacion_interna, name="editar_concurso"),



     path('internos/postular/<uuid:postulacion_id>/', views.ingreso_postulante_interno, name='postular_interno'),
     path('internos/ver-postulante-interno/<uuid:id>/', views.ver_postulantes_internos, name='ver_postulante_interno'),
     path('internos/detalle-postulante/<uuid:id>/', views.detalle_postulante_interno, name='detalle_postulacion_interna'),
     path('exportar_postulantes_internos/<uuid:postulacion_id>/',views.exportar_postulantes_internos, name='exportar_postulantes_internos'),


     
     path('acceso-denegado/', TemplateView.as_view(template_name='errores/403.html'), name='acceso_denegado'),
     
     
     
     ]

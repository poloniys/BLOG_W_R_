""" Urls patterns for users."""
from django.urls import path, include

from APP_Profile.views import *



urlpatterns = [
    # Django's defaults auth urls login/logout
   # path('', include('django.contrib.auth.urls')),
    # Registration/Modification patterns

    path('perfil/<user_id>/', Perfil_V, name='perfil'),
    path('editarPerfil', editarPerfil, name='editarPerfil'),
    path('cambiar_foto_perfil', Cambiar_foto_perfil_V, name='cambiar_foto_perfil'),
    path('inbox/', inbox, name='inbox'),
    #path('busquedaUsuario/', buscar, name='busquedaUsuario'),
    #path('buscar/', buscar ,name='buscar' ),
   # path('leerMensajes/', leerMensajes ,name='leerMensajes' ),
    path('eliminarMensaje/<id>', eliminarMensaje ,name='eliminarMensaje' ),
    #path('editarMensaje/<id>', editarMensaje ,name='editarMensaje' ),
    path('mensaje_nuevo', mensaje_nuevo_V ,name='mensaje_nuevo' ),
    path('mostrar_otros_perfil', Mostrar_O_Perfil_V ,name='mostrar_otros_perfil' ),


]
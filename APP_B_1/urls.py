from django.urls import path
from APP_B_1.views import *
from APP_Profile.views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', Home_V, name= 'home'),
    path('posts', Posts_V, name= 'posts'),
    path('crear_post', Crear_post, name='crear_post'),
    path('<slug:slug>/', post_detail, name='post_detail'),
    path('editar_post/<slug:slug>/', Editar_Post_V, name= 'editar_post'),
    path('eliminar_post/<slug:slug>/', Eliminar_Post_V, name= 'eliminar_post'),
    path('login', Log_In_V, name= 'login'),
    path('registro', Registro_V, name= 'registro'),
    path('logout', LogoutView.as_view(template_name='APP_B_1/logout.html'), name= 'logout'),
    path('mi_blog', Mi_Blog_V, name= 'mi_blog'),
    path('about', About_V, name= 'about'),
    path('perfil', Perfil_V, name= 'perfil')

]

"""User's views for register; update profile and messageing between users."""

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls.base import reverse
# Decorators
from django.contrib.auth.decorators import login_required
# For make complex lookups (AND/OR)
from django.db.models import Q

from django.contrib.auth.decorators import user_passes_test

# Defined User's models and forms
from APP_Profile.forms import AvatarForm,UserEditForm, MensajesFormulario, UserEditForm
from APP_Profile.models import Avatar, Mensajes


@login_required
def Perfil_V(request):
    """Profile view data"""
    user = request.user
    # Para buscar si el usuario tiene avatar
    try:
        avatar = Avatar.objects.get(user=request.user.id)
        avatar = avatar.avatar.url
    except:
        avatar = ''

    context = {
        'user': user,
        'avatar': avatar,
        'title': 'Profile',
    }
    return render(request, 'APP_Profile/perfil.html',context)

@login_required
def editarPerfil(request):
    """Update user profile."""
    
    usuario = request.user
    if request.method=="POST":
        form=UserEditForm(request.POST, instance=usuario)
        if form.is_valid():
            info=form.cleaned_data

            usuario.email=info["email"]
            usuario.first_name=info["first_name"]
            usuario.last_name=info["last_name"]
            usuario.password1=info["password1"]
            usuario.password2=info["password2"]
            usuario.link_pagina_web=info["link_pagina_web"]
            usuario.descripcion=info["descripcion"]
            usuario.save()
            return render(request, 'APP_Profile/perfil.html')

    else:
        form=UserEditForm(instance=usuario)
    return render(request, 'APP_Profile/editarPerfil.html', {'form':form})

@login_required
def Cambiar_foto_perfil_V(request):
    
    user = request.user
    # Para buscar si el usuario tiene avatar
    try:
        avatar = Avatar.objects.get(user=request.user.id)
        avatar = avatar.avatar.url
    except:
        avatar = ''

    if request.method != 'POST':
        # No data submited. Paso formulario vacio
        form = AvatarForm()
    
    else:
        form = AvatarForm(request.POST, request.FILES)

        if form.is_valid():
            avatars = Avatar.objects.filter(user=user)

            if len(avatars) > 0:
                new_avatar = avatars[0]
                new_avatar.avatar = form.cleaned_data['avatar']
                new_avatar.save()
            else:
                new_avatar = Avatar(user=user, avatar=form.cleaned_data['avatar'])
                new_avatar.save()
        
        return redirect('perfil')
    
    context = {
        'title': 'Update Avatar',
        'subtitle': 'Actualizar avatar',
        'form': form,
        'avatar': avatar
    }
    return render(request, "APP_Profile/cambiar_foto_perfil.html", context)


@login_required
def inbox(request):
    if request.method == "POST":
        miFormulario=MensajesFormulario(request.POST)
        print(miFormulario)
        if miFormulario.is_valid():
            info=miFormulario.cleaned_data
            usuario=info.get("usuario")
            texto=info.get("texto")
            mensaje=Mensajes(usuario=usuario, texto=texto)
            mensaje.save()
            return render(request, "APP_Profile/inbox.html", {"comentario":"Mensaje enviado"})

        else:
            return render(request, "APP_Profile/inbox.html", {"comentario":"Ingrese nuevamente, pero bien"})

    else:
        miFormulario=MensajesFormulario()
        return render(request,"APP_Profile/inbox.html", {"formulario":miFormulario,"avatar":obtenerAvatar(request)})


def obtenerAvatar(request):
    lista=Avatar.objects.filter(user=request.user)
    if len(lista)!=0:
            avatar=lista[0].avatar.url
    else:
            avatar=None
    return avatar

    
def home(request):
    contexto={'home_im':"media/post_images/pet_1.png"}    

    return render(request,'APP_Profile/home.html', contexto )
@login_required
def busquedaUsuario(request):
    return render(request, "APP_Profile/busquedaUsuario.html") 

@login_required
def buscar(request):
    if request.GET["usuario"]:
        usua=request.GET["usuario"]
        mensajes=Mensajes.objects.filter(usuario=usua)
        if len(mensajes)!=0:
            return render(request, "APP_Profile/resultadoBusqueda.html", {"mensaje":mensajes})
        else:
            return render(request, "APP_Profile/resultadoBusqueda.html", {"comentario":"No existe mensajes de este compa!"})
    
    else:
         return render(request, "APP_Profile/resultadoBusqueda.html", {"comentario":"No enviaste datos, intentalo de nuevo"})

@login_required
def leerMensajes(request):
    mensajes=Mensajes.objects.all()
    print(mensajes)
    return render(request, "APP_Profile/leerMensajes.html", {"mensajes":mensajes})

@login_required
def eliminarMensaje(request, id):
    mensa=Mensajes.objects.get(id=id)
    mensa.delete()
    mensajes=Mensajes.objects.all()
    return render(request, "APP_Profile/leerMensajes.html", {"mensajes":mensajes})
    
@login_required
def editarMensaje(request, id):
    mensa=Mensajes.objects.get(id=id)
    if request.method=="POST":
        form=MensajesFormulario(request.POST)
        if form.is_valid():

            info=form.cleaned_data
            mensa.usuario=info["usuario"]
            mensa.texto=info["texto"]
            mensa.save()
            mensajes=Mensajes.objects.all()
            return render(request, "APP_Profile/leerMensajes.html", {"mensajes":mensajes})

    else:
        form=MensajesFormulario(initial={"usuario":mensa.usuario, "texto":mensa.texto})
        return render(request, "APP_Profile/editarMensaje.html", {"formulario":form, "mensaje_enviado":mensa.usuario, "id":mensa.id})
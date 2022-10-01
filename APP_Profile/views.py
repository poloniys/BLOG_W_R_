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
from APP_Profile.forms import AvatarForm,UserEditForm, MensajesFormulario, UserEditForm, Busq_Us_Form
from APP_Profile.models import Avatar, Mensajes

from django.contrib.auth.models import User

@login_required
def Perfil_V(request, user_id):
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
    try:
        avatar = Avatar.objects.get(user=request.user.id)
        avatar = avatar.avatar.url
    except:
        avatar = ''


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

            return render(request, 'APP_Profile/perfil.html',{'avatar':avatar})


    else:

        form=UserEditForm(instance=usuario)

    return render(request, 'APP_Profile/editarPerfil.html', {'form':form,'avatar':avatar})

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

            return redirect(reverse('perfil', args=[id]))

    
    context = {
        'title': 'Update Avatar',
        'subtitle': 'Actualizar avatar',
        'form': form,
        'avatar': avatar
    }
    return render(request, "APP_Profile/cambiar_foto_perfil.html", context)



def obtenerAvatar(request):
    lista=Avatar.objects.filter(user=request.user)
    if len(lista)!=0:
            avatar=lista[0].avatar.url
    else:
            avatar=None
    return avatar



@login_required
def inbox(request):
    
    user = request.user
    # Para buscar si el usuario tiene avatar
    try:
        avatar = Avatar.objects.get(user=request.user.id)
        avatar = avatar.avatar.url
    except:
        avatar= ''

    messages = Mensajes.objects.filter(Q(receiver=user) | Q(sender=user)).order_by('-sent_at')
    received = messages.filter(receiver=user).order_by('-sent_at')
    sent = messages.filter(sender=user).order_by('-sent_at')

    context = {
        'title': 'MENSAJERIA',
        'user': user,
        'messages': messages,
        'received': received,
        'sent':sent,
        'avatar': avatar,
    }
    return render(request, "APP_Profile/inbox.html", context)

@login_required
def mensaje_nuevo_V(request):
    """Sending new messages."""
    
    user = request.user
    # Para buscar si el usuario tiene avatar
    try:
        avatar = Avatar.objects.get(user=request.user.id)
        avatar = avatar.avatar.url
    except:
        avatar = ''

    if request.method != 'POST':
        # No data submited. Paso formulario vacio
        form = MensajesFormulario()
    
    else:
        # Data submitted. Paso formulario con datos ingresados por POST
        form = MensajesFormulario(data=request.POST)
        if form.is_valid():

            #msg=form.cleaned_data
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()

            return redirect('mensaje_nuevo')
    
    context = {
        'form': form,
        'title': 'New message',
        'avatar':avatar,
    }
    return render(request, 'APP_Profile/mensaje_nuevo.html', context)


@login_required
def eliminarMensaje(request, id):
    mensa=Mensajes.objects.get(id=id)
    mensa.delete()
    mensajes=Mensajes.objects.all()
    return render(request, "APP_Profile/inbox.html", {"mensajes":mensajes})

@login_required
def Mostrar_O_Perfil_V(request):
    user = request.user

    """Profile view data"""
    try:
        avatar = Avatar.objects.get(user=request.user.id)
        avatar = avatar.avatar.url
    except:
        avatar = ''

    if request.method != 'POST':
        # No data submited. Paso formulario vacio
        form = Busq_Us_Form()
    
    else:
        # Data submitted. Paso formulario con datos ingresados por POST
        form = Busq_Us_Form(data=request.POST)
       # if form.is_valid():
        if form.is_valid():

            user= form.cleaned_data['receiver']
          #  usuario_b = Mensajes.objects.filter(id=user)
            usuario=User.objects.get(username=user)
            print(usuario)
            try:
                avatar2 = Avatar.objects.get(user=usuario)
                avatar2 = avatar2.avatar.url
            except:
                avatar2 = ''
                print('avatar2')

            print(avatar2)

            context = {
                'form':form,
                'usuario': usuario,
                'avatar':avatar,
                'avatar2': avatar2,
                'title': 'Explorando Usuarios!',
            }
            return render(request, 'APP_Profile/mostrar_otros_perfil.html', context)


    return render(request, 'APP_Profile/mostrar_otros_perfil.html', {'form':form,'avatar':avatar})

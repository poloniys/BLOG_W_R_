"""Forms for users app. Register new user; update profiles; messages."""

from email.message import Message
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# My models
from APP_Profile.models import Avatar, Mensajes

# Forms


class AvatarForm(forms.ModelForm):
    """Avatar form"""

    class Meta:
        model = Avatar
        fields = ['avatar',]

class UpdateProfileForm(UserCreationForm):
    """Customization for new user registration form."""
    
    username = forms.CharField(label='Usuario')
    email = forms.EmailField(label='email')
    first_name = forms.CharField(label='Nombre', required=False)
    last_name = forms.CharField(label='Apellido', required=False)    
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Reingrese contraseña', widget=forms.PasswordInput)
    link_pagina_web = forms.CharField(label='Link')
    descripcion = forms.CharField(label='Descripcion')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'link_pagina_web',
            'descripcion',
        ]

#class MensajesFormulario(forms.Form):
#    usuario=forms.CharField(max_length=50)
#    texto=forms.CharField(max_length=1000)

#    class Meta:
#        model = Mensajes


class MensajesFormulario(forms.ModelForm):
    """DM's form"""
    
    class Meta:
        model = Mensajes  # Modelo del cual importa
        fields = [
            'receiver',
            'texto',
        ]
        #  Widget para agrandar el area de texto(TextField) a 80 columnas
        widgets = {'texto': forms.Textarea(attrs={'cols': 80})}

class UserEditForm(UserCreationForm):
    username = forms.CharField(label='Modificar Usuario')
    email = forms.EmailField(label='Modificar email')
    first_name = forms.CharField(label='Modificar Nombre', required=False)
    last_name = forms.CharField(label='Modificar Apellido', required=False)    
    password1 = forms.CharField(label='Modificar Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Reingrese contraseña', widget=forms.PasswordInput)
    link_pagina_web = forms.CharField(label='Modificar Link')
    descripcion = forms.CharField(label='Modificar Descripcion')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'link_pagina_web',
            'descripcion',
        ]
        help_texts = {k:"" for k in fields}




class Busq_Us_Form(forms.ModelForm):
    """DM's form"""
    
    class Meta:
        model = Mensajes  # Modelo del cual importa
        fields = [
            'receiver',          
        ]
      
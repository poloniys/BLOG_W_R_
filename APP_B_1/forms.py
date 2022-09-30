from collections import UserDict
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from APP_B_1.models import Post, Comment
from django_summernote.fields import SummernoteWidget

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repetir Contraseña', widget=forms.PasswordInput)

    class Meta:
        model= User 
        fields = ['username', 'email', 'password1', 'password2']
        #Saca los mensajes de ayuda
        help_texts = {k:"" for k in fields}


class NuevoPost(forms.ModelForm):
    """Form to add new posts."""
    
    class Meta:
        model = Post  # Modelo del cual importa
        fields = [
            'title',
            'subtitle',
            'content',
            'image',
            ]

        #  Widget para agrandar el area de texto(TextField) a 80 columnas
       # widgets = {'content': forms.Textarea(attrs={'cols': 80})}

    content = forms.CharField(widget=SummernoteWidget())


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


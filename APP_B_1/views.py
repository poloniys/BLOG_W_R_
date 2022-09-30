#Se importa todo lo necesario para las funcioens en views
from django.shortcuts import render, redirect
from APP_B_1.models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import AuthenticationForm
from APP_B_1.forms import * 
from .models import Post
from django.urls.base import reverse
from APP_Profile.models import Avatar
from APP_Profile.views import obtenerAvatar

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

import os

#Se desarrollan las funcioens para url

def Home_V(request):
    contexto={'home_im':"media/post_images/pet_1.png"}    

    return render(request,'APP_B_1/home.html', contexto )

def Posts_V(request):
    
    post_list =  Post.objects.filter(status=1).order_by('-created_on')

    paginator = Paginator(post_list, 5)  # 5 post por pagina
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)


    return render(request,'APP_B_1/posts.html',{'post_list':post_list,'page': page} )



def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    comments = post.comments.filter(active=True)
    new_comment =None
    user_commenting=request.user
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            new_comment.name= user_commenting
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'APP_B_1/post_detail.html', {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form
                                           })



def Log_In_V(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)

        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            contra = form.cleaned_data.get('password')

            user = authenticate(username=usuario, password=contra)

            if user is not None:
                login(request, user)
                usuario=  request.user

                post_list =  Post.objects.filter(status=1,author=usuario).order_by('-created_on')

                return render(request,'APP_B_1/mi_blog.html',{'post_list':post_list,"mensaje":f"  {usuario}, Bienvenido!"} )

            else:

                return render(request,"APP_B_1/login.html",{"mensaje":"Error, datos incorrectos"})

        else:
                return render(request,"APP_B_1/login.html",{"mensaje":"Error, formulario erroneo"})

    form = AuthenticationForm()

    return render(request, "APP_B_1/login.html",{'form':form})

def Registro_V(request):

    if request.method == 'POST':

        form = UserRegisterForm(request.POST)

        if form.is_valid():

            usuario= form.cleaned_data['username']
            new_user=form.save()
            # Para loguearse al crear nuevo usuario
            login(request, new_user)
            # Redirecciono a Perfil con usuario ya logueado
            return render(request,"APP_B_1/mi_blog.html",{"mensaje":f" {usuario}, Bienvenido! Tu pefil se ha creado con éxito."})
    
    else:
        form = UserRegisterForm()


    return render(request,'APP_B_1/registro.html', {"form":form})


@login_required
def Mi_Blog_V(request):
    usuario=  request.user
    post_list =  Post.objects.filter(status=1,author=usuario).order_by('-created_on')

    return render(request,'APP_B_1/mi_blog.html',{'post_list':post_list,"mensaje":f" {usuario}", "avatar":obtenerAvatar(request)} )

def About_V(request):
    return render(request,'APP_B_1/about.html')


@login_required
def Crear_post(request):

    if request.method != 'POST':
        #GET. Paso formulario vacio
        form = NuevoPost()
    
    else:
        # POST. Paso formulario con datos ingresados por POST 
        form = NuevoPost(request.POST, request.FILES)
        if form.is_valid():
            post_nuevo = form.save(commit=False)
            post_nuevo.author = request.user
            post_nuevo.status=True
            #En cuanto a la siguiente línea:Había una manera mas sencilla, usando userid. Pero ya estaba implentada con slugs, 
            # se hizo este arreglo para crear una identidad única por post.
            post_nuevo.slug= (str(post_nuevo.author)+str(post_nuevo.title)).replace(" ", "").lower() 
            post_nuevo.save()

            return redirect('posts')

    context = {
        'form': form, 
        'title': 'Nuevo Post',
    }
    return render(request, 'APP_B_1/crear_post.html', context)


@login_required
def Editar_Post_V(request, slug):
    """Edit an existing post."""


    # Post que se va a editar
    post = Post.objects.get(slug=slug)

    if request.method != 'POST':
        # No data submitted. Formulario ya poblado con los datos a editar (antes de enviar/guardar)
        form = NuevoPost(instance=post)

    else:
        # Data submitted. Formulario para guardar con los datos enviados por POST
        form = NuevoPost(data=request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            form.save()

            return redirect('posts')
            
    context = {
        'title': 'Edit',
        'subtitle': post.title,
        'form': form,
    }
    return render(request, 'APP_B_1/editar_post.html', context)

@login_required
def Eliminar_Post_V(slug):
    #Delete post
    
    # Post que se va a borrar
    post = Post.objects.get(slug=slug)
    post.delete()
    return redirect('posts')

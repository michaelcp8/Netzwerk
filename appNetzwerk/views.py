#encoding: utf-8
import re
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from appNetzwerk.models import Usuario, Mensaje
from appNetzwerk.forms import registroUsuariosForm, editUsuariosForm, editPasswordForm, publicarMensajeForm
from appNetzwerk.funciones import tendencias
from django.contrib.auth.decorators import login_required

# Create your views here.

def registroUsuarios(request):
	if request.method == 'POST':
		form = registroUsuariosForm(request.POST, request.FILES)

		if form.is_valid():
			# Asignamos a las variables para crear el usuario
            		username = request.POST['username']
			password = request.POST['password']
			email = request.POST['email']
			first_name = request.POST['first_name']

			if not re.match('^[a-zA-Z0-9_]+$', username):
				mensaje="El nombre de usuario solo puede contener letras, numeros y _"
				return render(request, 'appNetzwerk/register.html', {'form':form, 'mensaje':mensaje})

			password = request.POST['password']
			email = request.POST['email']
			first_name = request.POST['first_name']
			
			user = Usuario.objects.create_user(username, email, password)
            		user.first_name = first_name
 
           		# Guardamos el usuario
            		user.save()
			return redirect('/')
		elif Usuario.objects.filter(username = request.POST['username']):
			mensaje="El usuario ya existe."
			return render(request, 'appNetzwerk/register.html', {'form':form, 'mensaje':mensaje})
		else:
			mensaje="Todos los campos son obligatorios."
			return render(request, 'appNetzwerk/register.html', {'form':form, 'mensaje':mensaje})
	else:
		form = registroUsuariosForm()

	context = {'form':form}
	return render(request, 'appNetzwerk/register.html', context)

def userLogin(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			user = request.POST['username']
			passwd = request.POST['password']
			access = authenticate(username=user, password=passwd)
			if access is not None and access.is_active:
				login(request, access)
				return redirect('/%s/' % user)
		else:
			mensaje = "Usuario o contraseña incorrecta."
			return render(request, 'appNetzwerk/index.html', {'form':form, 'mensaje':mensaje})
	else:
		form = AuthenticationForm()
	context = {'form':form}
	return render(request, 'appNetzwerk/index.html', context)


@login_required(login_url='/')
def userLogout(request):
	logout(request)
	return redirect('/')

@login_required(login_url='/')
def editUsuarios(request):
	if request.method == 'POST':
		usuario = Usuario.objects.get(username = request.user)
		form = editUsuariosForm(request.POST, request.FILES, instance=usuario)
		if form.is_valid():
           		# Guardamos el usuario editado
            		form.save()
			return redirect('/%s/' % usuario)
	else:
		usuario = Usuario.objects.get(username = request.user)
		form = editUsuariosForm(instance=usuario)

	context = {'form':form, 'usuario':usuario}
	return render(request, 'appNetzwerk/editusuario.html', context)

@login_required(login_url='/')
def editPassword(request):
	if request.method == 'POST':
		usuario = Usuario.objects.get(username = request.user)
		form = editPasswordForm(request.POST, request.FILES)
		if form.is_valid():
			# Asignamos a las variables para modificar la contraseña
			oldpasswd = request.POST['oldpassword']
			passwd = request.POST['password']
			
			if usuario.check_password(oldpasswd):
		   		# Set de la contraseña y guardamos
		    		usuario.set_password(passwd)
				usuario.save()
				access = authenticate(username=usuario.username, password=passwd)
				login(request, access)
				return redirect('/%s/' % usuario)
			else:
			       mensaje ="Contraseña actual incorrecta."
			       return render(request, 'appNetzwerk/editpassword.html', {'form':form, 'usuario':usuario, 'mensaje':mensaje})
	else:
		usuario = Usuario.objects.get(username = request.user)
		form = editPasswordForm()

	context = {'form':form, 'usuario':usuario}
	return render(request, 'appNetzwerk/editpassword.html', context)

@login_required(login_url='/')
def home(request):
	# Usamos .distinct() para que, con los rewerk nos muestre solo una vez
	usuario = Usuario.objects.get(username = request.user)
	mensajesPropios = Mensaje.objects.filter(usuario = usuario).distinct()
	mensajesSeguidores = Mensaje.objects.filter(usuario = usuario.seguidores.all()).distinct()
	mensajesRewerkSeguidores = Mensaje.objects.filter(rewerk = usuario.seguidores.all()).distinct()
	mensajesRewerkPropios = Mensaje.objects.filter(rewerk = usuario).distinct()
	mensajes = mensajesPropios | mensajesSeguidores | mensajesRewerkSeguidores | mensajesRewerkPropios
	numMensajes = len(mensajesPropios)
	mensajes = mensajes.order_by("fecha").reverse()

	# Si el usuario ha rewerkeado un mensaje, se le suma uno a sus werk
	for mensaje in mensajes:
		if usuario in mensaje.rewerk.all():
			numMensajes +=1

	if request.method == 'POST':
		form = publicarMensajeForm(request.POST, request.FILES)

		if form.is_valid():
			mensaje = form.save(commit=False)
			mensaje.usuario = usuario
			mensaje.save()
			return redirect('/%s/' % usuario)
	else:
		form = publicarMensajeForm()

	context = {'usuario':usuario, 'form':form, 'mensajes':mensajes, 'numMensajes':numMensajes, 'tendencias':tendencias()}
	return render(request,'appNetzwerk/home.html', context)

@login_required(login_url='/')
def deleteMensaje(request, mensaje_id):
	mensaje = Mensaje.objects.get(pk = mensaje_id)
	mensaje.delete()

	#Redireccionamos a la página donde estábamos
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def deleteUsuario(request):
	usuario = Usuario.objects.get(username = request.user)
	mensajes = Mensaje.objects.filter(usuario = usuario).all()
	mensajes.delete()
	usuario.delete()

	return redirect('/')

@login_required(login_url='/')
def rewerkMensaje(request, mensaje_id):
	usuario = Usuario.objects.get(username = request.user)
	mensaje = Mensaje.objects.get(pk = mensaje_id)

	if (usuario in mensaje.rewerk.all()): # Devuelve True si el usuario tiene el werk en favorito
		mensaje.rewerk.remove(usuario)
	else:
		mensaje.rewerk.add(usuario)

	#Redireccionamos a la página donde estábamos
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def favMensaje(request, mensaje_id):
	usuario = Usuario.objects.get(username = request.user)
	mensaje = Mensaje.objects.get(pk = mensaje_id)

	if (usuario in mensaje.fav.all()): # Devuelve True si el usuario tiene el werk en favorito
		mensaje.fav.remove(usuario)
	else:
		mensaje.fav.add(usuario)

	#Redireccionamos a la página donde estábamos
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def seguirUsuario(request, usuario):
	usuario = Usuario.objects.get(username = usuario)
	user = Usuario.objects.get(username = request.user)
	
	seguidores = user.seguidores.all() # Los seguidores del usuario logueado

	if (usuario in seguidores): # Devuelve True si el usuario esta entre los seguidores del logueado
		user.seguidores.remove(usuario)
	else:
		user.seguidores.add(usuario)

	#Redireccionamos a la página donde estábamos
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))	

@login_required(login_url='/')
def mostrarUsuario(request, usuario):
	user = Usuario.objects.get(username = request.user)
	# Comprobamos que el usuario exista, ya que se pueden equivocar en las menciones
	if Usuario.objects.filter(username = usuario):
		flag = True
		usuario = Usuario.objects.get(username = usuario)
		mensajesPropios = Mensaje.objects.filter(usuario = usuario).distinct()
		mensajesRewerk = Mensaje.objects.filter(rewerk = usuario).distinct()
		mensajes = mensajesPropios | mensajesRewerk
		mensajes = mensajes.order_by("fecha").reverse()
		numMensajes = len(mensajesPropios)

		# Si el usuario ha rewerkeado un mensaje, se le suma uno a sus werk
		for mensaje in mensajes:
			if usuario in mensaje.rewerk.all():
				numMensajes +=1


		seguidores = user.seguidores.all() # Los seguidores del usuario logueado
		siguiendo= (usuario in seguidores) # Devuelve True si el usuario esta entre los seguidores del logueado
		context = {'usuario':usuario, 'mensajes':mensajes, 'user':user, 'numMensajes':numMensajes, 'siguiendo':siguiendo, 'flag':flag}
		return render(request,'appNetzwerk/mostrarUsuario.html', context)
	else:
		flag = False
		context = {'user':user, 'flag':flag}
		return render(request,'appNetzwerk/mostrarUsuario.html', context)

@login_required(login_url='/')
def mostrarSeguidores(request, user, metodo, usuario):
	usuario = Usuario.objects.get(username = usuario)
	user = Usuario.objects.get(username = request.user)
	mensajesPropios = Mensaje.objects.filter(usuario = usuario).distinct()
	mensajesRewerk = Mensaje.objects.filter(rewerk = usuario).distinct()
	mensajes = mensajesPropios | mensajesRewerk
	numMensajes = len(mensajesPropios)

	# Si el usuario ha rewerkeado un mensaje, se le suma uno a sus werk
	for mensaje in mensajes:
		if usuario in mensaje.rewerk.all():
			numMensajes +=1

	if metodo == 'seguidores':
		seguidores = usuario.seguido_por.all()
		flag=True
	else:
		seguidores = usuario.seguidores.all()
		flag = False
	
	context = {'user':user, 'seguidores':seguidores, 'usuario':usuario, 'numMensajes':numMensajes, 'flag':flag}
	return render(request,'appNetzwerk/mostrarSeguidores.html', context)

@login_required(login_url='/')
def mostrarFavoritos(request, usuario):
	user = Usuario.objects.get(username = request.user)
	usuario = Usuario.objects.get(username = usuario)
	mensajesPropios = Mensaje.objects.filter(usuario = usuario).distinct()
	mensajesRewerk = Mensaje.objects.filter(rewerk = usuario).distinct()
	mensajes = mensajesPropios | mensajesRewerk
	numMensajes = len(mensajesPropios)

	mensajesFav = Mensaje.objects.filter(fav = usuario).order_by("fecha").reverse()

	# Si el usuario ha rewerkeado un mensaje, se le suma uno a sus werk
	for mensaje in mensajes:
		if usuario in mensaje.rewerk.all():
			numMensajes +=1


	seguidores = user.seguidores.all() # Los seguidores del usuario logueado
	siguiendo= (usuario in seguidores) # Devuelve True si el usuario esta entre los seguidores del logueado


	context = {'usuario':usuario, 'mensajesFav':mensajesFav, 'numMensajes':numMensajes, 'user':user, 'siguiendo':siguiendo}
	return render(request,'appNetzwerk/mostrarFavoritos.html', context)

@login_required(login_url='/')
def buscar(request):
	#Formulario de búsqueda
	query = request.GET.get('busqueda', '')
	menciones = False
	flag = False # Hashtag o usuario
	usuario = Usuario.objects.get(username = request.user)

	if query:
		if re.findall('^#[a-zA-Z][a-zA-Z0-9_]*', query): # Hashtags
			mset = (
			Q(texto__icontains=query)
			)
			resultado = Mensaje.objects.filter(mset)
			flag = True

		elif re.findall('^@[a-zA-Z0-9_]*', query): # Menciones
			menciones = True
			mset = (
			Q(texto__icontains=query)
			)
			resultado = Mensaje.objects.filter(mset)

		else: # Nombre o usuario
			uset = (
			Q(username__icontains=query) |
			Q(first_name__icontains=query)
			)
			resultado = Usuario.objects.filter(uset)
		
		context = {"resultado": resultado ,"query": query, 'usuario':usuario, 'flag':flag, 'menciones':menciones}
		return render(request,'appNetzwerk/busqueda.html', context)

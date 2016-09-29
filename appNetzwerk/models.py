#encoding: utf-8
from django.db import models
from django.contrib.auth.models import User
import re # Expresiones regulares
from urllib import urlencode

class Usuario(User):
	biografia = models.CharField(max_length=200, null = True, blank = True)
	imagenPerfil = models.ImageField(upload_to='perfil', null=True, blank=True)
	seguidores = models.ManyToManyField('self', related_name='seguido_por', symmetrical=False)

	def __unicode__(self):
		return self.username

class Mensaje(models.Model):
	texto = models.CharField(max_length=140)
	usuario = models.ForeignKey(Usuario)
    	fecha = models.DateTimeField(auto_now=True, blank=True)
	rewerk = models.ManyToManyField(Usuario, related_name='rewerkeado_por')
	fav = models.ManyToManyField(Usuario, related_name='favorito_de')

	def __unicode__(self):
		return self.texto

	def filtrar(self):
		# Reconocer hashtags, menciones o páginas
		mensaje = self.texto

		hashtags = re.findall('#[a-zA-Z][a-zA-Z0-9_]*', mensaje) # Se crea una lista de los hastags
		for hashtag in hashtags:
			mensaje = mensaje.replace(hashtag, '<a href="/buscar/?%s">%s</a>' % (urlencode({'busqueda':hashtag}), hashtag))
		
		links = re.findall('[^ ]+\.[a-z/0-9]+', mensaje)
		for link in links:
			if re.findall('^http', link):
				mensaje = mensaje.replace(link, '<a target="_blank" href="%s">%s</a>' % (link, link))
			else:
				mensaje = mensaje.replace(link, '<a target="_blank" href="http://%s">%s</a>' % (link, link))

		menciones = re.findall('\\@[a-zA-Z0-9_]+', mensaje)
		for mencion in menciones:
			mensaje = mensaje.replace(mencion, '<a href="/mostrar/%s/">%s</a>' % (mencion[1:], mencion))

		return mensaje

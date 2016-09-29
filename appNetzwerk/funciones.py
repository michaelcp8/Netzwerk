#encoding: utf-8
from appNetzwerk.models import Mensaje, Usuario
import re # Expresiones regulares

def tendencias():
	hashtags = {} # Creamos el diccionario
	mensajes = Mensaje.objects.all().order_by("fecha")[:500] # Obtenemos los 500 últimos mensajes

	for mensaje in mensajes:
		aux = re.findall('#[a-zA-Z][a-zA-Z0-9_]*', mensaje.texto, re.IGNORECASE) # Filtramos los hashtags de los mensajes
		for hashtag in aux:
			# Si el hastag esta en el diccionario, incrementamos; si no esta en el diccionario le asignamos el valor 1
			# y se añadiria al diccionario
			if hashtag in hashtags: 
				hashtags[hashtag] += 1
			else:
				hashtags[hashtag] = 1
	
	# Creamos una lista para ordenar el numero de veces que se ha utilizado el hashtag, siendo el primer elemento el numero de veces
	# que aparece el hashtag en los mensajes y el segundo es el nombre del hashtag
	aux = []
	for hashtag in hashtags.keys(): # key() Nos devuelve las palabras del diccionario, en nuestro caso los hashtag
		aux.append((hashtags[hashtag], hashtag))

	aux.sort() # Ordenamos la lista con sort() que ordena de menor a mayor
	aux.reverse() # La revertimos para que sea de mayor a menor

	tendencias = []
	# Cogemos solo el nombre del hashtag, entre los 5 mas utilizados
	for i in aux[:5]:
		# Le quitamos el primer carácter porque a la hora de hacer una búsqueda de los hashtags en la página, la almohadilla '#'
		# se corresponde con la codificación %23 para la transmición correcta por internet.
		tendencias.append(i[1][1:])
	return tendencias

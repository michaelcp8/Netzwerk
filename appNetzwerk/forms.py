#encoding: utf-8
from django.forms.extras.widgets import SelectDateWidget
from django.forms import ModelForm
from django import forms
from appNetzwerk.models import Mensaje, Usuario

class registroUsuariosForm(ModelForm):
	username = forms.CharField(required=True, max_length=20)
	email = forms.EmailField(required=True)
    	first_name = forms.CharField(required=True, max_length=25)

	class Meta:
	        model = Usuario

	        fields = ['username', 'first_name', 'password', 'email']
        
		widgets = {
			'password': forms.PasswordInput(),
	        }


class editUsuariosForm(ModelForm):
	class Meta:
	        model = Usuario

		fields = ['first_name', 'email', 'biografia', 'imagenPerfil']
        
		widgets = {
			'password': forms.PasswordInput(),
			'biografia': forms.Textarea(attrs={'cols': 30, 'rows': 5})
	        }

class editPasswordForm(ModelForm):
	oldpassword = forms.CharField(required=True, widget=forms.widgets.PasswordInput())

	class Meta:
	        model = Usuario

		fields = ['oldpassword', 'password']
        
		widgets = {
			'password': forms.PasswordInput(),
	        }

class publicarMensajeForm(ModelForm):
	class Meta:
	        model = Mensaje

	        fields = ['texto']
        
		widgets = {
			'texto': forms.Textarea(attrs={'cols': 25, 'rows': 5, 'placeholder': 'Escribe tu werk...'})
	        }	
		

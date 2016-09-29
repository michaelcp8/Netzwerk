from django.conf.urls import patterns, url
from appNetzwerk import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

#^$ --> es una cadena vacia
 
urlpatterns = patterns('',
	url(r'^$', views.userLogin, name='userLogin'),
	url(r'^logout/$', views.userLogout, name='userLogout'),
	url(r'^register/$', views.registroUsuarios, name='registroUsuarios'),
	url(r'^buscar/$', views.buscar, name='buscar'),
	url(r'^\w+/$', views.home, name='home'),
	url(r'^\w+/edit/$', views.editUsuarios, name='editUsuarios'),
	url(r'^\w+/password/$', views.editPassword, name='editPassword'),
	url(r'^\w+/(?P<mensaje_id>\d+)/delete/$', views.deleteMensaje, name='deleteMensaje'),
	url(r'^\w+/(?P<mensaje_id>\d+)/rewerk/$', views.rewerkMensaje, name='rewerkMensaje'),
	url(r'^\w+/(?P<mensaje_id>\d+)/fav/$', views.favMensaje, name='favMensaje'),
	url(r'^\w+/delete/$', views.deleteUsuario, name='deleteUsuario'),
	url(r'^fav/(?P<usuario>\w+)$', views.mostrarFavoritos, name='mostrarFavoritos'),
	url(r'^mostrar/(?P<usuario>\w+)/$', views.mostrarUsuario, name='mostrarUsuario'),
	url(r'^\w+/follow/(?P<usuario>\w+)/$', views.seguirUsuario, name='seguirUsuario'),
	url(r'^(?P<user>\w+)/(?P<metodo>(seguidores|siguiendo))/(?P<usuario>\w+)/$', views.mostrarSeguidores, name='mostrarSeguidores'),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

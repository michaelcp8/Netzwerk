from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls.static import static
from appNetzwerk import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Netzwerk.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	#url(r'^$', TemplateView.as_view (template_name='base.html'), name='base'),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^', include('appNetzwerk.urls')),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

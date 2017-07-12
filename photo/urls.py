#-*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.static import serve

from website import views

from filebrowser.sites import site

urlpatterns = [
    # static.serve debe ser usado solo en dev environment Fuck!
	# url(r'^static/(?P<path>.*)$',serve,{'document_root': settings.STATIC_ROOT}),

    url(r'^admin/filebrowser/', include(site.urls)), # filebrowser URLS
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='home'),
    url(r'^setup/$', views.setup, name='setup'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^tag/(?P<tag>[a-z0-9-]+)/$', views.tag, name='tag'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

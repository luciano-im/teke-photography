#-*- coding: utf-8 -*-

import os

from django.forms import ModelForm
from django import forms

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group
from django.template.loader import render_to_string

from website.models import Photo, Photos

#from sorl.thumbnail import get_thumbnail

# Unregister models
admin.site.unregister(Group)


class PhotosInline(admin.TabularInline):
	model = Photos
	extra = 1

class PhotoAdmin(admin.ModelAdmin):
	inlines = [PhotosInline, ]
	list_display = ('date_created','date_modified', 'tag_list', 'image_list')
	allow_tags = True

	def get_queryset(self, request):
		return super(PhotoAdmin, self).get_queryset(request).prefetch_related('tags')

	def tag_list(self, obj):
		return u", ".join(o.name for o in obj.tags.all())

	tag_list.short_description = 'Tags'

	def image_list(self, obj):
		#return "".join('<img src="'+os.path.join(settings.MEDIA_URL, str(o.image))+'"/>' for o in obj.photos_set.all())
		return render_to_string('admin_thumb.html',{'obj':obj.photos_set.all()})

	image_list.allow_tags = True
	image_list.short_description = 'Fotos'


# Register models
admin.site.register(Photo, PhotoAdmin)

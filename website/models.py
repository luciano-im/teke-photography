#-*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
from time import strftime

from django.db import models
from django.conf import settings

from taggit.managers import TaggableManager
from taggit.models import Tag
from filebrowser.base import FileObject
from filebrowser.fields import FileBrowseField
from filebrowser import signals
from PIL import Image


class Photo(models.Model):

	# def tag_helptext():
	# 	help_text = "Options: "
	# 	for t in Tag.objects.all():
	# 	    help_text += t.name + " ||| "
	# 	return help_text

	photo_id = models.AutoField(primary_key=True)
	date_created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creacion')
	date_modified = models.DateTimeField(auto_now=True, verbose_name='Fecha de Modificacion')
	tags = TaggableManager(verbose_name='Tags')
	# tags = TaggableManager(verbose_name='Tags', help_text=tag_helptext())

	class Meta:
		verbose_name = 'Foto'
		verbose_name_plural = 'Fotos'

	def __unicode__(self):
		return unicode(self.date_created)


class Photos(models.Model):
	photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
	image = FileBrowseField(verbose_name='Foto', max_length=200, extensions=['.jpg','.png'])

	class Meta:
		verbose_name = 'Foto'
		verbose_name_plural = 'Fotos'

	def post_upload(sender, **kwargs):
		#print "Post Upload"
		#print "kwargs:", kwargs
		path_root = kwargs['file'].head
		filename = kwargs['file'].filename
		ext = kwargs['file'].extension
		datetime = kwargs['file'].datetime
		new_name = datetime.strftime('%Y%m%d%H%M%S%f') + ext
		old_file = os.path.join(settings.MEDIA_ROOT, path_root, filename)
		new_file = os.path.join(settings.MEDIA_ROOT, path_root, new_name)
		#print "old_file:", old_file
		#print "new_file:", new_file
		os.rename(old_file, new_file)
		try:
			size = (1000, 1000)
			im = Image.open(new_file)
			im.thumbnail(size)
			im.save(new_file, im.format)
		except IOError:
			print("cannot create image for", new_file)


	signals.filebrowser_post_upload.connect(post_upload)

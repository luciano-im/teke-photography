#-*- coding: utf-8 -*-

import json
import random

from django.conf import settings
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.vary import vary_on_headers

from website.models import Photos, Photo

def get_random_list(photos):
	random_list = list(photo['id'] for photo in photos)
	random.shuffle(random_list)

	# print random_list
	return random_list

def get_ajax_response(request):
	response = request.session['ids'][:settings.ITEMS_PER_PAGE]
	random_ids =  request.session['ids'][settings.ITEMS_PER_PAGE:]
	request.session['ids'] = random_ids
	photos = Photos.objects.filter(id__in=response)
	data = []
	for photo in photos:
		pic = {}
		pic['original'] = photo.image.url
		# Media URL + Version's folder + Version file
		pic['thumb'] = settings.MEDIA_URL + photo.image.version_path('thumbnail')
		data.append(pic)

	return data

def get_photos_response(request, tag):
	if request.is_ajax():
		# print "ES AJAXXXXXXXX"
		return {'ajax':get_ajax_response(request)}
	else:
		# print "ES GETTTTTTTTT"
		if tag:
			photos = Photos.objects.filter(photo__tags__slug = tag).values('id')
			# print "Photos por TAG(", tag, "):", photos
		else:
			photos = Photos.objects.values('id')
			# print "Photos:", photos
		random_ids = get_random_list(photos)
		response = random_ids[:settings.ITEMS_PER_PAGE]
		request.session['ids'] = random_ids[settings.ITEMS_PER_PAGE:]
		photos = Photos.objects.filter(id__in=response)

		return {'photos':photos}

# Inlcude this decorator to process again the ajax view when use browser back button
@vary_on_headers('X-Requested-With')
def index(request):
	response = get_photos_response(request, None)
	# print response
	# print request.session['ids']
	if response.get('photos'):
		return render(request, 'index.html', {'photos':response['photos'], 'tags':Photo.tags.all()})
	else:
		return HttpResponse(json.dumps(response['ajax']), content_type='application/json')


def tag(request, tag):
	response = get_photos_response(request, tag)
	if response.get('photos'):
		return render(request, 'index.html', {'photos':response['photos'], 'tags':Photo.tags.all()})
	else:
		return HttpResponse(json.dumps(response['ajax']), content_type='application/json')


def setup(request):
	return render(request, 'setup.html')

def contact(request):
	return render(request, 'contact.html')

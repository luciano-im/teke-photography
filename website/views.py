#-*- coding: utf-8 -*-

import json
import random

from django.conf import settings
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse

from website.models import Photos, Photo

def get_random_list(photos):
	random_list = list(photo['id'] for photo in photos)
	random.shuffle(random_list)

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
		pic['thumb'] = settings.MEDIA_URL + photo.image.versions_basedir + '/' + photo.image.version_name('thumbnail')
		data.append(pic)

	return data

def get_photos_response(request, tag):
	if request.is_ajax():
		return {'ajax':get_ajax_response(request)}
	else:
		if tag:
			photos = Photos.objects.filter(photo__tags__slug = tag).values('id')
		else:
			photos = Photos.objects.values('id')
		random_ids = get_random_list(photos)
		response = random_ids[:settings.ITEMS_PER_PAGE]
		request.session['ids'] = random_ids[settings.ITEMS_PER_PAGE:]
		photos = Photos.objects.filter(id__in=response)

		return {'photos':photos}


def index(request):
	response = get_photos_response(request, None)
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

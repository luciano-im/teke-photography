#-*- coding: utf-8 -*-

import random

from django.conf import settings
from django.shortcuts import render

from website.models import Photos, Photo

def get_random_list(photos):
	random_list = list(photo['id'] for photo in photos)
	random.shuffle(random_list)

	return random_list

def get_photos_response(request, tag):
	if tag:
		photos = Photos.objects.filter(photo__tags__slug = tag).values('id')
	else:
		photos = Photos.objects.values('id')
	random_ids = get_random_list(photos)
	photos = Photos.objects.filter(id__in=random_ids)

	return {'photos':photos}


def index(request):
	response = get_photos_response(request, None)

	return render(request, 'index.html', {'photos':response['photos'], 'tags':Photo.tags.all()})


def tag(request, tag):
	response = get_photos_response(request, tag)

	return render(request, 'index.html', {'photos':response['photos'], 'tags':Photo.tags.all()})


def setup(request):
	return render(request, 'setup.html')


def contact(request):
	return render(request, 'contact.html')

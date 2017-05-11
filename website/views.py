#-*- coding: utf-8 -*-

import json
import random 

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse

from website.models import Photos, Photo

def index(request):
	if request.is_ajax():
		response = request.session['ids'][:settings.ITEMS_PER_PAGE]
		#print 'response: ', response
		random_ids =  request.session['ids'][settings.ITEMS_PER_PAGE:]
		request.session['ids'] = random_ids
		photos_list = Photos.objects.in_bulk(response)
		ordered_photos = [photos_list.get(id,None) for id in response]
		photos = filter(None, ordered_photos)
		data = []
		for photo in photos:
			data.append(photo.image.url)

		return HttpResponse(json.dumps(data), content_type='application/json')
	else:
		max_id = Photos.objects.all().order_by("-id")[0]
		#print xrange(1, max_id.id)
		random_ids = random.sample(xrange(1, max_id.id+1), max_id.id)
		response = random_ids[:settings.ITEMS_PER_PAGE]
		#print 'random_ids: ', random_ids
		request.session['ids'] = random_ids[settings.ITEMS_PER_PAGE:]
		#print 'response: ', response
		photos_list = Photos.objects.in_bulk(response)
		ordered_photos = [photos_list.get(id,None) for id in response]
		photos = filter(None, ordered_photos)

		tags = Photo.tags.all()

		return render(request, 'index.html', {'photos':photos, 'tags':tags})


def setup(request):
	return render(request, 'setup.html')


def tag(request, tag):
	tags = Photo.objects.filter(tags__slug=tag)
	photos = Photos.objects.filter(photo=tags)
	
	return render(request, 'index.html', {'photos':photos})
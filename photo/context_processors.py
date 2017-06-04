#-*- coding: utf-8 -*-

def whereIAm(request):
	urlpath = request.path.strip('/').split("/")
	print urlpath
	# whereIAm = urlpath[0]
	
	return {'whereIAm': urlpath}

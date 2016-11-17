def whereIAm(request):
	urlpath = request.path.strip('/').split("/")
	whereIAm = urlpath[0]
	
	return {'whereIAm': whereIAm}
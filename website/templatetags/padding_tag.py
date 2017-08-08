from django import template

register = template.Library()

@register.assignment_tag
def padding_tag(height, width):
	# print float(height)
	# print float(width)
	res = float(height) / float(width)
	res = res * 100
	print res
	return res

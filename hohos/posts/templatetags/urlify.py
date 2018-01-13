# this is the place to register custom filters to the things you want like the below one adds
# a filter urlify which uses function quote_plus(),  
# quote_plus splits the content using plus that is it makes it url encoded text type to encode in urls


from urllib import quote_plus 
from django import template

register = template.Library()

@register.filter
def urlify(value):
	return quote_plus(value)
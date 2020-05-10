from django import template

register = template.Library()

# A template to assist generating the rating form
@register.filter(name="int_range")
def int_range(count):
	return range(int(count))
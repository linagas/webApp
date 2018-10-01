from django import template
register = template.Library()

@register.filter(name='zip')
def zip_lists(a, b):
  if b:
    return zip(a, b)
  else:
    return {}
from django import template
import json

register = template.Library()

@register.filter(name='zip')
def zip_lists(a, b):
  if b:
    return zip(json.loads(a), json.loads(b))
  else:
    return {}
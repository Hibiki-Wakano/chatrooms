from django import template
from .. import models
register = template.Library()




@register.filter
def analyze(object):
    config = models.Config.objects.get()
    try:
        name = object.data['name']
        value = object.data['value']
    except:
        return object
    if name == 'friend':
        pass
    return object
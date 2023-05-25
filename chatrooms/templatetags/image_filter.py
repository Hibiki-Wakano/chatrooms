from django import template
register = template.Library()

@register.filter
def image_filter(image_field):
    if image_field != 'False':
        return '/media/'+str(image_field)
    else:
        return False
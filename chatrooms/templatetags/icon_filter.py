from django import template
register = template.Library()

@register.filter
def icon_filter(icon_field):
    if icon_field != 'False':
        return '/media/'+str(icon_field)
    else:
        return '/media/icon/none.png'
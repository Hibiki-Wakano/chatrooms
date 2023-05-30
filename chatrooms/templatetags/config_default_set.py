from django import template
register = template.Library()


@register.filter
def config_default_set(object):
    object.data['selected'] = True
    object.data['attrs']['checked'] = True
    print(vars(object.parent_widget))
    return object
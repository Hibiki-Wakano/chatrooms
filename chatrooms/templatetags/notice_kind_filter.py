from django import template
from .. import models
register = template.Library()

@register.filter
def notice_kind_filter(kind):
    return models.Notice.kind_list[kind][1]
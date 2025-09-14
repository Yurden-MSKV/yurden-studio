from django import template
from django.utils.html import mark_safe
import re

register = template.Library()


@register.filter
def add_nbsp(value):
    if not value:
        return ""
    return mark_safe(value.replace(' — ', '&nbsp;— '))
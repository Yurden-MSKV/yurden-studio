from django import template

register = template.Library()

@register.filter
def reverse_list(value):
    """Переворачивает список"""
    return list(reversed(value))
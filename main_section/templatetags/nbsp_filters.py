from django import template
from django.utils.html import mark_safe
import re

register = template.Library()


@register.filter
def add_nbsp(value):
    if not value:
        return ""

    patterns = [
        # (r'(\s)([а-яёa-z]{1,2}\s)', r'&nbsp;\2'),
        (r'(\s)(—)', r'&nbsp;\2'),
        # (r'(\s)(г\.)', r'&nbsp;\2'),
        # (r'(\s)(№)', r'&nbsp;\2'),
    ]

    for pattern, replacement in patterns:
        value = re.sub(pattern, replacement, value)

    return mark_safe(value)
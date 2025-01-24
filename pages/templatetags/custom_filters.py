from django import template

register = template.Library()


@register.filter
def first_part(email):
    return email.split("@")[0]

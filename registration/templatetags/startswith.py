from django import template

register = template.Library()


@register.filter("startswith")
def startswith(text, starts):
    return text.startswith(starts)


def key(d, key_name):
    return d[key_name]


key = register.filter("key", key)

import json

from django import template

register = template.Library()


@register.filter
def loadjson(data):
    print(type(data))
    return json.loads(data)

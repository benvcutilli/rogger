from django import template

register = template.Library()

@register.filter
def prettydecimal(thing):
    stringThing = str(thing)
    if len(stringThing) == 0:
        return ""
    index = len(stringThing) - 1
    while stringThing[index] == '0' and stringThing[index] != '.':
        index -= 1
    if stringThing[index] == '.':
        return stringThing[:index]
    else:
        return stringThing[:index+1]

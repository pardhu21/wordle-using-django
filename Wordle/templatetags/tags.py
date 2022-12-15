from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def index(context, a, b, c):
    request = context['request']
    return request.session[a][int(b)][c]

@register.simple_tag(takes_context=True)
def is_disabled(context, j):
    request = context['request']
    return not request.session['guess_counter'] == int(j)
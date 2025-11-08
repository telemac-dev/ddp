from django import template
from django.urls import resolve, reverse
from ..menu import get_menu_items

register = template.Library()

@register.inclusion_tag('accounts/tags/menu.html', takes_context=True)
def render_menu(context):
    user = context['user']
    request = context['request']
    current_url = request.path

    menu_items = get_menu_items(user)
    
    return {
        'menu_items': menu_items,
        'current_url': current_url,
        'user': user
    }
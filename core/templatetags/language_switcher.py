from django import template
from django.conf import settings
from django.urls import translate_url
from django.utils.translation import get_language, get_language_info

register = template.Library()

@register.simple_tag(takes_context=True)
def change_language(context, lang_code, *args, **kwargs):    
    """
    Get the URL for the current page in the specified language.
    Usage: {% change_language 'en' %}
    """
    path = '/'  # Default to root path
    
    # Try to get the request from context
    request = None
    if 'request' in context:
        request = context['request']
    
    if request:
        path = request.path
        # Handle the case where we're already on a language-prefixed URL
        path_components = path.lstrip('/').split('/')
        if path_components and path_components[0] in dict(settings.LANGUAGES).keys():
            path = '/' + '/'.join(path_components[1:]) if len(path_components) > 1 else '/'
    
    # Use Django's built-in translate_url function
    translated_url = translate_url(path, lang_code)
    return translated_url or f'/{lang_code}/'

@register.inclusion_tag('partials/language_switcher.html', takes_context=True)
def language_switcher(context):
    """
    Render a language switcher dropdown.
    Usage: {% language_switcher %}
    """
    current_language = get_language()
    languages = []
    
    for code, name in settings.LANGUAGES:
        lang_info = get_language_info(code)
        languages.append({
            'code': code,
            'name': name,
            'name_local': lang_info['name_local'],
            'is_current': code == current_language,
        })
    
    return {
        'languages': languages,
        'current_language': current_language,
    }

from django.utils import translation
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import get_script_prefix, is_valid_path
from django.utils.cache import patch_vary_headers
from django.utils.deprecation import MiddlewareMixin

class LanguageMiddleware(MiddlewareMixin):
    """
    This is a simplified version of Django's LocaleMiddleware that:
    1. Doesn't redirect for the default language (en)
    2. Only adds language prefix for non-default languages
    """
    response_redirect_class = HttpResponseRedirect

    def process_request(self, request):
        # Check if language is in the URL
        path = request.path_info
        language = settings.LANGUAGE_CODE  # Default language
        
        # Check if the first part of the URL is a language code
        path_components = path.lstrip('/').split('/')
        if path_components and path_components[0] in dict(settings.LANGUAGES).keys():
            language = path_components[0]
            
        # If it's the default language and it's in the URL, remove it
        if language == settings.LANGUAGE_CODE and path_components and path_components[0] == language:
            new_path = '/' + '/'.join(path_components[1:]) if len(path_components) > 1 else '/'
            return self.response_redirect_class(new_path)
            
        # If it's a non-default language and not in the URL, add it
        if language != settings.LANGUAGE_CODE and (not path_components or path_components[0] != language):
            new_path = f'/{language}{path}'
            return self.response_redirect_class(new_path)
            
        # Set the language for this request
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()
        
    def process_response(self, request, response):
        language = translation.get_language()
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME, language,
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN,
            secure=settings.LANGUAGE_COOKIE_SECURE,
            httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
            samesite=settings.LANGUAGE_COOKIE_SAMESITE,
        )
        patch_vary_headers(response, ('Accept-Language',))
        return response
        
        return response

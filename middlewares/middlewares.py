from django.utils import translation
from users.models import User


class UserLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user_language = User.objects.get(pk=request.user.pk).language
            translation.activate(user_language)
            request.LANGUAGE_CODE = translation.get_language()

        response = self.get_response(request)
        return response

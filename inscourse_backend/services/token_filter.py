from django.http import HttpResponse

from inscourse_backend.services.sys.token import fetch_user_by_token, TOKEN_HEADER_KEY


def acquire_token(func):
    def wrapper(request):
        try:
            user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
            if not user:
                return HttpResponse(content='登录状态已过期', status=401)
        except KeyError:
            return HttpResponse(content='登录状态已过期', status=401)
        return func(request)

    return wrapper

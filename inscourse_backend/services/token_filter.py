from django.http import HttpResponse

from inscourse_backend.services.sys.token import fetch_user_by_token, TOKEN_HEADER_KEY


def acquire_token(func):
    def wrapper(request):
        try:
            print(request.headers)
            user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
            if not user:
                print('no user')
                return HttpResponse(content='Unauthorized', status=401)
        except KeyError:
            print('key error')
            print(request.META)
            return HttpResponse(content='Unauthorized', status=401)
        return func(request)
    return wrapper

import json

from django.http import HttpResponse, HttpResponseBadRequest

from inscourse_backend.models.user import User
from inscourse_backend.services.constants import EM_INVALID_OR_MISSING_PARAMETERS, APP_ID, APP_SECRET
from inscourse_backend.services.sys.token import fetch_user_by_token, TOKEN_HEADER_KEY, update_token
from inscourse_backend.utils.request_processor import fetch_parameter_dict
from inscourse_backend.utils.rpc import do_request


def change_username(request):
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    if not user:
        return HttpResponse(content='Unauthorized', status=401)

    parameter_dict = fetch_parameter_dict(request, 'POST')
    try:
        new_name = parameter_dict['newName']
    except KeyError:
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    user.username = new_name
    user.save()
    return HttpResponse({
        'code': 1,
        'message': u'修改成功'
    })


def login(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    try:
        code = parameter_dict['code']
    except KeyError:
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    openid = _get_openid_of_wx_user(code)
    if not openid:
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)
    print(openid)

    try:
        user = User.objects.get(openid=openid)
        new_token, new_expire_time = update_token(user)
        return HttpResponse(json.dumps({
            'code': 1,
            'message': u'登陆成功',
            'data': user.to_dict(),
            'token': new_token,
            'expire_time': new_expire_time
        }))
    except User.DoesNotExist:
        new_user = User(openid=openid, username='init username')
        new_user.save()
        new_token, new_expire_time = update_token(new_user)
        return HttpResponse(json.dumps({
            'code': 1,
            'message': u'登陆成功',
            'data': new_user.to_dict(),
            'token': new_token,
            'expire_time': new_expire_time
        }))


def _get_openid_of_wx_user(code):
    api_url = "https://api.weixin.qq.com/sns/jscode2session"
    params = {
        'appid': APP_ID,
        'secret': APP_SECRET,
        'js_code': code,
        'grant_type': 'authorization_code'
    }
    status_code, response_dict = do_request('GET', api_url, params=params)
    print('status_code: [%d] and response: %s' % (status_code, response_dict))
    if status_code == 200:
        return response_dict['openid']
    return None

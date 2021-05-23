import json

import requests
from django.http import HttpResponse, HttpResponseBadRequest

from inscourse_backend.models.user import User
from inscourse_backend.services.constants import EM_INVALID_OR_MISSING_PARAMETERS, APP_ID, APP_SECRET
from inscourse_backend.services.sys.token import fetch_user_by_token, TOKEN_HEADER_KEY, update_token
from inscourse_backend.services.token_filter import acquire_token
from inscourse_backend.utils.image_generator import generate_icon, fetch_user_avatar_schema
from inscourse_backend.utils.request_processor import fetch_parameter_dict
from inscourse_backend.utils.rpc import do_request
from project_config import PROJECT_ROOT


@acquire_token
def get_my_info(request):
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    return HttpResponse(json.dumps({
        'user': user.to_dict()
    }))


@acquire_token
def change_user_info(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    try:
        username = parameter_dict['username']
        workspace = parameter_dict['workspace']
        email = parameter_dict['email']
    except KeyError:
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    user.username = username
    user.workspace = workspace
    user.email = email
    user.save()
    return HttpResponse(json.dumps({
        'message': u'修改成功'
    }))


def admin_login(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    try:
        openid = parameter_dict['openid']
        username = parameter_dict['username']
    except KeyError:
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)
    try:
        user = User.objects.get(openid=openid)
        new_token, new_expire_time = update_token(user)
        return HttpResponse(json.dumps({
            'new_user': 0,
            'message': u'登陆成功',
            'data': user.to_dict(),
            'token': new_token,
            'expire_time': new_expire_time
        }))
    except User.DoesNotExist:
        new_user = User(openid=openid, username=username)
        new_user.save()
        new_token, new_expire_time = update_token(new_user)
        return HttpResponse(json.dumps({
            'new_user': 1,
            'message': u'登陆成功',
            'data': new_user.to_dict(),
            'token': new_token,
            'expire_time': new_expire_time
        }))


def login(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    try:
        code = parameter_dict['code']
        username = parameter_dict['username']
        avatar_url = parameter_dict['avatar_url']
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
            'new_user': 0,
            'message': u'登陆成功',
            'data': user.to_dict(),
            'token': new_token,
            'expire_time': new_expire_time
        }))
    except User.DoesNotExist:
        new_user = User(openid=openid, username=username)
        new_user.save()

        background_color, font_color = fetch_user_avatar_schema(new_user.user_id)

        response = requests.request('GET', avatar_url)
        print(response)
        if response.status_code == 200:
            with open(PROJECT_ROOT + '/inscourse_backend/assets/avatar/user_avatar_' + str(
                              new_user.user_id) + '.png', 'wb') as f:
                f.write(response.content)
        else:
            generate_icon(new_user.username[:2], 'zh', background_color, font_color,
                          PROJECT_ROOT + '/inscourse_backend/assets/avatar/user_avatar_' + str(
                              new_user.user_id) + '.png')
        new_token, new_expire_time = update_token(new_user)
        return HttpResponse(json.dumps({
            'new_user': 1,
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
    # print('status_code: [%d] and response: %s' % (status_code, response_dict))
    if status_code == 200:
        return response_dict['openid']
    return None


def get_user_avatar(request):
    parameter_dict = fetch_parameter_dict(request, 'GET')
    try:
        user = User.objects.get(user_id=int(parameter_dict['user_id']))
    except (KeyError, ValueError, User.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    with open(PROJECT_ROOT + '/inscourse_backend/assets/avatar/user_avatar_' + str(user.user_id) + '.png', 'rb') as img:
        return HttpResponse(img.read(), content_type='image/png')

    return HttpResponseNotFound()
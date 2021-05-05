from inscourse_tests.rpc_utils import *


def sys_admin_login(openid: str, username: str, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('sys/adminLogin', data={'openid': openid, 'username': username})
    return do_post_request('sys/adminLogin', data={'openid': openid, 'username': username})


def sys_change_username(token: str, new_name: str, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('sys/changeUsername', headers={TOKEN_HEADER_KEY: token}, data={'newName': new_name})
    return do_post_request('sys/changeUsername', headers={TOKEN_HEADER_KEY: token}, data={'newName': new_name})


def sys_get_my_info(token: str, is_rpc=True):
    if is_rpc:
        return do_rpc_get_request('sys/getMyInfo', headers={TOKEN_HEADER_KEY: token})
    return do_rpc_get_request('sys/getMyInfo', headers={TOKEN_HEADER_KEY: token})

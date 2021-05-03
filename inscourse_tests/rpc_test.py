from inscourse_tests.rpc_utils import *


def sys_admin_login(openid: str, username: str, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('sys/adminLogin', data={'openid': openid, 'username': username})
    return do_post_request('sys/adminLogin', data={'openid': openid, 'username': username})


def sys_change_username(token: str, new_name: str, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('sys/changeUsername', headers={TOKEN_HEADER_KEY: token}, data={'newName': new_name})
    return do_post_request('sys/changeUsername', headers={TOKEN_HEADER_KEY: token}, data={'newName': new_name})


# 数据库初始化脚本
if __name__ == '__main__':
    status_code, response_dict = sys_admin_login('test-id-001', 'test-user1')
    show_info(status_code, response_dict)
    user1_token = response_dict['token']

    status_code, response_dict = sys_admin_login('test-id-002', 'test-user2')
    show_info(status_code, response_dict)
    user2_token = response_dict['token']

    status_code, response_dict = sys_change_username(user1_token, 'test-user2-new-name')
    show_info(status_code, response_dict)

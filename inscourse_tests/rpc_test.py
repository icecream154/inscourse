from inscourse_backend.services.sys.token import TOKEN_HEADER_KEY
from inscourse_tests.rpc_utils import do_post_request, do_get_request


def sys_admin_login(openid: str, username: str):
    return do_post_request('sys/admin_login', data={'openid': openid, 'username': username})


def show_info(status_code: int, response_dict: dict):
    print('status_code[%d] and response: [%s]' % (status_code, response_dict))


# 数据库初始化脚本
if __name__ == '__main__':
    status_code, response_dict = sys_admin_login('test-id-001', 'test-user1')
    show_info(status_code, response_dict)
    status_code, response_dict = sys_admin_login('test-id-001', 'test-user2')
    show_info(status_code, response_dict)

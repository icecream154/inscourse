from inscourse_tests.rpc_utils import *


def sys_admin_login(openid: str, username: str, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('sys/adminLogin', data={'openid': openid, 'username': username})
    return do_post_request('sys/adminLogin', data={'openid': openid, 'username': username})


def sys_change_username(token: str, new_name: str, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('sys/changeUsername', headers={TOKEN_HEADER_KEY: token}, data={'newName': new_name})
    return do_post_request('sys/changeUsername', headers={TOKEN_HEADER_KEY: token}, data={'newName': new_name})


def course_upload(token: str, name: str, description: str, category: int, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('course/uploadCourse', headers={TOKEN_HEADER_KEY: token}, data={
            'name': name,
            'description': description,
            'category': category
        })
    return do_post_request('course/uploadCourse', headers={TOKEN_HEADER_KEY: token}, data={
        'name': name,
        'description': description,
        'category': category
    })


def course_publish(token: str, course_id: int, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('course/publish', headers={TOKEN_HEADER_KEY: token}, data={
            'course_id': course_id
        })
    return do_rpc_post_request('course/publish', headers={TOKEN_HEADER_KEY: token}, data={
        'course_id': course_id
    })


def course_query_my_course(token: str, is_rpc=True):
    if is_rpc:
        return do_rpc_get_request('course/queryMyCourse', headers={TOKEN_HEADER_KEY: token})
    return do_rpc_get_request('course/queryMyCourse', headers={TOKEN_HEADER_KEY: token})


def course_query_open_courses(name: str, category: int, order_by: str, page_size: int, page_num: int, is_rpc=True):
    if is_rpc:
        return do_rpc_get_request('course/queryOpenCourses', params={
            'name': name,
            'category': category,
            'order_by': order_by,
            'page_size': page_size,
            'page_num': page_num
        })
    return do_rpc_get_request('course/queryOpenCourses', params={
        'name': name,
        'category': category,
        'order_by': order_by,
        'page_size': page_size,
        'page_num': page_num
    })


# 数据库初始化脚本
if __name__ == '__main__':
    status_code, response_dict = sys_admin_login('test-id-001', 'test-user1')
    show_info(status_code, response_dict)
    # user 1
    user1_token = response_dict['token']

    status_code, response_dict = sys_admin_login('test-id-002', 'test-user2')
    show_info(status_code, response_dict)
    # user 2
    user2_token = response_dict['token']

    status_code, response_dict = sys_change_username(user2_token, 'test-user2-new-name')
    show_info(status_code, response_dict)

    status_code, response_dict = course_upload(user1_token, 'Java Programming', 'This is a course that teaches you how'
                                                                                'to write programs in java.', 1)
    show_info(status_code, response_dict)
    # course 1: Java
    java_course_id = response_dict['course_id']

    status_code, response_dict = course_upload(user2_token, 'C Programming', 'You may want to learn C here.', 1)
    show_info(status_code, response_dict)
    # course 2: C
    c_course_id = response_dict['course_id']

    # 公开失败，不是课程的创建者
    status_code, response_dict = course_publish(user2_token, java_course_id)
    show_info(status_code, response_dict)

    # 公开成功
    status_code, response_dict = course_publish(user2_token, c_course_id)
    show_info(status_code, response_dict)

    # 公开失败，已经公开过了
    status_code, response_dict = course_publish(user2_token, c_course_id)
    show_info(status_code, response_dict)

    # 公开成功
    status_code, response_dict = course_publish(user1_token, java_course_id)
    show_info(status_code, response_dict)

    # course 3: C++
    status_code, response_dict = course_upload(user2_token, 'C++ Programming', 'C++ is just dark magic.', 1)
    show_info(status_code, response_dict)

    # 目前 user1 有一个java课程，已公开， user2 有两个课程, c 公开了， c++ 未公开

    # user 1 查询
    status_code, response_dict = course_query_my_course(user1_token)
    show_info(status_code, response_dict)

    # user 2 查询
    status_code, response_dict = course_query_my_course(user2_token)
    show_info(status_code, response_dict)

    # 查公开课程，应查到两个
    status_code, response_dict = course_query_open_courses('', 1, 'default', 5, 1)
    show_info(status_code, response_dict)


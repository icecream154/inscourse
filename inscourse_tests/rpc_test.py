from inscourse_tests.api_requests.sys_requests import *
from inscourse_tests.api_requests.course_requests import *
from inscourse_tests.api_requests.resource_requests import *

from inscourse_tests.rpc_utils import *

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
    c_plus_plus_course_id = response_dict['course_id']

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

    # user 1 上传 java 资源
    status_code, response_dict = resource_release(user1_token, java_course_id, 'textbook',
                                                  'This is the classic textbook for java programming.', 1,
                                                  'https://fakegoturl.cn')
    show_info(status_code, response_dict)
    java_resource1_id = response_dict['resource_id']

    # user 2 上传 java 资源
    status_code, response_dict = resource_release(user2_token, java_course_id, 'notes',
                                                  'This is my notes when learning java.', 2,
                                                  'You\'d better learn java from the very beginning to have a better'
                                                  'understanding of object oriented programming')
    show_info(status_code, response_dict)
    java_resource2_id = response_dict['resource_id']

    # 查询 java 课的资源
    status_code, response_dict = resource_query_by_course(user1_token, java_course_id)
    show_info(status_code, response_dict)

    # user 1 修改资源 1，修改成功
    status_code, response_dict = resource_modify(user1_token, java_resource1_id, 'textbook',
                                                 'This is the classic textbook for java programming.', 1,
                                                 'https://another.fakegoturl.cn')
    show_info(status_code, response_dict)

    # user 2 修改资源 1，修改失败
    status_code, response_dict = resource_modify(user2_token, java_resource1_id, 'textbook',
                                                 'Useless description', 1,
                                                 'https://another2.fakegoturl.cn')
    show_info(status_code, response_dict)

    # user 2 删除资源 2，删除失败
    status_code, response_dict = resource_delete(user2_token, java_resource2_id)
    show_info(status_code, response_dict)

    # 查询 java 课的资源，只剩下修改过的资源 1
    status_code, response_dict = resource_query_by_course(user1_token, java_course_id)
    show_info(status_code, response_dict)

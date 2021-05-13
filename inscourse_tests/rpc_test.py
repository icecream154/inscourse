from inscourse_tests.api_requests.sys_requests import *
from inscourse_tests.api_requests.course_requests import *
from inscourse_tests.api_requests.resource_requests import *
from inscourse_tests.api_requests.mate_requests import *
from inscourse_tests.api_requests.assignment_requests import *
from inscourse_tests.rpc_utils import *

# 数据库初始化脚本
if __name__ == '__main__':
    # 系统模块测试
    # ---------------------------------------------------------
    show_separate_line()
    status_code, response_dict = sys_admin_login('test-uid-001', 'test-user1')
    show_info(1, status_code, response_dict)
    # user 1
    user1_token = response_dict['token']
    status_code, response_dict = sys_get_my_info(user1_token)
    show_info(2, status_code, response_dict)
    user1_user_id = response_dict['user']['user_id']

    status_code, response_dict = sys_admin_login('test-uid-002', 'test-user2')
    show_info(3, status_code, response_dict)
    # user 2
    user2_token = response_dict['token']
    status_code, response_dict = sys_get_my_info(user2_token)
    show_info(4, status_code, response_dict)
    user2_user_id = response_dict['user']['user_id']

    status_code, response_dict = sys_change_username(user2_token, 'test-user2-new-name')
    show_info(5, status_code, response_dict)

    # 课程模块测试
    # ---------------------------------------------------------
    show_separate_line()
    # course 1: Java
    status_code, response_dict = course_upload(user1_token, 'Java', 'Java', 'This is a course that teaches you how'
                                                                            'to write programs in java.', 1)
    show_info(1, status_code, response_dict)
    java_course_id = response_dict['course_id']

    # course 2: C
    status_code, response_dict = course_upload(user2_token, 'C', 'C', 'You may want to learn C here.', 1)
    show_info(2, status_code, response_dict)
    c_course_id = response_dict['course_id']

    # 公开失败，不是课程的创建者
    status_code, response_dict = course_publish(user2_token, java_course_id)
    show_info(3, status_code, response_dict)

    # 公开成功
    status_code, response_dict = course_publish(user2_token, c_course_id)
    show_info(4, status_code, response_dict)

    # 公开失败，已经公开过了
    status_code, response_dict = course_publish(user2_token, c_course_id)
    show_info(5, status_code, response_dict)

    # 公开成功
    status_code, response_dict = course_publish(user1_token, java_course_id)
    show_info(6, status_code, response_dict)

    # course 3: C++
    status_code, response_dict = course_upload(user2_token, 'C++ Programming', 'C++', 'C++ is just dark magic.', 1)
    show_info(7, status_code, response_dict)
    c_plus_plus_course_id = response_dict['course_id']

    # course 4: Go
    status_code, response_dict = course_upload(user2_token, 'Go', 'Go',
                                               'Go is an amazing language developed by Google.', 1)
    show_info(7, status_code, response_dict)
    go_course_id = response_dict['course_id']
    status_code, response_dict = course_publish(user2_token, go_course_id)

    # course 5: Perl
    status_code, response_dict = course_upload(user2_token, 'Perl', 'Perl', 'Perl is a language often used on Linux.',
                                               1)
    show_info(7, status_code, response_dict)
    perl_course_id = response_dict['course_id']
    status_code, response_dict = course_publish(user2_token, perl_course_id)

    # course 6: Ruby
    status_code, response_dict = course_upload(user2_token, 'Ruby', 'Ruby', 'Ruby is a language often used on Linux.',
                                               1)
    show_info(7, status_code, response_dict)
    ruby_course_id = response_dict['course_id']
    status_code, response_dict = course_publish(user2_token, ruby_course_id)

    # 目前 user1 有一个java课程，已公开， user2 有两个课程, c 公开了， c++ 未公开

    # 查询指定的课程
    status_code, response_dict = course_query_certain_course(user1_token, java_course_id)
    show_info(8, status_code, response_dict)
    java_course_invitation_code = response_dict['course']['invitation_code']

    status_code, response_dict = course_query_certain_course(user1_token, c_course_id)
    show_info(9, status_code, response_dict)
    c_course_invitation_code = response_dict['course']['invitation_code']

    status_code, response_dict = course_query_certain_course(user2_token, c_plus_plus_course_id)
    show_info(10, status_code, response_dict)
    c_plus_plus_course_invitation_code = response_dict['course']['invitation_code']

    # user 1 查询自己加入的课程，查到自己新建的 java 课程
    status_code, response_dict = course_query_my_joined_course(user1_token)
    show_info(11, status_code, response_dict)

    # user 2 查询自己加入的课程，查到自己新建的 c, c++ 课程
    status_code, response_dict = course_query_my_joined_course(user2_token)
    show_info(12, status_code, response_dict)

    # user 1 加入 Java 课程，因为已经加入课程，加入失败
    status_code, response_dict = course_join(user1_token, java_course_invitation_code)
    show_info(13, status_code, response_dict)

    # user 1 加入 c 课程，加入成功
    status_code, response_dict = course_join(user1_token, c_course_invitation_code)
    show_info(14, status_code, response_dict)

    # 查公开课程，应查到两个
    status_code, response_dict = course_query_open_courses(user1_token, '', 1, 'default', 5, 1)
    show_info(15, status_code, response_dict)

    # 查公开课程，应查到两个
    status_code, response_dict = course_query_open_courses(user2_token, '', 1, 'default', 2, 1)
    show_info(16, status_code, response_dict)

    # 查公开课程，应查到零个
    status_code, response_dict = course_query_open_courses(user2_token, '', 1, 'default', 2, 2)
    show_info(17, status_code, response_dict)

    # user 2 加入 java 课程，加入成功
    status_code, response_dict = course_join(user2_token, java_course_invitation_code)
    show_info(18, status_code, response_dict)

    # 资源模块测试
    # ---------------------------------------------------------
    show_separate_line()
    # user 1 现在创建了 java，加入了 java 和 c
    # user 2 现在创建了 c 和 c++, 加入了 c 和 c++

    # user 1 上传 c 资源
    status_code, response_dict = resource_release(user1_token, c_course_id, 'textbook',
                                                  'This is the classic textbook for c programming.', 0,
                                                  'https://fakegoturl.cn')
    show_info(1, status_code, response_dict)
    c_resource1_id = response_dict['resource_id']

    # user 2 上传 c 资源
    status_code, response_dict = resource_release(user2_token, c_course_id, 'notes',
                                                  'This is my notes when learning c.', 0,
                                                  'You\'d better learn c from the very beginning to have a better'
                                                  'understanding of object oriented programming')
    show_info(2, status_code, response_dict)
    c_resource2_id = response_dict['resource_id']

    # 查询 c 的资源
    status_code, response_dict = resource_query_by_course(user1_token, c_course_id)
    show_info(3, status_code, response_dict)

    # user 1 修改资源 1，修改成功
    status_code, response_dict = resource_modify(user1_token, c_resource1_id, 'textbook',
                                                 'This is the classic textbook for c programming.', 0,
                                                 'https://another.fakegoturl.cn')
    show_info(4, status_code, response_dict)

    # user 2 修改资源 1，修改失败
    status_code, response_dict = resource_modify(user2_token, c_resource1_id, 'textbook',
                                                 'Useless description', 0,
                                                 'https://another2.fakegoturl.cn')
    show_info(5, status_code, response_dict)

    # user 2 查询自己在 c 下的 resource
    status_code, response_dict = resource_query_mine_by_course(user2_token, c_course_id)
    show_info(6, status_code, response_dict)

    # user 2 删除资源 2，删除成功
    status_code, response_dict = resource_delete(user2_token, c_resource2_id)
    show_info(7, status_code, response_dict)

    # user 2 查询自己在 c 下的 resource，无记录
    status_code, response_dict = resource_query_mine_by_course(user2_token, c_course_id)
    show_info(8, status_code, response_dict)

    # 查询 c 的资源，只剩下修改过的资源 1
    status_code, response_dict = resource_query_by_course(user1_token, c_course_id)
    show_info(9, status_code, response_dict)

    # user 1 给资源 1 取消点赞和取消收藏，均失败，因为还未点赞和收藏
    status_code, response_dict = resource_cancel_fav(user1_token, c_resource1_id)
    show_info(10, status_code, response_dict)

    status_code, response_dict = resource_cancel_prefer(user1_token, c_resource1_id)
    show_info(11, status_code, response_dict)

    # user 1 给资源 1 点赞和收藏，成功
    status_code, response_dict = resource_fav(user1_token, c_resource1_id)
    show_info(12, status_code, response_dict)

    status_code, response_dict = resource_prefer(user1_token, c_resource1_id)
    show_info(13, status_code, response_dict)

    # user 1 查询 c 的资源，只剩下修改过的资源 1, 点赞和收藏字段为 True
    status_code, response_dict = resource_query_by_course(user1_token, c_course_id)
    show_info(14, status_code, response_dict)

    # user 2 查询 c 的资源，只剩下修改过的资源 1, 点赞和收藏字段为 False
    status_code, response_dict = resource_query_by_course(user2_token, c_course_id)
    show_info(15, status_code, response_dict)

    # user 1 上传其他 c 资源
    resource_release(user1_token, c_course_id, 'textbook 3',
                     'This is another classic textbook for c programming.', 0,
                     'https://fakegoturl.cn')
    resource_release(user1_token, c_course_id, 'textbook 4',
                     'This is another classic textbook for c programming.', 0,
                     'https://fakegoturl.cn')
    resource_release(user1_token, c_course_id, 'video 1',
                     'There are classic videos for c programming.', 1,
                     'https://fakecvideos.cn')

    # 课友模块测试
    # ---------------------------------------------------------
    show_separate_line()
    # user 2 查询所有课友，无课友
    status_code, response_dict = mate_query_all(user2_token)
    show_info(1, status_code, response_dict)

    # user 2 发送 c 课程邀请
    status_code, response_dict = mate_invite(user2_token, c_course_id, '求求大佬带我学c')
    show_info(2, status_code, response_dict)
    c_mate_invitation_code = response_dict['invitation_code']

    # user 2 再次发送 c 课程邀请， 失败
    status_code, response_dict = mate_invite(user2_token, c_course_id, '求求大佬带我学c')
    show_info(3, status_code, response_dict)

    # user2 接受自己的邀请，失败
    status_code, response_dict = mate_accept_invitation(user2_token, c_mate_invitation_code)
    show_info(4, status_code, response_dict)

    # user 1 查询 c 课程下邀请
    status_code, response_dict = mate_query_course_invitations(user1_token, c_course_id)
    show_info(5, status_code, response_dict)

    # user 2 查询 c++ 课程下邀请, 空
    status_code, response_dict = mate_query_course_invitations(user2_token, c_plus_plus_course_id)
    show_info(6, status_code, response_dict)

    # user 1 接受 user 2 的邀请，成功
    status_code, response_dict = mate_accept_invitation(user1_token, c_mate_invitation_code)
    show_info(7, status_code, response_dict)

    # user 2 查询所有课友，课友user 1
    status_code, response_dict = mate_query_all(user2_token)
    show_info(8, status_code, response_dict)

    # user 2 查询 c 课友 ， user 1
    status_code, response_dict = mate_query_by_course(user1_token, c_course_id)
    show_info(9, status_code, response_dict)
    c_mate_id = response_dict['mate']['mate_id']

    # user 2 查询 c++ 课友， 无
    status_code, response_dict = mate_query_by_course(user2_token, c_plus_plus_course_id)
    show_info(10, status_code, response_dict)

    # user 2 发送 c++ 课程邀请
    status_code, response_dict = mate_invite(user2_token, c_plus_plus_course_id, '求求大佬带我学 c++')
    show_info(11, status_code, response_dict)
    c_plus_plus_course_invitation_id = response_dict['invitation_id']

    # user 1 取消 c++ 课程邀请，失败
    status_code, response_dict = mate_cancel_invitation(user1_token, c_plus_plus_course_invitation_id)
    show_info(12, status_code, response_dict)

    # user 2 取消 c++ 课程邀请，成功
    status_code, response_dict = mate_cancel_invitation(user2_token, c_plus_plus_course_invitation_id)
    show_info(13, status_code, response_dict)

    # user 2 发送 java 课程邀请
    status_code, response_dict = mate_invite(user2_token, java_course_id, '求求大佬带我学 java')
    show_info(14, status_code, response_dict)
    java_mate_invitation_code = response_dict['invitation_code']

    # user 1 接受 user 2 的邀请，成功
    status_code, response_dict = mate_accept_invitation(user1_token, java_mate_invitation_code)
    show_info(15, status_code, response_dict)

    # user 2 查询 java 课友 ， user 1
    status_code, response_dict = mate_query_by_course(user1_token, java_course_id)
    show_info(16, status_code, response_dict)
    java_mate_id = response_dict['mate']['mate_id']

    # user 2 解除 java 课友关系，成功
    status_code, response_dict = mate_unbind(user2_token, java_mate_id)
    show_info(17, status_code, response_dict)

    # 日程模块测试
    # ---------------------------------------------------------
    show_separate_line()

    # user2 新建 Chapter 1 日程
    status_code, response_dict = assignment_new(user2_token, c_mate_id, 'Chapter 1', '2021-05-10')
    show_info(1, status_code, response_dict)
    c_chapter1_schedule_id = response_dict['assignment_id']

    # user1 新建 Chapter 2 日程
    status_code, response_dict = assignment_new(user1_token, c_mate_id, 'Chapter 2', '2021-05-12')
    show_info(2, status_code, response_dict)
    c_chapter2_schedule_id = response_dict['assignment_id']

    # user1 查询日程
    status_code, response_dict = assignment_query_by_mate(user1_token, c_mate_id)
    show_info(3, status_code, response_dict)

    # user1 修改 Chapter 1 日程
    status_code, response_dict = assignment_modify(user1_token, c_chapter1_schedule_id, 'New Chapter 1',
                                                   '2021-05-11')
    show_info(4, status_code, response_dict)

    # user2 修改 Chapter 2 日程
    status_code, response_dict = assignment_modify(user2_token, c_chapter2_schedule_id, 'New Chapter 2',
                                                   '2021-05-13')
    show_info(5, status_code, response_dict)

    # user2 查询日程
    status_code, response_dict = assignment_query_by_mate(user2_token, c_mate_id)
    show_info(6, status_code, response_dict)

    # user2 删除 Chapter 2 日程
    status_code, response_dict = assignment_delete(user2_token, c_chapter2_schedule_id)
    show_info(7, status_code, response_dict)

    # user1 查询日程
    status_code, response_dict = assignment_query_by_mate(user1_token, c_mate_id)
    show_info(8, status_code, response_dict)

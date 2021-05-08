from inscourse_tests.rpc_utils import *


def course_query_certain_course(token: str, course_id: int, is_rpc=True):
    if is_rpc:
        return do_rpc_get_request('course/queryCertainCourse', headers={TOKEN_HEADER_KEY: token},
                                  params={'course_id': course_id})
    return do_get_request('course/queryCertainCourse', headers={TOKEN_HEADER_KEY: token},
                          params={'course_id': course_id})


def course_query_open_courses(token: str, name: str, category: int, order_by: str,
                              page_size: int, page_num: int, is_rpc=True):
    if is_rpc:
        return do_rpc_get_request('course/queryOpenCourses', headers={TOKEN_HEADER_KEY: token}, params={
            'name': name,
            'category': category,
            'order_by': order_by,
            'page_size': page_size,
            'page_num': page_num
        })
    return do_get_request('course/queryOpenCourses', headers={TOKEN_HEADER_KEY: token}, params={
        'name': name,
        'category': category,
        'order_by': order_by,
        'page_size': page_size,
        'page_num': page_num
    })


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


def course_query_my_joined_course(token: str, is_rpc=True):
    if is_rpc:
        return do_rpc_get_request('course/queryMyJoinedCourse', headers={TOKEN_HEADER_KEY: token})
    return do_get_request('course/queryMyJoinedCourse', headers={TOKEN_HEADER_KEY: token})


def course_join(token: str, invitation_code: int, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('course/joinCourse', headers={TOKEN_HEADER_KEY: token}, data={
            'invitation_code': invitation_code
        })
    return do_post_request('course/joinCourse', headers={TOKEN_HEADER_KEY: token}, data={
        'invitation_code': invitation_code
    })


def course_drop_out(token: str, course_id: int, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('course/dropOutCourse', headers={TOKEN_HEADER_KEY: token}, data={
            'course_id': course_id
        })
    return do_post_request('course/dropOutCourse', headers={TOKEN_HEADER_KEY: token}, data={
        'course_id': course_id
    })

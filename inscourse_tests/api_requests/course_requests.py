from inscourse_tests.rpc_utils import *


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
from inscourse_tests.rpc_utils import *


def resource_release(token: str, course_id: int, resource_key: str,
                     description: str, content_type: int, content: str, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('resource/releaseResource', headers={TOKEN_HEADER_KEY: token}, data={
            'course_id': course_id,
            'resource_key': resource_key,
            'description': description,
            'content_type': content_type,
            'content': content
        })
    return do_post_request('resource/releaseResource', headers={TOKEN_HEADER_KEY: token}, data={
        'course_id': course_id,
        'resource_key': resource_key,
        'description': description,
        'content_type': content_type,
        'content': content
    })


def resource_query_by_course(token: str, course_id: int, is_rpc=True):
    if is_rpc:
        return do_rpc_get_request('resource/queryResourceByCourse', headers={TOKEN_HEADER_KEY: token}, params={
            'course_id': course_id
        })
    return do_get_request('resource/queryResourceByCourse', headers={TOKEN_HEADER_KEY: token}, params={
        'course_id': course_id
    })


def resource_modify(token: str, resource_id: int, resource_key: str,
                    description: str, content_type: int, content: str, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('resource/modifyResource', headers={TOKEN_HEADER_KEY: token}, data={
            'resource_id': resource_id,
            'resource_key': resource_key,
            'description': description,
            'content_type': content_type,
            'content': content
        })
    return do_post_request('resource/modifyResource', headers={TOKEN_HEADER_KEY: token}, data={
        'resource_id': resource_id,
        'resource_key': resource_key,
        'description': description,
        'content_type': content_type,
        'content': content
    })


def resource_delete(token: str, resource_id: int, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('resource/deleteResource', headers={TOKEN_HEADER_KEY: token}, data={
            'resource_id': resource_id
        })
    return do_post_request('resource/deleteResource', headers={TOKEN_HEADER_KEY: token}, data={
        'resource_id': resource_id
    })


def resource_query_mine_by_course(token: str, course_id: int, is_rpc=True):
    if is_rpc:
        return do_rpc_get_request('resource/queryMyResourceByCourse', headers={TOKEN_HEADER_KEY: token}, data={
            'course_id': course_id
        })
    return do_get_request('resource/queryMyResourceByCourse', headers={TOKEN_HEADER_KEY: token}, data={
        'course_id': course_id
    })

#     path('resource/resourceFav', resource_fav, name='resource_fav'),
#     path('resource/cancelResourceFav', cancel_resource_fav, name='cancel_resource_fav'),
#     path('resource/resourcePrefer', resource_prefer, name='resource_prefer'),
#     path('resource/cancelResourcePrefer', cancel_resource_prefer, name='cancel_resource_prefer'),
#     path('resource/queryFavoredResources', query_favored_resource, name='query_favored_resource'),
#     path('resource/queryCertainResource', query_certain_resource, name='query_certain_resource'),


def resource_fav(token: str, resource_id: int, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('resource/resourceFav', headers={TOKEN_HEADER_KEY: token}, data={
            'resource_id': resource_id
        })
    return do_post_request('resource/resourceFav', headers={TOKEN_HEADER_KEY: token}, data={
        'resource_id': resource_id
    })


def resource_cancel_fav(token: str, resource_id: int, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('resource/cancelResourceFav', headers={TOKEN_HEADER_KEY: token}, data={
            'resource_id': resource_id
        })
    return do_post_request('resource/cancelResourceFav', headers={TOKEN_HEADER_KEY: token}, data={
        'resource_id': resource_id
    })


def resource_prefer(token: str, resource_id: int, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('resource/resourcePrefer', headers={TOKEN_HEADER_KEY: token}, data={
            'resource_id': resource_id
        })
    return do_post_request('resource/resourcePrefer', headers={TOKEN_HEADER_KEY: token}, data={
        'resource_id': resource_id
    })


def resource_cancel_prefer(token: str, resource_id: int, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('resource/cancelResourcePrefer', headers={TOKEN_HEADER_KEY: token}, data={
            'resource_id': resource_id
        })
    return do_post_request('resource/cancelResourcePrefer', headers={TOKEN_HEADER_KEY: token}, data={
        'resource_id': resource_id
    })


def resource_query_favored(token: str, course_id: int, is_rpc=True):
    if is_rpc:
        return do_rpc_get_request('resource/queryFavoredResources', headers={TOKEN_HEADER_KEY: token}, data={
            'course_id': course_id
        })
    return do_get_request('resource/queryFavoredResources', headers={TOKEN_HEADER_KEY: token}, data={
        'course_id': course_id
    })


def resource_query_certain(token: str, resource_id: int, is_rpc=True):
    if is_rpc:
        return do_rpc_get_request('resource/queryCertainResource', headers={TOKEN_HEADER_KEY: token}, data={
            'resource_id': resource_id
        })
    return do_get_request('resource/queryCertainResource', headers={TOKEN_HEADER_KEY: token}, data={
        'resource_id': resource_id
    })

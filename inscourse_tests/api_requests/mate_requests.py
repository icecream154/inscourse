from inscourse_tests.rpc_utils import *


def mate_query_all(token: str, is_rpc=True):
    if is_rpc:
        return do_rpc_get_request('mate/queryMyMates', headers={TOKEN_HEADER_KEY: token})
    return do_get_request('mate/queryMyMates', headers={TOKEN_HEADER_KEY: token})


def mate_query_by_course(token: str, course_id: int, is_rpc=True):
    if is_rpc:
        return do_rpc_get_request('mate/queryMyMateByCourse', headers={TOKEN_HEADER_KEY: token}, params={
            'course_id': course_id
        })
    return do_get_request('mate/queryMyMateByCourse', headers={TOKEN_HEADER_KEY: token}, params={
        'course_id': course_id
    })


def mate_query_course_invitations(token: str, course_id: int, is_rpc=True):
    if is_rpc:
        return do_rpc_get_request('mate/queryCourseMateInvitations', headers={TOKEN_HEADER_KEY: token}, params={
            'course_id': course_id
        })
    return do_get_request('mate/queryCourseMateInvitations', headers={TOKEN_HEADER_KEY: token}, params={
        'course_id': course_id
    })


def mate_invite(token: str, course_id: int, description: str, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('mate/inviteMate', headers={TOKEN_HEADER_KEY: token}, data={
            'course_id': course_id,
            'description': description
        })
    return do_post_request('mate/inviteMate', headers={TOKEN_HEADER_KEY: token}, data={
        'course_id': course_id,
        'description': description
    })


def mate_accept_invitation(token: str, invitation_code: str, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('mate/acceptMateInvitation', headers={TOKEN_HEADER_KEY: token}, data={
            'invitation_code': invitation_code
        })
    return do_post_request('mate/acceptMateInvitation', headers={TOKEN_HEADER_KEY: token}, data={
        'invitation_code': invitation_code
    })


def mate_cancel_invitation(token: str, invitation_id: int, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('mate/cancelMateInvitation', headers={TOKEN_HEADER_KEY: token}, data={
            'invitation_id': invitation_id
        })
    return do_post_request('mate/cancelMateInvitation', headers={TOKEN_HEADER_KEY: token}, data={
        'invitation_id': invitation_id
    })


def mate_unbind(token: str, mate_id: int, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('mate/unbind', headers={TOKEN_HEADER_KEY: token}, data={
            'mate_id': mate_id
        })
    return do_post_request('mate/unbind', headers={TOKEN_HEADER_KEY: token}, data={
        'mate_id': mate_id
    })

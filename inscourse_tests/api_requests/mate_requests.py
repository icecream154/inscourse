from inscourse_tests.rpc_utils import *


def mate_query_all(token: str, is_rpc=True):
    if is_rpc:
        return do_rpc_get_request('mate/queryMyMates', headers={TOKEN_HEADER_KEY: token})
    return do_get_request('mate/queryMyMates', headers={TOKEN_HEADER_KEY: token})


def mate_query_by_course(token: str, course_id: int, is_rpc=True):
    if is_rpc:
        return do_rpc_get_request('mate/queryMyMatesByCourse', headers={TOKEN_HEADER_KEY: token}, params={
            'course_id': course_id
        })
    return do_get_request('mate/queryMyMatesByCourse', headers={TOKEN_HEADER_KEY: token}, params={
        'course_id': course_id
    })


def mate_invite(token: str, course_id: int, accept_id: int, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('mate/inviteMate', headers={TOKEN_HEADER_KEY: token}, data={
            'course_id': course_id,
            'accept_id': accept_id
        })
    return do_post_request('mate/inviteMate', headers={TOKEN_HEADER_KEY: token}, data={
        'course_id': course_id,
        'accept_id': accept_id
    })


def mate_deal_invitation(token: str, invitation_id: int, status: int, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('mate/dealMateInvitation', headers={TOKEN_HEADER_KEY: token}, data={
            'invitation_id': invitation_id,
            'status': status
        })
    return do_post_request('mate/dealMateInvitation', headers={TOKEN_HEADER_KEY: token}, data={
        'invitation_id': invitation_id,
        'status': status
    })


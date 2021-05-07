from inscourse_tests.rpc_utils import *


def assignment_query_by_mate(token: str, mate_id: int, is_rpc=True):
    if is_rpc:
        return do_rpc_get_request('assignment/queryMyAssignmentsByMate', headers={TOKEN_HEADER_KEY: token},
                                  params={'mate_id': mate_id})
    return do_get_request('assignment/queryMyAssignmentsByMate', headers={TOKEN_HEADER_KEY: token},
                          params={'mate_id': mate_id})


def assignment_new(token: str, mate_id: int, content: str, assignment_date: str, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('assignment/newAssignment', headers={TOKEN_HEADER_KEY: token},
                                   data={
                                       'mate_id': mate_id,
                                       'content': content,
                                       'assignment_date': assignment_date
                                   })
    return do_post_request('assignment/newAssignment', headers={TOKEN_HEADER_KEY: token},
                           data={
                               'mate_id': mate_id,
                               'content': content,
                               'assignment_date': assignment_date
                           })


def assignment_modify(token: str, assignment_id: int, content: str, assignment_date: str, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('assignment/modifyAssignment', headers={TOKEN_HEADER_KEY: token},
                                   data={
                                       'assignment_id': assignment_id,
                                       'content': content,
                                       'assignment_date': assignment_date
                                   })
    return do_post_request('assignment/modifyAssignment', headers={TOKEN_HEADER_KEY: token},
                           data={
                               'assignment_id': assignment_id,
                               'content': content,
                               'assignment_date': assignment_date
                           })


def assignment_delete(token: str, assignment_id: int, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('assignment/deleteAssignment', headers={TOKEN_HEADER_KEY: token},
                                   data={'assignment_id': assignment_id})
    return do_post_request('assignment/deleteAssignment', headers={TOKEN_HEADER_KEY: token},
                           data={'assignment_id': assignment_id})

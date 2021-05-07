from inscourse_tests.rpc_utils import *


def schedule_query_by_mate(token: str, mate_id: int, is_rpc=True):
    if is_rpc:
        return do_rpc_get_request('assignment/queryMySchedulesByMate', headers={TOKEN_HEADER_KEY: token},
                                  params={'mate_id': mate_id})
    return do_get_request('assignment/queryMySchedulesByMate', headers={TOKEN_HEADER_KEY: token},
                          params={'mate_id': mate_id})


def schedule_new(token: str, mate_id: int, content: str, schedule_date: str, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('assignment/newSchedule', headers={TOKEN_HEADER_KEY: token},
                                   data={
                                       'mate_id': mate_id,
                                       'content': content,
                                       'schedule_date': schedule_date
                                   })
    return do_post_request('assignment/newSchedule', headers={TOKEN_HEADER_KEY: token},
                           data={
                               'mate_id': mate_id,
                               'content': content,
                               'schedule_date': schedule_date
                           })


def schedule_modify(token: str, schedule_id: int, content: str, schedule_date: str, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('assignment/modifySchedule', headers={TOKEN_HEADER_KEY: token},
                                   data={
                                       'assignment_id': schedule_id,
                                       'content': content,
                                       'schedule_date': schedule_date
                                   })
    return do_post_request('assignment/modifySchedule', headers={TOKEN_HEADER_KEY: token},
                           data={
                               'assignment_id': schedule_id,
                               'content': content,
                               'schedule_date': schedule_date
                           })


def schedule_delete(token: str, schedule_id: int, is_rpc=True):
    if is_rpc:
        return do_rpc_post_request('assignment/deleteSchedule', headers={TOKEN_HEADER_KEY: token},
                                   data={'assignment_id': schedule_id})
    return do_post_request('assignment/deleteSchedule', headers={TOKEN_HEADER_KEY: token},
                           data={'assignment_id': schedule_id})

import json
from datetime import datetime
from django.http import *

from inscourse_backend.models.mate.mate import Mate
from inscourse_backend.models.mate.mate_assignment import MateAssignment
from inscourse_backend.services.constants import EM_INVALID_OR_MISSING_PARAMETERS, DATE_FORMAT
from inscourse_backend.services.sys.token import fetch_user_by_token, TOKEN_HEADER_KEY
from inscourse_backend.services.token_filter import acquire_token
from inscourse_backend.utils.request_processor import fetch_parameter_dict


@acquire_token
def query_my_assignments_by_mate(request):
    parameter_dict = fetch_parameter_dict(request, 'GET')

    try:
        mate_id = int(parameter_dict['mate_id'])
        mate = Mate.objects.get(mate_id=mate_id)
    except(KeyError, TypeError, Mate.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    if mate.requester != user and mate.acceptor != user:
        return HttpResponseBadRequest(json.dumps({
            'message': u'无权查看'
        }))

    assignments = mate.mateassignment_set.all()
    assignment_list = []
    for assignment in assignments:
        assignment_list.append(assignment.to_detail_dict(user))
    return HttpResponse(json.dumps({
        'assignments': assignment_list
    }))


@acquire_token
def new_assignment(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')

    # 检查参数
    try:
        mate_id = int(parameter_dict['mate_id'])
        mate = Mate.objects.get(mate_id=mate_id)
        content = parameter_dict['content']
        assignment_date = datetime.strptime(parameter_dict['assignment_date'], DATE_FORMAT).date()
    except(KeyError, ValueError, TypeError, Mate.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    # 核对 mate
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    if mate.requester.user_id != user.user_id and mate.acceptor.user_id != user.user_id:
        return HttpResponseForbidden(json.dumps({
            'message': u'无权创建打卡计划'
        }))

    # 新建日程
    assignment = MateAssignment(
        mate=mate,
        content=content,
        assignment_date=assignment_date
    )
    assignment.save()

    return HttpResponse(json.dumps({
        'message': u'新建打卡成功',
        'assignment_id': assignment.assignment_id
    }))


@acquire_token
def modify_assignment(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')

    # 检查参数
    try:
        assignment_id = int(parameter_dict['assignment_id'])
        assignment = MateAssignment.objects.get(assignment_id=assignment_id)
        content = parameter_dict['content']
        assignment_date = datetime.strptime(parameter_dict['assignment_date'], DATE_FORMAT).date()
    except(KeyError, ValueError, TypeError, MateAssignment.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    # 核对schedule mate
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    if assignment.status != 0:
        return HttpResponseForbidden(json.dumps({
            'message': u'打卡进行中，无法修改'
        }))
    if assignment.mate.requester.user_id != user.user_id and assignment.mate.acceptor.user_id != user.user_id:
        return HttpResponseForbidden(json.dumps({
            'message': u'无权修改'
        }))

    # 修改schedule
    assignment.assignment_date = assignment_date
    assignment.content = content
    assignment.save()
    return HttpResponse(json.dumps({
        'message': u'修改打卡计划成功'
    }))


@acquire_token
def delete_assignment(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')

    # 检查参数
    try:
        assignment_id = int(parameter_dict['assignment_id'])
        assignment = MateAssignment.objects.get(assignment_id=assignment_id)
    except(KeyError, TypeError, MateAssignment.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    # 核对assignment mate
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    if assignment.mate.requester.user_id != user.user_id and assignment.mate.acceptor.user_id != user.user_id:
        return HttpResponseForbidden(json.dumps({
            'message': u'无权删除'
        }))

    # 删除assignment
    assignment.delete()
    return HttpResponse(json.dumps({
        'message': u'删除日程成功'
    }))


@acquire_token
def check_assignment(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')

    # 检查参数
    try:
        assignment_id = int(parameter_dict['assignment_id'])
        assignment = MateAssignment.objects.get(assignment_id=assignment_id)
    except(KeyError, TypeError, MateAssignment.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    # 核对assignment mate
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    if assignment.mate.requester.user_id != user.user_id and assignment.mate.acceptor.user_id != user.user_id:
        return HttpResponseForbidden(json.dumps({
            'message': u'无权打卡'
        }))

    if assignment.check_status(user) != 0:
        assignment.save()
        return HttpResponse(json.dumps({
            'message': u'打卡成功'
        }))
    else:
        return HttpResponseForbidden(json.dumps({
            'message': u'你已完成打卡'
        }))

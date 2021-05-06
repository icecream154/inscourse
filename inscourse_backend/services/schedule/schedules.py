import json
from datetime import datetime
from django.http import *

from inscourse_backend.models.mate import Mate
from inscourse_backend.models.mateschedule import MateSchedule
from inscourse_backend.services.constants import EM_INVALID_OR_MISSING_PARAMETERS, DATE_FORMAT
from inscourse_backend.services.sys.token import fetch_user_by_token, TOKEN_HEADER_KEY
from inscourse_backend.services.token_filter import acquire_token
from inscourse_backend.utils.request_processor import fetch_parameter_dict


@acquire_token
def query_my_schedules_by_mate(request):
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

    schedules = mate.mateschedule_set.all()
    schedule_list = []
    for schedule in schedules:
        schedule_list.append(schedule.to_dict())
    return HttpResponse(json.dumps({
        'schedules': schedule_list
    }))


@acquire_token
def new_schedule(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')

    # 检查参数
    try:
        mate_id = int(parameter_dict['mate_id'])
        mate = Mate.objects.get(mate_id=mate_id)
        content = parameter_dict['content']
        schedule_date = datetime.strptime(parameter_dict['schedule_date'], DATE_FORMAT).date()
    except(KeyError, ValueError, TypeError, Mate.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    # 核对schedule mate
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    if mate.requester.user_id != user.user_id and mate.acceptor.user_id != user.user_id:
        return HttpResponseForbidden(json.dumps({
            'message': u'无权创建日程'
        }))

    # 新建日程
    schedule = MateSchedule(
        mate=mate,
        content=content,
        schedule_date=schedule_date
    )
    schedule.save()

    return HttpResponse(json.dumps({
        'message': u'新建日程成功',
        'schedule_id': schedule.schedule_id
    }))


@acquire_token
def modify_schedule(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')

    # 检查参数
    try:
        schedule_id = int(parameter_dict['schedule_id'])
        schedule = MateSchedule.objects.get(schedule_id=schedule_id)
        content = parameter_dict['content']
        schedule_date = datetime.strptime(parameter_dict['schedule_date'], DATE_FORMAT).date()
    except(KeyError, ValueError, TypeError, MateSchedule.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    # 核对schedule mate
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    if schedule.mate.requester.user_id != user.user_id and schedule.mate.acceptor.user_id != user.user_id:
        return HttpResponseForbidden(json.dumps({
            'message': u'无权修改'
        }))

    # 修改schedule
    schedule.schedule_date = schedule_date
    schedule.content = content
    schedule.save()
    return HttpResponse(json.dumps({
        'message': u'修改日程成功'
    }))


@acquire_token
def delete_schedule(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')

    # 检查参数
    try:
        schedule_id = int(parameter_dict['schedule_id'])
        schedule = MateSchedule.objects.get(schedule_id=schedule_id)
    except(KeyError, TypeError, MateSchedule.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    # 核对schedule mate
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    if schedule.mate.requester.user_id != user.user_id and schedule.mate.acceptor.user_id != user.user_id:
        return HttpResponseForbidden(json.dumps({
            'message': u'无权删除'
        }))

    # 删除schedule
    schedule.delete()
    return HttpResponse(json.dumps({
        'message': u'删除日程成功'
    }))

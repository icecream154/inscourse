import json
from datetime import datetime

from django.db.models import Q
from django.http import *

from inscourse_backend.models.course import Course
from inscourse_backend.models.mate import Mate
from inscourse_backend.models.mateschedule import MateSchedule
from inscourse_backend.models.resource import Resource
from inscourse_backend.services.constants import EM_INVALID_OR_MISSING_PARAMETERS
from inscourse_backend.services.sys.token import fetch_user_by_token, TOKEN_HEADER_KEY
from inscourse_backend.services.token_filter import acquire_token
from inscourse_backend.utils.request_processor import fetch_parameter_dict


@acquire_token
def query_my_schedules(request):
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    try:
        mates = Mate.objects.filter(Q(requester=user) | Q(acceptor=user))
        schedule_list = []
        for mate in mates:
            schedules = MateSchedule.objects.filter(Q(mate=mate))
            for schedule in schedules:
                schedule_list.append(schedule.to_dict())
        return HttpResponse(json.dumps({
            'schedules': schedule_list
        }))

    # TODO: 解决判断没有schedule的问题，我现在是先找mate，再遍历找mate_schedule，所以中途有一个mate没有schedule不能直接抛出异常
    except Exception:
        return HttpResponseNotFound(json.dumps({
            'message': u'当前没有日程'
        }))


@acquire_token
def query_my_schedules_by_course(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')

    # 检查参数
    try:
        course_id = int(parameter_dict['course_id'])
    except(KeyError, TypeError):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    try:
        mates = Mate.objects.filter(Q(course_id=course_id), Q(requester=user) | Q(acceptor=user))
        schedule_list = []
        for mate in mates:
            schedules = MateSchedule.objects.filter(Q(mate=mate))
            for schedule in schedules:
                schedule_list.append(schedule.to_dict())
        return HttpResponse(json.dumps({
            'schedules': schedule_list
        }))

    # TODO: 解决判断没有schedule的问题，我现在是先找mate，再遍历找mate_schedule，所以中途有一个mate没有schedule不能直接抛出异常
    except Exception:
        return HttpResponseNotFound(json.dumps({
            'message': u'当前没有日程'
        }))


@acquire_token
def new_schedule(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')

    # 检查参数
    try:
        mate_id = int(parameter_dict['mate_id'])
        date = datetime.date(parameter_dict['date'])  # TODO: 不确定这个转换
        content = parameter_dict['content']
    except(KeyError, TypeError):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    # 检查mate
    try:
        mate = Mate.objects.get(mate_id=mate_id)
    except Mate.DoesNotExist:
        return HttpResponseNotFound(json.dumps({
            'message': u'课友不存在'
        }))

    # 新建schedule
    schedule = MateSchedule(
        mate=mate,
        date=date,
        content=content,
        progress=0,
        status=0
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
        date = datetime.date(parameter_dict['date'])  # TODO: 不确定这个转换
        content = parameter_dict['content']
        progress = parameter_dict['progress']
    except(KeyError, TypeError):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    # 检查schedule
    try:
        schedule = MateSchedule.objects.get(schedule_id=schedule_id)
    except MateSchedule.DoesNotExist:
        return HttpResponseNotFound(json.dumps({
            'message': u'日程不存在'
        }))

    # 核对schedule mate
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    if schedule.mate.requester.user_id != user.user_id or schedule.mate.acceptor.user_id != user.user_id:
        return HttpResponseForbidden(json.dumps({
            'message': u'对不起，你不是日程的课友之一'
        }))

    # 修改schedule
    schedule.date = date
    schedule.content = content
    schedule.progress = progress
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
    except(KeyError, TypeError):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    # 检查schedule
    try:
        schedule = MateSchedule.objects.get(schedule_id=schedule_id)
    except MateSchedule.DoesNotExist:
        return HttpResponseNotFound(json.dumps({
            'message': u'日程不存在'
        }))

    # 核对schedule mate
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    if schedule.mate.requester.user_id != user.user_id or schedule.mate.acceptor.user_id != user.user_id:
        return HttpResponseForbidden(json.dumps({
            'message': u'对不起，你不是日程的课友之一'
        }))

    # 删除schedule
    schedule.delete()
    return HttpResponse(json.dumps({
        'message': u'删除日程成功'
    }))

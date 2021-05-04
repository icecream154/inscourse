import json
import datetime

from django.db.models import Q
from django.http import *

from inscourse_backend.models.course import Course
from inscourse_backend.models.mate import Mate
from inscourse_backend.models.mateinvitation import MateInvitation
from inscourse_backend.models.user import User
from inscourse_backend.services.constants import EM_INVALID_OR_MISSING_PARAMETERS
from inscourse_backend.services.sys.token import fetch_user_by_token, TOKEN_HEADER_KEY
from inscourse_backend.services.token_filter import acquire_token
from inscourse_backend.utils.request_processor import fetch_parameter_dict


@acquire_token
def query_my_mates(request):
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    try:
        mates = Mate.objects.filter(Q(requester=user) | Q(acceptor=user))
        mate_list = []
        for mate in mates:
            mate_list.append(mate.to_dict())
        return HttpResponse(json.dumps({
            'mates': mate_list
        }))
    except Mate.DoesNotExist:
        return HttpResponseNotFound(json.dumps({
            'message': u'当前没有课友'
        }))


@acquire_token
def query_my_mates_by_course(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    try:
        course_id = parameter_dict['course_id']
    except (KeyError, TypeError):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    try:
        mates = Mate.objects.filter(Q(course_id=course_id), Q(requester=user) | Q(acceptor=user))
        mate_list = []
        for mate in mates:
            mate_list.append(mate.to_dict())
        return HttpResponse(json.dumps({
            'mates': mate_list
        }))
    except Mate.DoesNotExist:
        return HttpResponseNotFound(json.dumps({
            'message': u'当前没有课友'
        }))


@acquire_token
def invite_mate(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    try:
        course_id = parameter_dict['course_id']
        accept_id = parameter_dict['accept_id']
    except (KeyError, TypeError):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)
    requester = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    try:
        acceptor = User.objects.get(user_id=accept_id)
        course = Course.objects.get(course_id=course_id)
    except (User.DoesNotExist, Course.DoesNotExist):
        return HttpResponseNotFound(json.dumps({
            'message': u'课程或用户不存在'
        }))
    mate_invitation = MateInvitation(
        course=course,
        requester=requester,
        acceptor=acceptor,
        status=0
    )
    return HttpResponse(json.dumps({
        'message': u'邀请成功'
    }))


@acquire_token
def accept_mate_invitation(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    try:
        invitation_id = parameter_dict['invitation_id']
    except (KeyError, TypeError):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)
    acceptor = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    try:
        invitation = MateInvitation.objects.get(invitation_id=invitation_id)
    except MateInvitation.DoesNotExist:
        return HttpResponseNotFound(json.dumps({
            'message': u'邀请不存在'
        }))
    if invitation.acceptor != acceptor:
        return HttpResponseNotAllowed(json.dumps({
            'message': u'无权限操作'
        }))
    invitation.status = 1
    invitation.save()
    new_mate = Mate(
        course=invitation.course,
        requester=invitation.requester,
        acceptor=invitation.acceptor,
        establish_time=datetime.datetime.now()
    )
    new_mate.save()
    return HttpResponse(json.dumps({
        'message': u'已接受邀请'
    }))



@acquire_token
def refuse_mate_invitation(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    try:
        invitation_id = parameter_dict['invitation_id']
    except (KeyError, TypeError):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)
    acceptor = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    try:
        invitation = MateInvitation.objects.get(invitation_id=invitation_id)
    except MateInvitation.DoesNotExist:
        return HttpResponseNotFound(json.dumps({
            'message': u'邀请不存在'
        }))
    if invitation.acceptor != acceptor:
        return HttpResponseNotAllowed(json.dumps({
            'message': u'无权限操作'
        }))
    invitation.status = -1
    invitation.save()
    return HttpResponse(json.dumps({
        'message': u'已拒绝邀请'
    }))

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
    mates = Mate.objects.filter(Q(requester=user) | Q(acceptor=user))
    mate_list = []
    for mate in mates:
        mate_list.append(mate.to_dict())
    return HttpResponse(json.dumps({
        'mates': mate_list
    }))


@acquire_token
def query_my_mates_by_course(request):
    parameter_dict = fetch_parameter_dict(request, 'GET')
    try:
        course_id = parameter_dict['course_id']
    except (KeyError, TypeError):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    mates = Mate.objects.filter(Q(course_id=course_id), Q(requester=user) | Q(acceptor=user))
    mate_list = []
    for mate in mates:
        mate_list.append(mate.to_dict())
    return HttpResponse(json.dumps({
        'mates': mate_list
    }))


@acquire_token
def invite_mate(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    try:
        course_id = int(parameter_dict['course_id'])
        accept_id = int(parameter_dict['accept_id'])
        acceptor = User.objects.get(user_id=accept_id)
        course = Course.objects.get(course_id=course_id)
    except (KeyError, TypeError, User.DoesNotExist, Course.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    requester = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    if requester.user_id == accept_id:
        return HttpResponseBadRequest(json.dumps({
            'message': u'你不能给自己发送邀请'
        }))

    if _fetch_mate_relation(requester, acceptor, course):
        return HttpResponseBadRequest(json.dumps({
            'message': u'你们已在该课程中建立课友关系'
        }))

    if _fetch_pending_invitation(requester, acceptor, course):
        return HttpResponseBadRequest(json.dumps({
            'message': u'你已发出邀请或已收到对方的邀请'
        }))

    mate_invitation = MateInvitation(
        course=course,
        requester=requester,
        acceptor=acceptor,
        status=0,
        request_time=datetime.datetime.now()
    )
    mate_invitation.save()
    return HttpResponse(json.dumps({
        'message': u'邀请成功',
        'invitation_id': mate_invitation.invitation_id
    }))


@acquire_token
def deal_mate_invitation(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    try:
        invitation_id = int(parameter_dict['invitation_id'])
        status = int(parameter_dict['status'])
        invitation = MateInvitation.objects.get(invitation_id=invitation_id)
    except (KeyError, TypeError, MateInvitation.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    acceptor = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    if invitation.acceptor != acceptor:
        return HttpResponseBadRequest(json.dumps({
            'message': u'无权限操作'
        }))
    if invitation.status == 1 or invitation.status == -1:
        return HttpResponseBadRequest(json.dumps({
            'message': u'你已接受或拒绝邀请'
        }))
    invitation.status = status
    invitation.save()

    if status == 1:
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
    elif status == -1:
        return HttpResponse(json.dumps({
            'message': u'已拒绝邀请'
        }))
    else:
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)


def _fetch_mate_relation(user1: User, user2: User, course: Course):
    try:
        mate = Mate.objects.get(course=course, requester=user1, acceptor=user2)
        return mate
    except Mate.DoesNotExist:
        try:
            mate = Mate.objects.get(course=course, requester=user2, acceptor=user1)
            return mate
        except Mate.DoesNotExist:
            return None


def _fetch_pending_invitation(user1: User, user2: User, course: Course):
    try:
        mate_invitation = MateInvitation.objects.get(course=course, requester=user1, acceptor=user2, status=0)
        return mate_invitation
    except MateInvitation.DoesNotExist:
        try:
            mate_invitation = MateInvitation.objects.get(course=course, requester=user2, acceptor=user1, status=0)
            return mate_invitation
        except MateInvitation.DoesNotExist:
            return None

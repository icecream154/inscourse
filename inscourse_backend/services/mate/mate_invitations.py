import json
import datetime

from django.db.models import Q
from django.http import *

from inscourse_backend.models.course.course import Course
from inscourse_backend.models.course.course_join import CourseJoin
from inscourse_backend.models.mate.mate import Mate
from inscourse_backend.models.mate.mate_invitation import MateInvitation
from inscourse_backend.models.user import User
from inscourse_backend.services.constants import EM_INVALID_OR_MISSING_PARAMETERS
from inscourse_backend.services.sys.token import fetch_user_by_token, TOKEN_HEADER_KEY
from inscourse_backend.services.token_filter import acquire_token
from inscourse_backend.utils.request_processor import fetch_parameter_dict
from inscourse_backend.utils.invitation_code_generator import *


@acquire_token
def query_course_mate_invitations(request):
    parameter_dict = fetch_parameter_dict(request, 'GET')
    try:
        course = Course.objects.get(course_id=int(parameter_dict['course_id']))
    except (KeyError, TypeError, Course.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)
    invitations = course.mateinvitation_set.all()
    invitations_list = []
    for invitation in invitations:
        invitations_list.append(invitation.to_dict())
    return HttpResponse(json.dumps({
        'invitations': invitations_list
    }))


@acquire_token
def invite_mate(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    print(parameter_dict)
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    try:
        course_id = int(parameter_dict['course_id'])
        print('cid: ' + str(course_id))
        description = parameter_dict['description']
        print('cid: ' + str(course_id) + ' des:' + description)
        course = Course.objects.get(course_id=course_id)
        CourseJoin.objects.get(course=course, user=user)
    except (KeyError, TypeError, User.DoesNotExist, Course.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)
    except CourseJoin.DoesNotExist:
        return HttpResponseForbidden(json.dumps({
            'message': u'你还未加入课程'
        }))

    try:
        Mate.objects.get(Q(course=course), Q(requester=user) | Q(acceptor=user))
        return HttpResponseForbidden(json.dumps({
            'message': u'你已经建立了课友关系'
        }))
    except Mate.DoesNotExist:
        try:
            MateInvitation.objects.get(course=course, requester=user)
            return HttpResponseForbidden(json.dumps({
                'message': u'你已经发布了课友邀请'
            }))
        except MateInvitation.DoesNotExist:
            mate_invitation = MateInvitation(
                course=course,
                requester=user,
                invitation_code='#',
                request_time=datetime.datetime.now(),
                description=description
            )
            mate_invitation.save()
            mate_invitation.invitation_code = generate_mate_invitation_code(mate_invitation.invitation_id)
            mate_invitation.save()
            return HttpResponse(json.dumps({
                'message': u'发布邀请成功',
                'invitation_id': mate_invitation.invitation_id,
                'invitation_code': mate_invitation.invitation_code
            }))


@acquire_token
def accept_mate_invitation(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    try:
        invitation_id = decode_mate_invitation_id_from_code(parameter_dict['invitation_code'])
        if invitation_id == -1:
            return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)
        invitation = MateInvitation.objects.get(invitation_id=invitation_id)
        course = invitation.course
        CourseJoin.objects.get(course=course, user=user)
    except (KeyError, TypeError, MateInvitation.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)
    except CourseJoin.DoesNotExist:
        return HttpResponseForbidden(json.dumps({
            'message': u'你还未加入课程'
        }))

    if invitation.requester.user_id == user.user_id:
        return HttpResponseForbidden(json.dumps({
            'message': u'你不能接受自己的邀请'
        }))

    try:
        Mate.objects.get(Q(course=course), Q(requester=user) | Q(acceptor=user))
        return HttpResponseBadRequest(json.dumps({
            'message': u'你已经建立了课友关系'
        }))
    except Mate.DoesNotExist:
        try:
            MateInvitation.objects.get(course=course, requester=user).delete()
        except MateInvitation.DoesNotExist:
            pass

        invitation.delete()
        Mate(course=course,
             requester=invitation.requester,
             acceptor=user,
             establish_time=datetime.datetime.now()).save()
        return HttpResponse(json.dumps({
            'message': u'接受邀请成功'
        }))


@acquire_token
def cancel_mate_invitation(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    try:
        invitation_id = int(parameter_dict['invitation_id'])
        invitation = MateInvitation.objects.get(invitation_id=invitation_id)
    except (KeyError, TypeError, MateInvitation.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)
    if invitation.requester != user:
        return HttpResponseForbidden(json.dumps({
            'message': u'无权操作'
        }))

    invitation.delete()
    return HttpResponse(json.dumps({
        'message': u'取消邀请成功'
    }))

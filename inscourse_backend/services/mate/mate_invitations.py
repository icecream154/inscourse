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


# TODO: 查询一门课下发出的课友邀请
def query_course_mate_invitations(request):
    pass


# TODO: 生成课友邀请邀请码
def _generate_mate_invitation_code():
    pass


@acquire_token
def invite_mate(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    try:
        course_id = int(parameter_dict['course_id'])
        description = parameter_dict['description']
        course = Course.objects.get(course_id=course_id)
        CourseJoin.objects.get(course=course, user=user)
    except (KeyError, TypeError, User.DoesNotExist, Course.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)
    except CourseJoin.DoesNotExist:
        return HttpResponseBadRequest(json.dumps({
            'message': u'你还未加入课程'
        }))

    try:
        Mate.objects.get(Q(course=course), Q(requester=user) | Q(acceptor=user))
        return HttpResponseBadRequest(json.dumps({
            'message': u'你已经建立了课友关系'
        }))
    except Mate.DoesNotExist:
        try:
            MateInvitation.objects.get(course=course, requester=user)
            return HttpResponseBadRequest(json.dumps({
                'message': u'你已经发布了课友邀请'
            }))
        except MateInvitation.DoesNotExist:
            mate_invitation = MateInvitation(
                course=course,
                requester=user,
                invitation_code=_generate_mate_invitation_code(),
                status=0,
                request_time=datetime.datetime.now(),
                description=description
            )
            mate_invitation.save()
            return HttpResponse(json.dumps({
                'message': u'邀请成功',
                'invitation_id': mate_invitation.invitation_id
            }))


@acquire_token
def accept_mate_invitation(request):
    # TODO：接受邀请，要检查是否加入课程，是否已经和其他人建立了课友关系，是否是自己接受自己的邀请
    #  接受邀请后检查自己是否已经发出了邀请，如果有，则需要删除自己发出的邀请
    parameter_dict = fetch_parameter_dict(request, 'POST')
    try:
        invitation_id = int(parameter_dict['invitation_id'])
        status = int(parameter_dict['status'])
        invitation = MateInvitation.objects.get(invitation_id=invitation_id)
    except (KeyError, TypeError, MateInvitation.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    # acceptor = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    # if invitation.acceptor != acceptor:
    #     return HttpResponseBadRequest(json.dumps({
    #         'message': u'无权限操作'
    #     }))
    # if invitation.status == 1 or invitation.status == -1:
    #     return HttpResponseBadRequest(json.dumps({
    #         'message': u'你已接受或拒绝邀请'
    #     }))
    # invitation.status = status
    # invitation.save()
    #
    # if status == 1:
    #     new_mate = Mate(
    #         course=invitation.course,
    #         requester=invitation.requester,
    #         acceptor=invitation.acceptor,
    #         establish_time=datetime.datetime.now()
    #     )
    #     new_mate.save()
    #     return HttpResponse(json.dumps({
    #         'message': u'已接受邀请'
    #     }))
    # elif status == -1:
    #     return HttpResponse(json.dumps({
    #         'message': u'已拒绝邀请'
    #     }))
    # else:
    #     return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)


def cancel_mate_invitation(request):
    # TODO: 取消课友邀请，要判断自己有没有在这门课下的邀请，判断是否已经有这门课下的课友关系
    pass

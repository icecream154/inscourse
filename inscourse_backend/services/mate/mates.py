import json

from django.db.models import Q
from django.http import *

from inscourse_backend.models.course.course import Course
from inscourse_backend.models.course.course_join import CourseJoin
from inscourse_backend.models.mate.mate import Mate
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
def query_my_mate_by_course(request):
    parameter_dict = fetch_parameter_dict(request, 'GET')
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    try:
        course = Course.objects.get(course_id=int(parameter_dict['course_id']))
        CourseJoin.objects.get(course=course, user=user)
    except (KeyError, TypeError, Course.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)
    except CourseJoin.DoesNotExist:
        return HttpResponseBadRequest(json.dumps({
            'message': u'你还未加入课程'
        }))

    try:
        mate = Mate.objects.get(Q(course=course), Q(requester=user) | Q(acceptor=user))
        return HttpResponse(json.dumps({
            'mate': mate.to_dict()
        }))
    except Mate.DoesNotExist:
        return HttpResponseNotFound(json.dumps({
            'message': u'你还没有课友'
        }))


@acquire_token
def unbind_mate(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    try:
        mate = Mate.objects.get(mate_id=int(parameter_dict['mate_id']))
    except (KeyError, TypeError, Mate.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    if mate.requester != user and mate.acceptor != user:
        return HttpResponseForbidden(json.dumps({
            'message': u'无权操作'
        }))

    return HttpResponse(json.dumps({
        'message': u'课友关系解除成功'
    }))

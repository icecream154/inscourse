import json

from django.http import *

from inscourse_backend.models.course.course import Course
from inscourse_backend.models.course.course_join import CourseJoin
from inscourse_backend.services.constants import EM_INVALID_OR_MISSING_PARAMETERS
from inscourse_backend.services.sys.token import fetch_user_by_token, TOKEN_HEADER_KEY
from inscourse_backend.services.token_filter import acquire_token
from inscourse_backend.utils.request_processor import fetch_parameter_dict


@acquire_token
def query_my_joined_course(request):
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    course_joins = user.coursejoin_set.all()
    courses_list = []
    for course_join in course_joins:
        courses_list.append(course_join.course.to_dict())
    return HttpResponse(json.dumps({
        'courses': courses_list
    }))


@acquire_token
def join_course(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    try:
        course = Course.objects.get(course_id=int(parameter_dict['course_id']))
    except (KeyError, TypeError, Course.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    if is_joined(user, course):
        return HttpResponseForbidden(json.dumps({
            'message': u'你已经加入该课程'
        }))
    else:
        CourseJoin(user=user, course=course).save()
        return HttpResponse(json.dumps({
            'message': u'加入课程成功'
        }))


@acquire_token
def drop_out_course(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    try:
        course = Course.objects.get(course_id=int(parameter_dict['course_id']))
    except (KeyError, TypeError, Course.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    try:
        CourseJoin.objects.get(user=user, course=course).delete()
        return HttpResponse(json.dumps({
            'message': u'退出课程成功'
        }))
    except CourseJoin.DoesNotExist:
        return HttpResponseForbidden(json.dumps({
            'message': u'你还未加入该课程'
        }))

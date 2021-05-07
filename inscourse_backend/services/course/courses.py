import json

from django.http import *

from inscourse_backend.models.course.course import Course
from inscourse_backend.models.course.course_join import CourseJoin
from inscourse_backend.services.constants import EM_INVALID_OR_MISSING_PARAMETERS
from inscourse_backend.services.sys.token import fetch_user_by_token, TOKEN_HEADER_KEY
from inscourse_backend.services.token_filter import acquire_token
from inscourse_backend.utils.invitation_code_generator import generate_course_invitation_code
from inscourse_backend.utils.request_processor import fetch_parameter_dict


@acquire_token
def query_certain_course(request):
    parameter_dict = fetch_parameter_dict(request, 'GET')
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    try:
        course = Course.objects.get(course_id=int(parameter_dict['course_id']))
    except (KeyError, TypeError, Course.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)
    return HttpResponse(json.dumps({
        'course': course.to_dict(user)
    }))


@acquire_token
def query_open_courses(request):
    parameter_dict = fetch_parameter_dict(request, 'GET')
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    try:
        name = parameter_dict['name']
        category = int(parameter_dict['category'])
        order_by = parameter_dict['order_by']
        page_size = int(parameter_dict['page_size'])
        page_num = int(parameter_dict['page_num'])
    except (KeyError, TypeError):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)
    # 查询数据库
    start = (page_num - 1) * page_size
    end = start + page_size
    courses = Course.objects.filter(name__contains=name, category=category, status=1)[start: end]
    count = Course.objects.filter(name__contains=name, category=category, status=1).count()
    course_list = []
    for course in courses:
        course_list.append(course.to_dict(user))
    # 返回成功
    return HttpResponse(json.dumps({
        'count': count,
        'courses': course_list
    }))


@acquire_token
def upload_course(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    try:
        name = parameter_dict['name']
        description = parameter_dict['description']
        category = parameter_dict['category']
    except KeyError:
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    course = Course(author=user,
                    status=0,
                    name=name,
                    description=description,
                    level=0,
                    heat=0,
                    category=category,
                    invitation_code='#')
    course.save()
    course.invitation_code = generate_course_invitation_code(course.course_id)
    course.save()
    CourseJoin(user=user, course=course).save()
    return HttpResponse(json.dumps({
        'message': u'新建成功',
        'course_id': course.course_id
    }))


@acquire_token
def publish(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    try:
        course = Course.objects.get(course_id=int(parameter_dict['course_id']))
    except (KeyError, TypeError, Course.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    # 是否为创建者
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    if course.author.user_id != user.user_id:
        return HttpResponseForbidden(json.dumps({
            'message': u'对不起，你不是课程的创建者'
        }))
    # 课程是否已经公开
    if course.status == 1:
        return HttpResponseForbidden(json.dumps({
            'message': u'该课程已公开'
        }))
    else:
        course.status = 1
        course.save()
        return HttpResponse(json.dumps({
            'message': u'公开课程成功'
        }))

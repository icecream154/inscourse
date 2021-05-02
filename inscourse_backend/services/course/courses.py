from django.db.models import Q
from django.http import *

from inscourse_backend.models.course import Course
from inscourse_backend.services.constants import EM_INVALID_OR_MISSING_PARAMETERS
from inscourse_backend.services.sys.token import fetch_user_by_token, TOKEN_HEADER_KEY
from inscourse_backend.services.token_filter import acquire_token
from inscourse_backend.utils.request_processor import fetch_parameter_dict


def fetch_open_courses(request):
    parameter_dict = fetch_parameter_dict(request, 'GET')
    try:
        course_id = parameter_dict['course_id']
        category = parameter_dict['category']
        # orderBy = parameter_dict['orderBy']
        pageSize = parameter_dict['pageSize']
        pageNum = parameter_dict['pageNum']
    except KeyError:
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)
    # 查询数据库
    try:
        start = (pageNum - 1) * pageSize
        end = start + pageSize
        courses = Course.objects.filter(
            Q(course_id=course_id) & Q(category=category)
        )[start, end]
        count = Course.objects.filter(
            Q(course_id=course_id) & Q(category=category)
        ).count()
        course_list = []
        for course in courses:
            course_list.append(course.to_dict())
        # 返回成功
        return HttpResponse({
            'count': count,
            'courses': course_list
        })
    except Course.DoesNotExist:
        return HttpResponseNotFound({
            'message': '没有查询到相关课程'
        })


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
    course = Course(author_id=user.user_id,
                    status=0,
                    name=name,
                    description=description,
                    category=category)
    course.save()


@acquire_token
def query_course(request):
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    courses = Course.objects.filter(author_id=user.user_id)
    courses_list = []
    for course in courses:
        courses_list.append(course.to_dict())
    return HttpResponse({
        'courses': courses_list
    })


@acquire_token
def publish(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    try:
        course_id = parameter_dict['course_id']
    except KeyError:
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)
    try:
        course = Course.objects.get(course_id=course_id)
        # 是否为创建者
        user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
        if course.author_id != user.user_id:
            return HttpResponseForbidden({
                'message': '对不起，你不是课程的创建者'
            })
        # 课程是否已经公开
        if course.status == 1:
            return HttpResponseForbidden({
                'message': '该课程已公开'
            })
        else:
            course.status = 1
            course.save()
            return HttpResponse({
                'message': '公开课程成功'
            })
    except Course.DoesNotExist:
        return HttpResponseNotFound({
            'message': '无法查询到该课程'
        })




import json

from django.http import *

from inscourse_backend.models.course import Course
from inscourse_backend.models.resource import Resource
from inscourse_backend.services.constants import EM_INVALID_OR_MISSING_PARAMETERS
from inscourse_backend.services.sys.token import fetch_user_by_token, TOKEN_HEADER_KEY
from inscourse_backend.services.token_filter import acquire_token
from inscourse_backend.utils.request_processor import fetch_parameter_dict


@acquire_token
def release_resource(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    try:
        course_id = int(parameter_dict['course_id'])
        resource_key = parameter_dict['resource_key']
        description = parameter_dict['description']
        content_type = int(parameter_dict['content_type'])
        content = parameter_dict['content']
        course = Course.objects.get(course_id=course_id)
    except (KeyError, TypeError, Course.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    resource = Resource(course=course,
                        user=user,
                        resource_key=resource_key,
                        description=description,
                        content_type=content_type,
                        content=content)
    resource.save()
    return HttpResponse(json.dumps({
        'message': u'发布成功',
        'resource_id': resource.resource_id
    }))


@acquire_token
def query_resource_by_course(request):
    parameter_dict = fetch_parameter_dict(request, 'GET')

    # 检查course_id
    try:
        course_id = int(parameter_dict['course_id'])
        course = Course.objects.get(course_id=course_id)
    except (KeyError, TypeError, Course.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    resources = course.resource_set.all()
    resources_list = []
    for resource in resources:
        resources_list.append(resource.to_dict())
    return HttpResponse(json.dumps({
        'resources': resources_list
    }))


@acquire_token
def modify_resource(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')

    # 检查resource_id
    try:
        resource_id = int(parameter_dict['resource_id'])
        resource = Resource.objects.get(resource_id=resource_id)
    except(KeyError, TypeError, Resource.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    # 核对resource提交人
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    if resource.user.user_id != user.user_id:
        return HttpResponseForbidden(json.dumps({
            'message': u'对不起，你不是课程资源的创建者'
        }))

    # 修改resource
    try:
        resource_key = parameter_dict['resource_key']
        description = parameter_dict['description']
        content_type = parameter_dict['content_type']
        content = parameter_dict['content']
    except KeyError:
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)
    resource.resource_key = resource_key
    resource.description = description
    resource.content_type = content_type
    resource.content = content
    resource.save()
    return HttpResponse(json.dumps({
        'message': u'修改成功'
    }))


@acquire_token
def delete_resource(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')

    # 检查resource_id
    try:
        resource_id = int(parameter_dict['resource_id'])
        resource = Resource.objects.get(resource_id=resource_id)
    except(KeyError, TypeError, Resource.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    # 核对resource提交人
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    if resource.user.user_id != user.user_id:
        return HttpResponseForbidden(json.dumps({
            'message': u'对不起，你不是课程资源的创建者'
        }))

    # 删除resource
    resource.delete()
    return HttpResponse(json.dumps({
        'message': u'删除成功'
    }))

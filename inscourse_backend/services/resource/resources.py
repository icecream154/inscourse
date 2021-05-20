import json

from django.http import *

from inscourse_backend.models.course.course import Course
from inscourse_backend.models.course.course_join import CourseJoin
from inscourse_backend.models.resource.resource import Resource
from inscourse_backend.models.resource.resource_fav import ResourceFav
from inscourse_backend.models.resource.resource_prefer import ResourcePrefer
from inscourse_backend.services.constants import EM_INVALID_OR_MISSING_PARAMETERS
from inscourse_backend.services.resource.resource_dict import to_resource_dict
from inscourse_backend.services.sys.token import fetch_user_by_token, TOKEN_HEADER_KEY
from inscourse_backend.services.token_filter import acquire_token
from inscourse_backend.utils.request_processor import fetch_parameter_dict


@acquire_token
def release_resource(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    try:
        course_id = int(parameter_dict['course_id'])
        resource_key = parameter_dict['resource_key']
        description = parameter_dict['description']
        content_type = int(parameter_dict['content_type'])
        content = parameter_dict['content']
        course = Course.objects.get(course_id=course_id)
        CourseJoin.objects.get(course=course, user=user)
    except (KeyError, TypeError, Course.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)
    except CourseJoin.DoesNotExist:
        return HttpResponseBadRequest(json.dumps({
            'message': u'你还未加入课程'
        }))

    resource = Resource(
        course=course,
        user=user,
        resource_key=resource_key,
        description=description,
        content_type=content_type,
        content=content
    )
    resource.save()
    return HttpResponse(json.dumps({
        'message': u'发布成功',
        'resource_id': resource.resource_id
    }))


@acquire_token
def query_resource_by_course(request):
    parameter_dict = fetch_parameter_dict(request, 'GET')
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])

    try:
        course = Course.objects.get(course_id=int(parameter_dict['course_id']))
        content_type = int(parameter_dict['content_type'])
        CourseJoin.objects.get(course=course, user=user)
    except (KeyError, TypeError, Course.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)
    except CourseJoin.DoesNotExist:
        return HttpResponseBadRequest(json.dumps({
            'message': u'你还未加入课程'
        }))

    if content_type == -1:
        resources = course.resource_set.all()
    else:
        resources = course.resource_set.filter(content_type=content_type)

    resources_list = []
    for resource in resources:
        resources_list.append(to_resource_dict(resource, user))
    return HttpResponse(json.dumps({
        'resources': resources_list
    }))


@acquire_token
def modify_resource(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')

    try:
        resource_id = int(parameter_dict['resource_id'])
        resource = Resource.objects.get(resource_id=resource_id)
    except(KeyError, TypeError, Resource.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    # 核对resource提交人
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    if resource.user.user_id != user.user_id:
        return HttpResponseForbidden(json.dumps({
            'message': u'你不是发布者'
        }))

    # 修改resource
    try:
        resource_key = parameter_dict['resource_key']
        description = parameter_dict['description']
        content_type = parameter_dict['content_type']
        content = parameter_dict['content']
    except (KeyError, TypeError):
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
            'message': u'你不是发布者'
        }))

    # 删除resource
    resource.delete()
    return HttpResponse(json.dumps({
        'message': u'删除成功'
    }))


@acquire_token
def query_my_resource_by_course(request):
    parameter_dict = fetch_parameter_dict(request, 'GET')
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])

    try:
        course_id = int(parameter_dict['course_id'])
        course = Course.objects.get(course_id=course_id)
    except (KeyError, TypeError, Course.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    resources = course.resource_set.filter(user=user)
    resources_list = []
    for resource in resources:
        resources_list.append(to_resource_dict(resource, user))
    return HttpResponse(json.dumps({
        'resources': resources_list
    }))


@acquire_token
def resource_fav(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])

    try:
        resource = Resource.objects.get(resource_id=int(parameter_dict['resource_id']))
    except(KeyError, TypeError, Resource.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    favors = ResourceFav.objects.filter(resource=resource, user=user)
    if favors.exists():
        return HttpResponseBadRequest(json.dumps({
            'message': u'你已收藏过该帖'
        }))
    else:
        favor = ResourceFav(
            resource=resource,
            user=user
        )
        favor.save()
        return HttpResponse(json.dumps({
            'message': u'收藏成功'
        }))


@acquire_token
def cancel_resource_fav(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])

    try:
        resource = Resource.objects.get(resource_id=int(parameter_dict['resource_id']))
        favor = ResourceFav.objects.get(resource=resource, user=user)
    except(KeyError, TypeError, Resource.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)
    except ResourceFav.DoesNotExist:
        return HttpResponseBadRequest(json.dumps({
            'message': u'你尚未收藏该帖'
        }))
    favor.delete()
    return HttpResponse(json.dumps({
        'message': u'取消收藏成功'
    }))


@acquire_token
def query_favored_resource(request):
    parameter_dict = fetch_parameter_dict(request, 'GET')
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    try:
        course = Course.objects.get(course_id=int(parameter_dict['course_id']))
    except (KeyError, TypeError, Course.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    favors = ResourceFav.objects.filter(resource__course=course, user=user)
    resources_list = []
    for favor in favors:
        resources_list.append(favor.to_resource_dict(favor.resource, user))
    return HttpResponse(json.dumps({
        'resources': resources_list
    }))


@acquire_token
def resource_prefer(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    try:
        resource = Resource.objects.get(resource_id=int(parameter_dict['resource_id']))
    except(KeyError, TypeError, Resource.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    prefers = ResourcePrefer.objects.filter(resource=resource, user=user)
    if prefers.exists():
        return HttpResponseBadRequest(json.dumps({
            'message': u'你已点赞过该帖'
        }))
    else:
        prefer = ResourcePrefer(
            resource=resource,
            user=user
        )
        prefer.save()
        return HttpResponse(json.dumps({
            'message': u'点赞成功'
        }))


@acquire_token
def cancel_resource_prefer(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])

    try:
        resource = Resource.objects.get(resource_id=int(parameter_dict['resource_id']))
        prefer = ResourcePrefer.objects.get(resource=resource, user=user)
    except(KeyError, TypeError, Resource.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)
    except ResourcePrefer.DoesNotExist:
        return HttpResponseBadRequest(json.dumps({
            'message': u'你尚未点赞该帖'
        }))

    prefer.delete()
    return HttpResponse(json.dumps({
        'message': u'已取消点赞'
    }))


@acquire_token
def query_certain_resource(request):
    parameter_dict = fetch_parameter_dict(request, 'GET')
    user = fetch_user_by_token(request.META[TOKEN_HEADER_KEY])
    try:
        resource = Resource.objects.get(resource_id=int(parameter_dict['resource_id']))
    except(KeyError, TypeError, Resource.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    return HttpResponse(json.dumps({
        'resource': to_resource_dict(resource, user)
    }))

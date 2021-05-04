import json

from django.db.models import Q
from django.http import *

from inscourse_backend.models.mate import Mate
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
def create_mate(request):
    return


@acquire_token
def invite_mate(request):
    return


@acquire_token
def accept_mate_invitation(request):
    return

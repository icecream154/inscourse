from django.urls import path

from inscourse_backend.services.course.courses import *
from inscourse_backend.services.course.course_joins import *
from inscourse_backend.services.resource.resources import *
from inscourse_backend.services.sys.users import *
from inscourse_backend.services.mate.mates import *
from inscourse_backend.services.mate.mate_invitations import *
from inscourse_backend.services.assignment.assignments import *

urlpatterns = [
    # 用户模块
    path('sys/login', login, name='login'),
    path('sys/adminLogin', admin_login, name='admin_login'),
    path('sys/changeUserInfo', change_user_info, name='change_user_info'),
    path('sys/getMyInfo', get_my_info, name='get_my_info'),
    path('sys/getUserAvatar', get_user_avatar, name='get_user_avatar'),

    # 课程模块
    path('course/queryCertainCourse', query_certain_course, name='query_certain_course'),
    path('course/queryOpenCourses', query_open_courses, name='query_open_courses'),
    path('course/publish', publish, name='publish'),
    path('course/uploadCourse', upload_course, name='upload_course'),
    path('course/queryMyJoinedCourse', query_my_joined_course, name='query_my_joined_course'),
    path('course/joinCourse', join_course, name='join_course'),
    path('course/dropOutCourse', drop_out_course, name='drop_out_course'),
    path('course/getCourseIcon', get_course_icon, name='get_course_icon'),

    # 帖子模块
    path('resource/releaseResource', release_resource, name='release_resource'),
    path('resource/queryResourceByCourse', query_resource_by_course, name='query_resource_by_course'),
    path('resource/modifyResource', modify_resource, name='modify_resource'),
    path('resource/deleteResource', delete_resource, name='delete_resource'),
    path('resource/queryMyResourceByCourse', query_my_resource_by_course, name='query_my_resource_by_course'),

    path('resource/resourceFav', resource_fav, name='resource_fav'),
    path('resource/cancelResourceFav', cancel_resource_fav, name='cancel_resource_fav'),
    path('resource/resourcePrefer', resource_prefer, name='resource_prefer'),
    path('resource/cancelResourcePrefer', cancel_resource_prefer, name='cancel_resource_prefer'),
    path('resource/queryFavoredResources', query_favored_resource, name='query_favored_resource'),
    path('resource/queryCertainResource', query_certain_resource, name='query_certain_resource'),

    # 课友模块
    path('mate/queryMyMates', query_my_mates, name='query_my_mates'),
    path('mate/queryMyMateByCourse', query_my_mate_by_course, name='query_my_mate_by_course'),
    path('mate/unbind', unbind_mate, name='unbind_mate'),

    # 课友邀请部分
    path('mate/queryCourseMateInvitations', query_course_mate_invitations, name='query_course_mate_invitations'),
    path('mate/inviteMate', invite_mate, name='invite_mate'),
    path('mate/acceptMateInvitation', accept_mate_invitation, name='accept_mate_invitation'),
    path('mate/cancelMateInvitation', cancel_mate_invitation, name='cancel_mate_invitation'),

    # 日程模块
    path('assignment/queryMyAssignmentsByMate', query_my_assignments_by_mate, name='query_my_assignments_by_mate'),
    path('assignment/newAssignment', new_assignment, name='new_assignment'),
    path('assignment/modifyAssignment', modify_assignment, name='modify_assignment'),
    path('assignment/deleteAssignment', delete_assignment, name='delete_assignment'),
    path('assignment/checkAssignment', check_assignment, name='check_assignment')
]

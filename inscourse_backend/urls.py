from django.urls import path

from inscourse_backend.services.course.courses import *
from inscourse_backend.services.resource.resources import *
from inscourse_backend.services.sys.users import *
from inscourse_backend.services.mate.mates import *
from inscourse_backend.services.assignment.assignments import *

urlpatterns = [
    # 用户模块
    path('sys/login', login, name='login'),
    path('sys/adminLogin', admin_login, name='admin_login'),
    path('sys/changeUsername', change_username, name='change_username'),
    path('sys/getMyInfo', get_my_info, name='get_my_info'),

    # 课程模块
    path('course/queryOpenCourses', query_open_courses, name='query_open_courses'),
    path('course/publish', publish, name='publish'),
    path('course/uploadCourse', upload_course, name='upload_course'),
    path('course/queryMyCourse', query_my_course, name='query_my_course'),

    # 帖子模块
    path('resource/releaseResource', release_resource, name='release_resource'),
    path('resource/queryResourceByCourse', query_resource_by_course, name='query_resource_by_course'),
    path('resource/modifyResource', modify_resource, name='modify_resource'),
    path('resource/deleteResource', delete_resource, name='delete_resource'),
    path('resource/queryMyResourceByCourse', query_my_resource_by_course, name='query_my_resource_by_course'),

    # TODO: 帖子的（取消）收藏和（取消）点赞，查看已收藏的帖子,查看某个帖子
    path('resource/resourceFav', resource_fav, name='resource_fav'),
    path('resource/cancelResourceFav', cancel_resource_fav, name='cancel_resource_fav'),
    path('resource/resourcePrefer', resource_prefer, name='resource_prefer'),
    path('resource/cancelResourcePrefer', cancel_resource_prefer, name='cancel_resource_prefer'),
    path('resource/queryFavoredResources', query_favored_resource, name='query_favored_resource'),
    path('resource/queryCertainResource', query_certain_resource, name='query_certain_resource')

    # # 课友模块
    # path('mate/queryMyMates', query_my_mates, name='query_my_mates'),
    # path('mate/queryMyMatesByCourse', query_my_mates_by_course, name='query_my_mates_by_course'),
    # path('mate/inviteMate', invite_mate, name='invite_mate'),
    # path('mate/dealMateInvitation', deal_mate_invitation, name='deal_mate_invitation'),
    #
    # # 日程模块
    # path('assignment/queryMySchedulesByMate', query_my_assignments_by_mate, name='query_my_schedules_by_mate'),
    # path('assignment/newSchedule', new_assignment, name='new_schedule'),
    # path('assignment/modifySchedule', modify_assignment, name='modify_schedule'),
    # path('assignment/deleteSchedule', delete_schedule, name='delete_schedule'),
]

from django.urls import path

from inscourse_backend.services.course.courses import *
from inscourse_backend.services.resource.resources import *
from inscourse_backend.services.sys.users import *


urlpatterns = [
    path('sys/login', login, name='login'),
    path('sys/adminLogin', admin_login, name='admin_login'),
    path('sys/changeUsername', change_username, name='change_username'),
    path('course/queryOpenCourses', query_open_courses, name='fetch_open_courses'),  # TODO: 为什么name不是query_open_courses
    path('course/publish', publish, name='publish'),
    path('course/uploadCourse', upload_course, name='upload_course'),
    path('course/queryMyCourse', query_my_course, name='query_course'),  # TODO: 为什么name不是query_my_course
    path('resource/releaseResource', release_resource, name='release_resource'),
    path('resource/queryResource', query_resource, name='query_resource'),
    path('resource/modifyResource', modify_resource, name='modify_resource'),
    path('resource/deleteResource', delete_resource, name='delete_resource')
]

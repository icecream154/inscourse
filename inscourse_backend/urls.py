from django.urls import path

from inscourse_backend.services.course.courses import *
from inscourse_backend.services.sys.users import *

urlpatterns = [
    path('sys/login', login, name='login'),
    path('sys/changeName', change_username, name='change_username'),
    path('course/fetchOpenCourses', fetch_open_courses, name='fetch_open_courses'),
    path('course/publish', publish, name='publish'),
    path('course/uploadCourse', upload_course, name='upload_course'),
    path('/course/queryCourse', query_course, name='query_course')
]

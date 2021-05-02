from django.contrib import admin

# Register your models here.
from inscourse_backend.models.course import Course
from inscourse_backend.models.coursejoin import CourseJoin
from inscourse_backend.models.mate import Mate
from inscourse_backend.models.mateschedule import MateSchedule
from inscourse_backend.models.user import User
from inscourse_backend.models.resource import Resource

admin.site.register(User)
admin.site.register(Course)
admin.site.register(CourseJoin)
admin.site.register(Mate)
admin.site.register(MateSchedule)
admin.site.register(Resource)

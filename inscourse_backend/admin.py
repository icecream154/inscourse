from django.contrib import admin

# Register your models here.
from inscourse_backend.models.course.course import Course
from inscourse_backend.models.course.course_join import CourseJoin
from inscourse_backend.models.mate.mate import Mate
from inscourse_backend.models.mate.mate_assignment import MateAssignment
from inscourse_backend.models.user import User
from inscourse_backend.models.resource.resource import Resource
from inscourse_backend.models.mate.mate_invitation import MateInvitation


admin.site.register(User)
admin.site.register(Course)
admin.site.register(CourseJoin)
admin.site.register(Mate)
admin.site.register(MateInvitation)
admin.site.register(MateAssignment)
admin.site.register(Resource)

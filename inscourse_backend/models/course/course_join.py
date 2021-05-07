from django.db import models

from inscourse_backend.models.course.course import Course
from inscourse_backend.models.user import User


class CourseJoin(models.Model):
    # 用户id
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 课程id
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

from django.db import models

from inscourse_backend.models.course import Course


class Mate(models.Model):
    # 课友关系id
    mate_id = models.AutoField(primary_key=True)
    # 课程id
    course_id = models.IntegerField()
    # 发起者id
    request_user = models.IntegerField()
    # 接受者id
    accept_id = models.IntegerField()
    # 建立时间
    establish_time = models.DateTimeField()

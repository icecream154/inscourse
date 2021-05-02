from django.db import models

from inscourse_backend.models.user import User


class Resource(models.Model):
    # 课程ID
    course_id = models.AutoField(primary_key=True)
    # 用户id
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # 资源名称
    resource_key = models.CharField(max_length=20)
    # 资源介绍
    description = models.CharField(max_length=255)
    # 资源类别
    type = models.IntegerField()
    # 资源内容
    content = models.CharField(max_length=255)

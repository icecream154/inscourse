from django.db import models

from inscourse_backend.models.course.course import Course
from inscourse_backend.models.user import User


class Resource(models.Model):
    # 资源id
    resource_id = models.AutoField(primary_key=True)
    # 课程ID
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # 上传用户id
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 资源名称
    resource_key = models.CharField(max_length=20)
    # 资源介绍
    description = models.CharField(max_length=255)
    # 资源类别
    content_type = models.IntegerField()
    # 资源内容
    content = models.TextField()

    def to_dict(self):
        dictionary = {
            'resource_id': self.resource_id,
            'course_id': self.course.course_id,
            'user_id': self.user.user_id,
            'resource_key': self.resource_key,
            'description': self.description,
            'content_type': self.content_type,
            'content': self.content
        }
        return dictionary
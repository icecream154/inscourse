from django.db import models

from inscourse_backend.models.course.course import Course
from inscourse_backend.models.user import User


class Resource(models.Model):
    # 资源id
    resource_id = models.AutoField(primary_key=True)
    # 课程ID
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # 上传用户
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 资源名称
    resource_key = models.CharField(max_length=20)
    # 资源介绍
    description = models.CharField(max_length=255)
    # 资源类别 0->text, 1->video, 2->pdf, 3->others
    content_type = models.IntegerField()
    # 资源内容
    content = models.TextField()
    # 总收藏数
    favors = models.IntegerField(default=0)
    # 总点赞数
    prefers = models.IntegerField(default=0)

    def to_dict(self):
        dictionary = {
            'resource_id': self.resource_id,
            'course_id': self.course.course_id,
            'user_id': self.user.user_id,
            'author_name': self.user.username,
            'resource_key': self.resource_key,
            'description': self.description,
            'content_type': self.content_type,
            'content': self.content,
            'favors': self.favors,
            'prefers': self.prefers
        }
        return dictionary

    def validate(self):
        valid_content_types = [0, 1, 2]
        if len(self.description) > 50:
            return u'简介不能超过50个字符'
        if self.content_type not in valid_content_types:
            return u'不支持的资源类型'
        return None

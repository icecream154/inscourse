from django.db import models

from inscourse_backend.models.user import User


class Course(models.Model):
    # 课程id
    course_id = models.AutoField(primary_key=True)
    # 上传者
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 课程公开状态 (0 为私有， 1 为公开)
    status = models.IntegerField()
    # 课程名
    name = models.CharField(max_length=20)
    # 课程简介
    description = models.CharField(max_length=255)
    # 课程评价
    level = models.IntegerField()
    # 课程热度
    heat = models.IntegerField()
    # 课程图标
    image = models.CharField(max_length=255, null=True)
    # 课程大类
    category = models.IntegerField()
    # 课程邀请码
    invitation_code = models.CharField(max_length=6)

    def to_dict(self):
        dictionary = {
            'course_id': self.course_id,
            'author_id': self.author.user_id,
            'status': self.status,
            'name': self.name,
            'description': self.description,
            'level': self.level,
            'heat': self.heat,
            'image': self.image,
            'category': self.category,
            'invitation_code': self.invitation_code
        }
        return dictionary

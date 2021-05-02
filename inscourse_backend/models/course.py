from django.db import models

from inscourse_backend.models.user import User


class Course(models.Model):
    # 课程id
    course_id = models.AutoField(primary_key=True)
    # 上传者id
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # 课程公开状态
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
    image = models.BinaryField()
    # 课程大类
    category = models.IntegerField()

    def to_dict(self):
        dictionary = {
            'course_id': self.course_id,
            'author_id': self.author_id,
            'status': self.status,
            'name': self.name,
            'description': self.description,
            'level': self.level,
            'heat': self.heat,
            'image': self.image,
            'category': self.category
        }
        return dictionary

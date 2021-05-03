from django.db import models

from inscourse_backend.models.course import Course


class Mate(models.Model):
    # 课友关系id
    mate_id = models.AutoField(primary_key=True)
    # 课程id
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    # 发起者id
    request_user = models.IntegerField()
    # 接受者id
    accept_id = models.IntegerField()
    # 建立时间
    establish_time = models.DateTimeField()

    def to_dict(self):
        dictionary = {
            'mate_id': self.mate_id,
            'course_id': self.course_id,
            'request_user': self.request_user,
            'accept_id': self.accept_id,
            'establish_time': self.establish_time
        }
        return dictionary

from django.db import models

from inscourse_backend.models.course import Course
from inscourse_backend.models.user import User


class Mate(models.Model):
    # 课友关系id
    mate_id = models.AutoField(primary_key=True)
    # 课程
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # 发起者
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requester')
    # 接受者
    acceptor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='acceptor')
    # 建立时间
    establish_time = models.DateTimeField()

    def to_dict(self):
        dictionary = {
            'mate_id': self.mate_id,
            'course_id': self.course.course_id,
            'requester_id': self.requester.user_id,
            'acceptor_id': self.acceptor.user_id,
            'establish_time': self.establish_time
        }
        return dictionary

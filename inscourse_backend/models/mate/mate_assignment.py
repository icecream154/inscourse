from django.db import models

from inscourse_backend.models.mate.mate import Mate
from inscourse_backend.services.constants import DATE_FORMAT


class MateAssignment(models.Model):
    # 日程id
    assignment_id = models.AutoField(primary_key=True)
    # 课友关系id
    mate = models.ForeignKey(Mate, on_delete=models.CASCADE)
    # 日程内容
    content = models.TextField()
    # 当前状态 0: 都未完成 1: requester完成 2: acceptor完成 3: 都完成
    status = models.IntegerField(default=0)
    # 计划完成时间
    assignment_date = models.DateField()
    # 完成时间
    done_date = models.DateField(null=True, default=None)

    def to_dict(self):
        dictionary = {
            'assignment_id': self.assignment_id,
            'course_name': self.mate.course.name,
            'mate_id': self.mate.mate_id,
            'content': self.content,
            'status': self.status,
            'assignment_date': self.assignment_date.strftime(DATE_FORMAT),
            'done_date': self.done_date.strftime(DATE_FORMAT) if self.done_date else 'None'
        }
        return dictionary

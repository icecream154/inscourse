from datetime import datetime

from django.db import models

from inscourse_backend.models.mate.mate import Mate
from inscourse_backend.models.user import User
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

    def to_detail_dict(self, user: User):
        dictionary = self.to_dict()
        my_check_bit = 1 if user == self.mate.requester else 2
        mate_check_bit = 3 - my_check_bit
        dictionary['my_status'] = 0 if self.status & my_check_bit == 0 else 1
        dictionary['mate_status'] = 0 if self.status & mate_check_bit == 0 else 1
        return dictionary

    def check_status(self, user: User):
        my_check_bit = 1 if user == self.mate.requester else 2
        if self.status & my_check_bit == 0:
            self.status += my_check_bit
            if self.status == 3:
                self.done_date = datetime.today().date()
            return my_check_bit
        else:
            return 0

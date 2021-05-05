from django.db import models

from inscourse_backend.models.mate import Mate
from inscourse_backend.services.constants import DATE_FORMAT


class MateSchedule(models.Model):
    # 日程id
    schedule_id = models.AutoField(primary_key=True)
    # 课友关系id
    mate = models.ForeignKey(Mate, on_delete=models.CASCADE)
    # 日程内容
    content = models.TextField()
    # 当前状态 0: 未完成 1: 已完成
    status = models.IntegerField(default=0)
    # 计划完成时间
    schedule_date = models.DateField()
    # 完成时间
    done_date = models.DateField(null=True, default=None)

    def to_dict(self):
        dictionary = {
            'schedule_id': self.schedule_id,
            'mate_id': self.mate.mate_id,
            'content': self.content,
            'status': self.status,
            'schedule_date': self.schedule_date.strftime(DATE_FORMAT),
            'done_date': self.done_date.strftime(DATE_FORMAT) if self.done_date else 'None'
        }
        return dictionary

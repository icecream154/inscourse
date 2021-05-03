from django.db import models

from inscourse_backend.models.mate import Mate


class MateSchedule(models.Model):
    # 日程id
    schedule_id = models.AutoField(primary_key=True)
    # 课友关系id
    mate = models.ForeignKey(Mate, on_delete=models.CASCADE)
    # 日程时间
    date = models.DateField()
    # 日程内容
    content = models.TextField()
    # 百分比进度
    progress = models.IntegerField()
    # 当前状态
    status = models.IntegerField()

    def to_dict(self):
        dictionary = {
            'schedule_id': self.schedule_id,
            'mate_id': self.mate.mate_id,
            'date': self.date,
            'content': self.content,
            'progress': self.progress,
            'status': self.status
        }
        return dictionary

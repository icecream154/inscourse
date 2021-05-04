from django.db import models

from inscourse_backend.models.course import Course
from inscourse_backend.models.user import User


class MateInvitation(models.Model):
    # 课友邀请id
    invitation_id = models.AutoField(primary_key=True)
    # 课程
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # 发起者
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requester')
    # 接受者
    acceptor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='acceptor')
    # 邀请接受状况 0: 等待接受 1: 接受邀请 -1: 拒绝邀请
    status = models.IntegerField()

    def to_dict(self):
        dictionary = {
            'invitation_id': self.invitation_id,
            'course': self.course.course_id,
            'requester_id': self.requester.user_id,
            'acceptor_id': self.acceptor.user_id,
            'status': self.status
        }
        return dictionary

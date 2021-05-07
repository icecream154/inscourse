from django.db import models

from inscourse_backend.models.course.course import Course
from inscourse_backend.models.user import User


class MateInvitation(models.Model):
    # 课友邀请id
    invitation_id = models.AutoField(primary_key=True)
    # 课程
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # 发起者
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_user')
    # 邀请码
    invitation_code = models.CharField(max_length=8)
    # 建立时间
    request_time = models.DateTimeField()
    # 邀请描述
    description = models.CharField(max_length=50)

    def to_dict(self):
        dictionary = {
            'invitation_id': self.invitation_id,
            'course': self.course.course_id,
            'requester_id': self.requester.user_id,
            'invitation_code': self.invitation_code,
            'request_time': str(self.request_time),
            'description': self.description
        }
        return dictionary

from django.db import models


class User(models.Model):
    # 用户ID
    user_id = models.AutoField(primary_key=True)
    # 微信ID
    openid = models.CharField(max_length=255, unique=True)
    # 用户名
    username = models.CharField(max_length=20)
    # 公司/学校
    workspace = models.CharField(max_length=40, default='inscourse university')
    # 邮箱
    email = models.CharField(max_length=40, default='youremail@inscourse.com')
    # 签名
    signature = models.CharField(max_length=30, default='快来编辑你的个性签名吧')

    def to_dict(self):
        dictionary = {
            'user_id': self.user_id,
            'openid': self.openid,
            'username': self.username,
            'workspace': self.workspace,
            'email': self.email,
            'signature': self.signature
        }
        return dictionary

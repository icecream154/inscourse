from django.db import models


class User(models.Model):
    # 用户ID
    user_id = models.AutoField(primary_key=True)
    # 微信ID
    openid = models.CharField(max_length=255, unique=True)
    # 用户名
    username = models.CharField(max_length=20)


    def to_dict(self):
        dictionary = {
            'user_id': self.user_id,
            'openid': self.openid,
            'username': self.username
        }
        return dictionary

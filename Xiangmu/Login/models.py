from django.db import models

#创建表
class Login_User(models.Model):
    username = models.CharField(max_length=32)#用户名
    password = models.CharField(max_length=32)#登录密码
# Create your models here.

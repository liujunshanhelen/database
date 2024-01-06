from django.db import models

# Create your models here.
class Department(models.Model):
    """
    部门表
    """

    title = models.CharField(verbose_name='标题',max_length=32)

class UserInfo(models.Model):
    """
    用户表
    """
    name = models.CharField(verbose_name='用户名',max_length=32)
    password = models.CharField(verbose_name='密码',max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(verbose_name='账户余额',max_digits=10,decimal_places=2,default=0)
    creat_time =models.DateTimeField(verbose_name='入职时间')
    depart=models.ForeignKey(verbose_name='部门',to='Department',to_field='id',on_delete=models.CASCADE)
    gender_choices = (
        (1,'男'),
        (2,'女'),
    )
    gender=models.SmallIntegerField(verbose_name="性别",choices=gender_choices)

class PrettyNum(models.Model):
    mobile = models.CharField(verbose_name='手机号',max_length=20)
    price = models.IntegerField(verbose_name='价格')
    level_choices = (
        (1,'一星'),
        (2,'二星'),
        (3,'三星'),
        (4,'四星'),
        (5,'五星'),
    )
    level = models.SmallIntegerField(verbose_name='星级',choices=level_choices)
    status_choices = (
        (1,'在售'),
        (2,'已售'),
    )
    status = models.SmallIntegerField(verbose_name='状态',choices=status_choices)

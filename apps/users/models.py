# -*- coding: utf-8 -*-
from django.db import models

from datetime import datetime

from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserProfile(AbstractUser):
    nickname = models.CharField(max_length=50, default='', null=True, blank=True, verbose_name=u'昵称')
    birthday = models.DateField(null=True, blank=True, verbose_name=u'出生日期')
    gender = models.CharField(max_length=10, choices=(('male', u'男'), ('female', u'女')), default='female',
                              verbose_name=u'性别')
    address = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'地址')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name=u'手机号码')
    image = models.ImageField(max_length=100, upload_to='image/%Y/%M', default=u'image/default.png', verbose_name='头像')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u'验证码')
    address = models.EmailField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(max_length=10, choices=(('register', u'注册'), ('forget', u'忘记密码')), verbose_name=u'类型')
    send_time = models.DateTimeField(max_length=50, default=datetime.now, verbose_name=u'发送时间')

    def __str__(self):
        return self.code + '(' + self.address + ')'

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'标题')
    image = models.ImageField(max_length=100, upload_to='banner/%Y/%M', verbose_name=u'轮播图')
    url = models.URLField(max_length=200, verbose_name=u'访问地址')
    index = models.IntegerField(default=100, verbose_name=u'索引')
    add_time = models.DateTimeField(max_length=50, default=datetime.now, verbose_name=u'添加时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

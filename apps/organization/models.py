# -*- coding: utf-8 -*-
from django.db import models

from datetime import datetime


# Create your models here.

class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name='城市名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    desc = models.CharField(max_length=200, verbose_name='城市描述')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name='机构名称')
    desc = models.TextField(verbose_name='机构描述')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name='logo')
    address = models.CharField(max_length=150, verbose_name='课程机构地址')
    city = models.ForeignKey(CityDict, verbose_name='城市')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    category = models.CharField(max_length=20, choices=(('pxjg', '培训机构'), ('xs', '学校'), ('gr', '个人')), default='pxjg',
                                verbose_name='机构类型')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    course_count = models.IntegerField(default=0, verbose_name='课程数')

    def __str__(self):
        return self.name

    def get_teacher_count(self):
        return self.teacher_set.all().count()

    class Meta:
        verbose_name = '机构课程'
        verbose_name_plural = verbose_name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name='所属机构')
    name = models.CharField(max_length=20, verbose_name='教师名')
    work_years = models.IntegerField(default=0, verbose_name='工作年限')
    work_company = models.CharField(max_length=50, verbose_name='就职公司')
    work_position = models.CharField(max_length=50, verbose_name='公司职位')
    points = models.CharField(max_length=50, verbose_name='教学特点')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    image = models.ImageField(upload_to='teacher/%Y/%m', verbose_name='头像', null=True)
    age = models.IntegerField(default=18, verbose_name='年龄')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name

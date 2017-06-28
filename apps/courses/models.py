# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models

from organization.models import CourseOrg, Teacher


# Create your models here.

class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name='课程机构', null=True)
    name = models.CharField(max_length=50, verbose_name='课程名称')
    desc = models.CharField(max_length=300, verbose_name='课程简介')
    detail = models.TextField(verbose_name='课程详情')
    category = models.CharField(max_length=20, default='后端课程', verbose_name='课程类别')
    degree = models.CharField(max_length=10, choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), verbose_name='课程难度')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%M', verbose_name='封面图')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    tag = models.CharField(default='', max_length=100, verbose_name='标签')
    teacher = models.ForeignKey(Teacher, null=True, blank=True, verbose_name='讲师')
    need_know = models.CharField(max_length=50, default='', verbose_name='课程须知')
    can_learn = models.CharField(max_length=50, default='', verbose_name='可以学到什么')

    def __str__(self):
        return self.name

    def get_zj_count(self):
        """
        获取章节数
        :return:
        """
        return self.lesson_set.all().count()

    def get_learn_students(self):
        """
        获取学习用户
        :return:
        """
        return self.usercourse_set.all()

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='章节名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    url = models.CharField(max_length=200, default="http://www.baidu.com", verbose_name='链接地址')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name


class Video(models.Model):
    name = models.CharField(max_length=100, verbose_name='视频名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    lesson = models.ForeignKey(Lesson, verbose_name='章节')
    learn_times = models.IntegerField(default=0, verbose_name='时长')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name


class CourseResource(models.Model):
    name = models.CharField(max_length=50, verbose_name='资源名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    course = models.ForeignKey(Course, verbose_name='课程')
    download = models.FileField(upload_to='courses/resource/%Y/%M', max_length=100, verbose_name='下载地址')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

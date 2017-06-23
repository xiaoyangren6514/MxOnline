from django.shortcuts import render
from django.views.generic.base import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course

from operation.models import UserFavorite


# Create your views here.


class CouseListView(View):
    def get(self, request):
        current_page = 'course'
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = all_courses.order_by('-click_nums')[:3]
        # 根据最新 热门 学习人数进行排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 实例分页类对象
        p = Paginator(all_courses, 6, request=request)
        # 通过分页配置信息取到要显示的数据
        courses = p.page(page)
        return render(request, 'course-list.html', {
            'all_courses': courses,
            'current_page': current_page,
            'sort': sort,
            'hot_courses': hot_courses
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 点击数+1
        course.click_nums += 1
        course.save()
        # 根据课程取出对应机构
        course_org = course.course_org
        # 查看用户是否收藏当前课程机构
        has_fav = False
        if request.user.is_authenticated():
            result = UserFavorite.objects.filter(user=request.user,fav_type=2,fav_id=int(course_id))
            if result:
                has_fav = True
        return render(request, 'course-detail.html', {
            'course': course,
            'course_org':course_org,
            'has_fav':has_fav
        })

from django.shortcuts import render
from django.views.generic.base import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course


# Create your views here.


class CouseListView(View):
    def get(self, request):
        current_page = 'course'
        all_courses = Course.objects.all().order_by('-add_time')
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
            'sort': sort
        })

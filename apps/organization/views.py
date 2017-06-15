from django.shortcuts import render
from django.views.generic import View

from .models import CityDict, CourseOrg
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
class OrgView(View):
    def get(self, request):
        # 取出全部课程和城市
        all_cities = CityDict.objects.all()
        all_orgs = CourseOrg.objects.all()
        # 获取授课机构排名
        hot_orgs = all_orgs.order_by('-click_nums')[:3]
        # 根据城市进行排序
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
        # 根据机构类型进行排序
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 根据课程数或者学习人数进行排序
        sort = request.GET.get('sort','')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_count')

        orgs_count = all_orgs.count()
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 实例分页类对象
        p = Paginator(all_orgs, 3, request=request)
        # 通过分页配置信息取到要显示的数据
        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'all_cities': all_cities,
            'all_orgs': orgs,
            'orgs_count': orgs_count,
            'city_id': city_id,
            'ct':category,
            'hot_orgs':hot_orgs,
            'sort':sort
        })

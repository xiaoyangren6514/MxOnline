from django.shortcuts import render
from django.views.generic import View

from .models import CityDict, CourseOrg
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
class OrgView(View):
    def get(self, request):
        all_cities = CityDict.objects.all()
        all_orgs = CourseOrg.objects.all()
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
            'orgs_count': orgs_count
        })

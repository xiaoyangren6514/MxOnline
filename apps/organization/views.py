from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from .models import CityDict, CourseOrg
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .forms import UserAskForm


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
        sort = request.GET.get('sort', '')
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
            'ct': category,
            'hot_orgs': hot_orgs,
            'sort': sort
        })


class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask_form.save(commit=True)
            return HttpResponse("{'status':'success'}", content_type='application/json')
        else:
            return HttpResponse("{'status':'fail','msg':'添加出错'}", content_type='application/json')


class OrgDetailView(View):
    """
    机构详情首页
    """

    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_course = course_org.course_set.all()[:3]
        all_teacher = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_course': all_course,
            'all_teacher': all_teacher,
            'course_org': course_org,
            'current_page': current_page
        })


class OrgCourseView(View):
    """
    机构课程页面
    """

    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_course = course_org.course_set.all()[:3]
        return render(request, 'org-detail-course.html', {
            'all_course': all_course,
            'course_org': course_org,
            'current_page': current_page
        })


class OrgDescView(View):
    """
    机构介绍页面
    """

    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page
        })


class OrgTeacherView(View):
    """
    机构教师页面
    """

    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teacher = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'course_org': course_org,
            'current_page': current_page,
            'all_teacher': all_teacher
        })

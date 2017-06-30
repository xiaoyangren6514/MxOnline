from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from .models import CityDict, CourseOrg, Teacher
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .forms import UserAskForm
from operation.models import UserFavorite


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
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_course = course_org.course_set.all()[:3]
        all_teacher = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_course': all_course,
            'all_teacher': all_teacher,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrgCourseView(View):
    """
    机构课程页面
    """

    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_course = course_org.course_set.all()[:3]
        return render(request, 'org-detail-course.html', {
            'all_course': all_course,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrgDescView(View):
    """
    机构介绍页面
    """

    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrgTeacherView(View):
    """
    机构教师页面
    """

    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_teacher = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'course_org': course_org,
            'current_page': current_page,
            'all_teacher': all_teacher,
            'has_fav': has_fav
        })


class AddFavView(View):
    """
    用户收藏 取消收藏功能
    """

    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated():
            # 未登录
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 取消收藏操作
            exist_records.delete()
            return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')
        else:
            # 收藏操作
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav = UserFavorite()
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()
        # 获取排序方式
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_teachers = all_teachers.order_by('-click_nums')
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 实例分页类对象
        p = Paginator(all_teachers, 3, request=request)
        # 通过分页配置信息取到要显示的数据
        teachers = p.page(page)
        # 获取排行榜数据
        hot_teachers = all_teachers.order_by('-click_nums')[:3]
        return render(request, 'teachers-list.html', {
            'all_teachers': teachers,
            'hot_teachers': hot_teachers,
            'sort': sort
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        hot_teachers = Teacher.objects.all().order_by('-click_nums')[:3]
        has_fav_teacher = False
        if UserFavorite.objects.filter(user=request.user, fav_id=int(teacher_id), fav_type=3):
            has_fav_teacher = True
        has_fav_org = False
        if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
            has_fav_org = True
        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'hot_teachers': hot_teachers,
            'has_fav_org': has_fav_org,
            'has_fav_teacher': has_fav_teacher
        })

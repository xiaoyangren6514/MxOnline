from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.db.models import Q

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course

from operation.models import UserFavorite, CourseComment, UserCourse

from utils.mixin_utils import LoginRequiredMixin


# Create your views here.


class CouseListView(View):
    """
    课程列表页
    """

    def get(self, request):
        current_page = 'course'
        # 默认按照时间排序
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = all_courses.order_by('-click_nums')[:3]
        # 根据关键词进行搜索
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_courses = all_courses.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords))
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
    """
    课程详情页
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 点击数+1
        course.click_nums += 1
        course.save()
        # 根据课程取出对应机构
        course_org = course.course_org
        # 查看用户是否收藏当前课程机构
        has_fav_org = False
        if request.user.is_authenticated():
            result = UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=course_org.id)
            if result:
                has_fav_org = True
        # 查看用户是否收藏当前课程
        has_fav_course = False
        if request.user.is_authenticated():
            result = UserFavorite.objects.filter(user=request.user, fav_type=1, fav_id=int(course.id))
            if result:
                has_fav_course = True
        # 搜索相关课程
        tag = course.tag
        if tag:
            about_courses = Course.objects.filter(tag=tag)[:1]
        else:
            about_courses = []
        return render(request, 'course-detail.html', {
            'course': course,
            'course_org': course_org,
            'has_fav_org': has_fav_org,
            'about_courses': about_courses,
            'has_fav_course': has_fav_course
        })


class AddFavView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        if request.user.is_authenticated():
            # 检测数据格式
            if int(fav_id) > 0 and int(fav_type) > 0:
                # 检测是否已存在对应记录
                exist_records = UserFavorite.objects.filter(user=request.user, fav_type=int(fav_type),
                                                            fav_id=int(fav_id))
                if exist_records:
                    # 取消收藏
                    exist_records.delete()
                    return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')
                else:
                    # 收藏
                    user_fav = UserFavorite()
                    user_fav.user = request.user
                    user_fav.fav_id = int(fav_id)
                    user_fav.fav_type = int(fav_type)
                    user_fav.save()
                    return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"数据格式非法"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_lessons = course.lesson_set.all()
        all_resources = course.courseresource_set.all()
        teacher = course.teacher
        # 取出学习过这门课程的所有数据
        user_courses = UserCourse.objects.filter(course=course)
        # 得到学习过这门课程的所有uid
        user_ids = [user_course.user.id for user_course in user_courses]
        # 得到相关用户学习过的所有课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        # 记录用户学习过当前课程
        current_user_course_records = UserCourse.objects.filter(user_id=request.user.id, course_id=int(course.id))
        if not current_user_course_records:
            user_course_record = UserCourse()
            user_course_record.user = request.user
            user_course_record.course = course
            user_course_record.save()
        return render(request, 'course-video.html', {
            'course': course,
            'all_lessons': all_lessons,
            'all_resources': all_resources,
            'teacher': teacher,
            'all_user_courses': relate_courses
        })


class CourseCommentView(View):
    """
    课程评论信息
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_course_comments = course.coursecomment_set.all()
        teacher = course.teacher
        return render(request, 'course-comment.html', {
            'course': course,
            'all_course_comments': all_course_comments,
            'teacher': teacher
        })


class CourseAddCommentView(View):
    """
    添加评论
    """

    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        user_comment = CourseComment()
        user_comment.user = request.user
        user_comment.course = Course.objects.get(id=int(request.POST.get('course_id', 0)))
        user_comment.comments = request.POST.get('comments', '')
        user_comment.save()
        return HttpResponse('{"status":"success","msg":"提交成功"}', content_type='application/json')


class DemoView(View):
    def get(self, request):
        return HttpResponse('{"status":1,"msg":"用户尚未登录"}', content_type='application/json', charset='utf-8')

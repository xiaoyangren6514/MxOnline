from django.conf.urls import url, include

from courses.views import CouseListView, CourseDetailView, \
    DemoView, AddFavView, CourseVideoView, CourseCommentView,CourseAddCommentView

urlpatterns = [
    url(r'^list/$', CouseListView.as_view(), name='course_list'),
    url(r'^detail/(?P<course_id>\d+)$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^add_fav/$', AddFavView.as_view(), name='course_add_fav'),
    url(r'^course_video/(?P<course_id>\d+)$', CourseVideoView.as_view(), name='course_video'),
    url(r'^course_comment/(?P<course_id>\d+)$', CourseCommentView.as_view(), name='course_comment'),
    url(r'^add_comment/$', CourseAddCommentView.as_view(), name='course_add_comment'),
    url(r'^demo/$', DemoView.as_view(), name='course_demo'),
]

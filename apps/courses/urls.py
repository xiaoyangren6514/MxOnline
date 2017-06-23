from django.conf.urls import url, include

from courses.views import CouseListView, CourseDetailView, DemoView, AddFavView

urlpatterns = [
    url(r'^list/$', CouseListView.as_view(), name='course_list'),
    url(r'^detail/(?P<course_id>\d+)$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^add_fav/$', AddFavView.as_view(), name='course_add_fav'),
    url(r'^demo/$', DemoView.as_view(), name='course_demo'),
]

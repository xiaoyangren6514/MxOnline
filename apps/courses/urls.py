from django.conf.urls import url, include

from courses.views import CouseListView, CourseDetailView

urlpatterns = [
    url(r'^list/$', CouseListView.as_view(), name='course_list'),
    url(r'^detail/(?P<course_id>\d+)$', CourseDetailView.as_view(), name='course_detail'),
]

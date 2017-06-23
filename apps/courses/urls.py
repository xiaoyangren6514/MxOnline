from django.conf.urls import url, include

from courses.views import CouseListView

urlpatterns = [
    url(r'^list/$', CouseListView.as_view(), name='course_list'),
]

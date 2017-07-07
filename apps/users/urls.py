from django.conf.urls import url

from users.views import UserCenterView

urlpatterns = [
    url(r'^info/$', UserCenterView.as_view(), name='user_info'),
]

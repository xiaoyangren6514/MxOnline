"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
import xadmin
from django.views.static import serve

import users.views as uv
from users.views import LoginView, RegisterView, ActiveView, ForgetPwdView, ResetPwdView, ModifyPwdView

from MxOnline.settings import MEDIA_ROOT, STATIC_ROOT

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', uv.index, name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^forget_pwd/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^active/(?P<active_code>.*)/$', ActiveView.as_view(), name='user_active'),
    url(r'^reset/(?P<resetpwd_code>.*)/$', ResetPwdView.as_view(), name='reset_pwd'),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),
    url(r'^captcha/', include('captcha.urls')),
    # url(r'^login/$', uv.user_login, name='login'),
    # url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    # url(r'^login/$', TemplateView.as_view(template_name='login.html'), name='login'),
    # url(r'^register/$', TemplateView.as_view(template_name='register.html'), name='register'),

    # 课程机构模块
    url(r'^org/', include('organization.urls', namespace='org')),
    # 个人中心模块
    url(r'^user/', include('users.urls', namespace='user')),
    # 公开课
    url(r'^course/', include('courses.urls', namespace='course')),
    # url(r'^org_list/$', OrgView.as_view(), name='org_list'),
    # 配置上传文件的URL访问
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    # 生产环境手动配置静态页面文件地址
    url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),

]

# 全局404 500页面配置
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.server_error'

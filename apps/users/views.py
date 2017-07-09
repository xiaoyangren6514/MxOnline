from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect

from .models import UserProfile, EmailVerifyRecord
from django.db.models import Q
from django.contrib.auth.hashers import make_password

import json

from .forms import LoginForm, RegisterForm, ForgetPwdForm, ResetPwdForm, UploadImageForm
from utils.email_send import send_register_email


# Create your views here.

class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


def index(request):
    return render(request, 'index.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        print('username:' + username + ",password:" + password)
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {
                        'msg': '该用户尚未激活'
                    })
            else:
                return render(request, 'login.html', {
                    'msg': '用户名或密码错误'
                })
        else:
            return render(request, 'login.html', {
                'login_form': login_form,
            })


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):
                return render(request, 'register.html', {
                    'register_form': register_form,
                    'msg': '该用户名已存在'
                })
            password = request.POST.get('password', '')
            user = UserProfile()
            user.username = email
            user.email = email
            user.password = make_password(password=password)
            user.is_active = False
            user.save()
            send_register_email(email, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {
                'register_form': register_form,
                'msg': 'test'
            })


class ActiveView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.address
                user = UserProfile.objects.get(email=email)
                if user:
                    user.is_active = True
                    user.save()
        return render(request, 'login.html')


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {
            'forget_form': forget_form
        })

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            return render(request, 'send_vcode_success.html')
        return render(request, 'forgetpwd.html', {
            'forget_form': forget_form
        })


class ResetPwdView(View):
    def get(self, request, resetpwd_code):
        all_records = EmailVerifyRecord.objects.filter(code=resetpwd_code)
        if all_records:
            for record in all_records:
                email = record.address
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ModifyPwdView(View):
    def post(self, request):
        reset_form = ResetPwdForm(request.POST)
        email = request.POST.get('email', '')
        if reset_form.is_valid():
            pwd = request.POST.get('password', '')
            pwd1 = request.POST.get('password1', '')
            email = request.POST.get('email', '')
            if pwd == pwd1:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(pwd)
                user.save
                return render(request, 'login.html')
            else:
                return render(request, 'password_reset.html', {
                    'msg': '两次输入的密码不一致',
                    'email': email
                })
        return render(request, 'password_reset.html', {
            'reset_form': reset_form,
            'email': email
        })


class UserCenterView(View):
    def get(self, request):
        return render(request, 'usercenter-info.html', {
        })


class UserUploadImageView(View):
    def post(self, request):
        upload_image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if upload_image_form.is_valid():
            upload_image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UserModifyPwd(View):
    def post(self, request):
        pwd = request.POST.get('password', '')
        pwd1 = request.POST.get('password1', '')
        if pwd == pwd1:
            request.user.password = make_password(pwd)
            request.user.save()
            return HttpResponse('{"status":"success","msg":"修改密码成功"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(), content_type='application/json')


class UpdateEmailView(View):
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"status":"fail","msg":"邮箱已存在"}', content_type='application/json')
        if send_register_email(email, 'update_email'):
            return HttpResponse('{"status":"success","msg":"发送成功"}', content_type='application/json')


class UpdateEmailVerifyView(View):
    def get(self, request):
        verify_email_code = request.GET.get('code', '')
        email = request.GET.get('email', '')
        if EmailVerifyRecord.objects.filter(code=int(verify_email_code), email=email, type='update_email'):
            pass
        else:
            return HttpResponse('{"status":"fail","msg":"验证码错误"}', content_type='application/json')


class LogoutView(View):
    def get(self, request):
        login(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('index'))


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        print('username:' + username + ",password:" + password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'index.html')
        else:
            return render(request, 'login.html', {
                'msg': '用户名或密码错误'
            })

    elif request.method == 'GET':
        return render(request, 'login.html')

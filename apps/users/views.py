from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.views.generic import View

from .models import UserProfile, EmailVerifyRecord
from django.db.models import Q
from django.contrib.auth.hashers import make_password

from .forms import LoginForm, RegisterForm
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

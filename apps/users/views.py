from django.shortcuts import render
from django.contrib.auth import authenticate, login


# Create your views here.

def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        print('username:' + username + ",password:" + password)
        user = authenticate(username, password)
        if user is not None:
            login(request, user)
            return render(request, 'index.html')
        else:
            pass

    elif request.method == 'GET':
        return render(request, 'login.html')

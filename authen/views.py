from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
import datetime
import json


def keep_login(lk, r):
    if (lk == 'one_day'):
        r.session.set_expiry(60 * 60 * 24)
    elif (lk == 'one_week'):
        r.session.set_expiry(60 * 60 * 24 * 7)
    elif (lk == 'one_month'):
        r.session.set_expiry(60 * 60 * 24 * 30)
    else:
        r.session.set_expiry(None)


def home(request):
    if request.user.is_authenticated():
        if (request.user.is_superuser):
            return render(request, 'home.html', {
                'login_flag': 'true',
                'isadmin': 'true'
            })
        else:
            return render(request, 'home.html', {
                'login_flag': 'true',
                'isadmin': 'false'
            })
    else:
        return render(request, 'home.html', {
            'login_flag': 'false',
            'isadmin': 'false'
        })


def login_view(request):
    if not request.is_ajax():
        return HttpResponseNotFound()
    username = request.GET.get('username', '')
    password = request.GET.get('password', '')
    loginkeep = request.GET.get('loginkeep', '')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            keep_login(loginkeep, request)
            if (request.user.is_superuser):
                res = {'status': True,
                       'message': '登录成功',
                       'isadmin': True}
            else:
                res = {'status': True,
                       'message': '登录成功',
                       'isadmin': False}
            return JsonResponse(res)
        else:
            return JsonResponse({'status': False,
                                 'message': '当前用户状态不正常，请联系管理员！'})
    else:
        return JsonResponse({'status': False, 'message': '用户名或密码错误，请重新登录！'})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


def system_view(request):
    if request.user.is_authenticated():
        return render(request, 'system.html')
    else:
        return HttpResponseRedirect("/")


def edit_user_view(request):
    if not request.is_ajax():
        return HttpResponseNotFound()
    if not request.user.is_authenticated():
        return HttpResponseNotFound()
    else:
        type = request.GET.get('type', '')
        u = request.user
        if (type == 'editname'):
            newname = request.GET.get('name', '')
            if (len(newname) >= 30):
                return JsonResponse({'message': '请输入30个字符以内的名字！'})
            u.first_name = newname
            u.save()
            return JsonResponse({'message': '用户名已成功修改为 \"' + newname + '\" !'})
        elif (type == 'editpass'):
            oldpass = request.GET.get('o_pass', '')
            newpass = request.GET.get('n_pass', '')
            if u.check_password(oldpass):
                u.set_password(newpass)
                u.save()
                return JsonResponse({'message': '密码修改成功！'})
            else:
                return JsonResponse({'message': '密码修改失败！请检查自己的输入！'})

        else:
            return HttpResponseNotFound()


def control_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'control.html')
            # return HttpResponseRedirect("/admin/auth/user/")
        else:
            return HttpResponseNotFound()
    else:
        return HttpResponseNotFound()


def users_get_view(request):
    # if request.is_ajax():
    if request.user.is_authenticated:
        if request.user.is_superuser:
            type = request.GET.get('type', '')
            if (type == 'get_users'):
                users = []
                alluser = User.objects.exclude(is_superuser=True)
                for u in alluser:
                    last = u.last_login
                    if last is not None:
                        last = last.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        last = 'N/A'
                    join = u.date_joined
                    if join is not None:
                        join = join.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        join = 'N/A'
                    name = u.first_name
                    if name is None or (name == ""):
                        name = 'N/A'
                    obj = {
                        'user': u.username,
                        'name': name,
                        'join': join,
                        'last': last
                    }
                    # users.append(json.dumps(obj))
                    users.append(obj)
                return JsonResponse({'users': users})
            else:
                return HttpResponseNotFound()
        else:
            return HttpResponseNotFound()
    else:
        return HttpResponseNotFound()

# else:
#     return HttpResponseNotFound()

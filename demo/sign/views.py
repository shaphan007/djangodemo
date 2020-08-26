from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from sign.models import Event, Guest


# Create your views here.
def index(request):
    return render(request, "index.html")


def login_action(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)  # 登录
            request.session['user'] = username  # session 信息记录到浏览器
            response = HttpResponseRedirect('/event_manage/')
            return response
        else:
            return render(request, "index.html", {'error': 'username or password error !'})
        '''
        if username == "admin" and password == "admin":
            request.session['user'] = username  # session 信息记录到浏览器
            response = HttpResponseRedirect('/event_manage/')
            # response.set_cookie('user', username, 3600)  # 设置浏览器cookie
            return response
        else:
            return render(request, "index.html", {'error': 'username or password error !'})
        '''


@login_required
def logout(request):
    auth.logout(request)  # 退出登录
    response = HttpResponseRedirect('/index/')
    return response


# 发布会管理
@login_required
def event_manage(request):
    event_list = Event.objects.all()
    # username = request.COOKIES.get('user', '')  # 读取浏览器cookie
    username = request.session.get('user', '')  # 读取浏览器session
    return render(request, "event_manage.html", {"user": username, "events": event_list})


@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user": username, "events": event_list})


@login_required
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    return render(request, 'sign_index.html', {'event': event})


@login_required
def sign_index_action(request, eid):
    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get('phone', '')
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'phone error.'})
    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'event id or phone error.'})
    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'user have sign'})
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign='1')
        return render(request, 'sign_index.html', {'event': event, 'hint': 'sign in success', 'guest': result})


# 用户管理
@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 1)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)

    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request, "guest_manage.html", {"user": username, "guests": contacts})


@login_required
def search_phone(request):
    username = request.session.get('user', '')
    search_phone = request.GET.get("phone", "")
    guest_list = Guest.objects.filter(phone__contains=search_phone)
    return render(request, "guest_manage.html", {"user": username, "guests": guest_list})

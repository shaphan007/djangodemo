from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.contrib import auth as django_auth
import base64


# Create your views here.

# 用户登录
def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = django_auth.authenticate(username=username, password=password)
    if user is not None:
        django_auth.login(request, user)  # 登录
        return JsonResponse({"status": 100, "message": "login success"})
    else:
        return JsonResponse({"status": 200, "message": "login failure"})


def user_auth(request):
    get_http_auth = request.META.get('HTTP_AUTHORIZATION', b'')
    auth = get_http_auth.split()
    try:
        auth_parts = base64.b64decode(auth[1]).decode('utf-8').partition(":")
    except IndexError:
        return "null"

    username, password = auth_parts[0], auth_parts[2]
    user = django_auth.authenticate(username=username, password=password)
    if user is not None:
        django_auth.login(request, user)
        return "success"
    else:
        return "fail"


def add_event(request):
    auth_result = user_auth(request)
    if auth_result == "null":
        return JsonResponse({'status': 10011, 'message': 'user auth null'})
    if auth_result == 'fail':
        return JsonResponse({'status': 10012, 'message': 'user auth fail'})
    eid = request.POST.get('eid', '')
    name = request.POST.get('name', '')
    limit = request.POST.get('limit', '')
    status = request.POST.get('status', '')
    address = request.POST.get('address', '')
    start_time = request.POST.get('start_time', '')
    print(eid)

    if eid == '' or name == '' or limit == '' or address == '' or start_time == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    result = Event.objects.filter(id=eid)

    if result:
        return JsonResponse({'status': 10022, 'message': 'event id already exists'})

    result = Event.objects.filter(name=name)
    if result:
        return JsonResponse({'status': 10023, 'message': 'event name already exists'})

    if status == '':
        status = 1

    try:
        Event.objects.create(id=eid, name=name, limit=limit, address=address, status=int(status), start_time=start_time)
    except ValidationError as e:
        error = 'start_time format error. It must be in YYYY-MM-DD HH:MM:SS format.'
        return JsonResponse({'status': 10024, 'message': error})

    return JsonResponse({'status': 200, 'message': 'add event success'})

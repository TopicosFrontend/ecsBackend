from django.shortcuts import render, HttpResponse

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from django.db import IntegrityError

from django.contrib.auth.models import User
from support.models import SupportInfo
from collector.models import CollectorInfo
from user.models import Code

from ecsBackend.ecs_decorators import ecs_login_required, ecs_support_only
from ecsBackend.ecs_utils import collector_to_json, form_to_json, string_to_json

# salgado
def index(request):
    return HttpResponse("Hello from support backend")

# salgado
@csrf_exempt
def login(request):
    data = string_to_json(request.body.decode("utf-8"))
    #import pdb; pdb.set_trace()
    username = data["user"]
    password = data["password"]
    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({"state": False, "msg": "wrong user or password"})
    else:
        response = JsonResponse({"state": True, "msg": "login successful"})
        response["Access-Control-Allow-Origin"] = "*"
        auth_login(request, user)
        return response

# salgado
@csrf_exempt
@ecs_login_required
def logout(request):
    auth_logout(request)
    if request.user.is_authenticated:
        return JsonResponse({"state": False, "msg": "error logout failed"})
    return JsonResponse({"state": True, "msg": "logout successful"})

# salgado
@csrf_exempt
@ecs_login_required
@ecs_support_only
def register(request):
    data = request.POST
    username = data["user"]
    password = data["password"]

    try:
        user = User.objects.create_user(username=username, password=password)
        user.save()
        support = SupportInfo(username=user.get_username())
        support.save()
    except IntegrityError:
        return JsonResponse({"state": "false", "msg": "error creating support user"})

    return JsonResponse({"state": "true", "msg": "user created"})

# salgado
@csrf_exempt
@ecs_login_required
@ecs_support_only
def show_collector(request):
    data = request.GET
    username = data["user"]

    try:
        collector = CollectorInfo.objects.get(username=username)
    except CollectorInfo.DoesNotExist:
        return JsonResponse({"state": "false", "msg": "user is not a collector member"})

    response = collector_to_json(collector)
    return JsonResponse(response)

# salgado
@csrf_exempt
@ecs_login_required
@ecs_support_only
def show_collectors(request):
    response = {}
    response["collectors"] = [collector_to_json(collector) for collector in CollectorInfo.objects.all()]
    return JsonResponse(response)

# salgado
@csrf_exempt
@ecs_login_required
@ecs_support_only
def show_form(request):
    data = request.GET
    cfn = data["cfn"]
    ecn = data["ecn"]

    try:
        code = Code.objects.get(cfn=cfn, ecn=ecn)
        form = code.form
    except Code.DoesNotExist:
        return JsonResponse({"state": "false", "msg": "code not found"})

    response = form_to_json(form)
    return JsonResponse(response)

# salgado
@csrf_exempt
@ecs_login_required
@ecs_support_only
def census_status(request):
    response = {}

    codes = Code.objects.all()
    completed_codes = Code.objects.filter(in_use=False)

    response["total"] = codes.count()
    response["completed"] = completed_codes.count()

    return JsonResponse(response)

# unassigned
def transfer_forms(request):
    return HttpResponse("support transfer_forms")

# salgado
@csrf_exempt
@ecs_login_required
@ecs_support_only
def register_collectors(request):
    raw_data = request.FILES["file"].read().decode("utf-8")

    error_users = []
    for line in raw_data.splitlines():
        username, password, name, cellphone = line.split(",")
        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            collector = CollectorInfo(username=username, name=name, cellphone=cellphone)
            collector.save()
        except IntegrityError:
            error_users.append(username)

    if not error_users:
        return JsonResponse({"state": "true", "msg": "collectors created"})
    else:
        return JsonResponse({"state": "false", "msg": "some users were not created: [%s]" % ", ".join(error_users)})

# silva
def set_population(request):
    return HttpResponse("support set_population")

# salgado
def start_census_night(request):
    return HttpResponse("support start_census_night")

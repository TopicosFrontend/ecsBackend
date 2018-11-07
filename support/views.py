from django.shortcuts import render, HttpResponse

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from django.contrib.auth.models import User
from support.models import SupportInfo
from collector.models import CollectorInfo

from django.db import IntegrityError
from ecsBackend.ecs_decorators import ecs_login_required, ecs_support_only

# salgado
def index(request): 
    return HttpResponse("Hello from support backend")

# salgado
@csrf_exempt
def login(request):
    data = request.POST
    username = data["user"]
    password = data["password"]

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({"state": "false", "msg": "wrong user or password"})
    else:
        auth_login(request, user)
        return JsonResponse({"state": "true", "msg": "login successful"})

# salgado
@csrf_exempt
@ecs_support_only
@ecs_login_required
def logout(request):
    auth_logout(request)
    if request.user.is_authenticated:
        return JsonResponse({"state": "false", "msg": "error logout failed"})
    return JsonResponse({"state": "true", "msg": "logout successful"})

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
def show_collector(request):
    try:
        username = request.user.get_username()
        user_support = SupportInfo.objects.get(username=username)
    except SupportInfo.DoesNotExist:
        return JsonResponse({"state": "false", "msg": "user is not a support member"})

    try:
        data = request.POST
        collector = CollectorInfo.objects.get(username=data["user"])
    except CollectorInfo.DoesNotExist:
        return JsonResponse({"state": "false", "msg": "user is not a collector member"})

    response = {"codes": []}

    for code in collector.code_set.all():
        response["codes"].append({"cfn": code.cfn, "ecn": code.ecn})

    return JsonResponse(response)

# salgado
def show_collectors(request):
    return HttpResponse("support show_collectors")

# salgado
def show_form(request):
    return HttpResponse("support show_form")

# silva
def census_status(request):
    return HttpResponse("support census_status")

# unassigned
def transfer_forms(request):
    return HttpResponse("support transfer_forms")

# salgado                                                                        
@csrf_exempt                                                                     
def register_collectors(request):                                                
    try:
        username = request.user.get_username()
        user_support = SupportInfo.objects.get(username=username)
    except SupportInfo.DoesNotExist:
        return JsonResponse({"state": "false", "msg": "user is not a support member"})

    raw_data = request.FILES["file"].read().decode("utf-8")                      
                                                                                 
    for line in raw_data.split():                                                
        username, password = line.split(",")                                     
        user = User.objects.create_user(username=username, password=password)    
        user.save()                                                              
        collector = CollectorInfo(username=user.get_username())                                     
        collector.save()                                                         
    return JsonResponse({"state": "true", "msg": "collectors created"})

# silva
def set_population(request):
    return HttpResponse("support set_population")

# salgado
def start_census_night(request):
    return HttpResponse("support start_census_night")

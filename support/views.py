from django.shortcuts import render, HttpResponse

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from django.contrib.auth.models import User
from support.models import SupportInfo

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
def logout(request):
    auth_logout(request)
    return JsonResponse({"state": "true", "msg": "logout successful"})

# salgado
@csrf_exempt
def register(request):
    try:
        username = request.user.get_username()
        user_support = SupportInfo.objects.get(username=username)
    except SupportInfo.DoesNotExist:
        return JsonResponse({"state": "false", "msg": "user is not a support member"})

    data = request.POST
    username = data["user"]
    password = data["password"]

    user = User.objects.create_user(username=username, password=password)
    user.save()
    support = SupportInfo(username=user.get_username())
    support.save()

    return JsonResponse({"state": "false", "msg": "user created"})

# salgado
def show_collector(request):
    return HttpResponse("support show_collector")

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
def register_collectors(request):
    return HttpResponse("support register_collectors")

# silva
def set_population(request):
    return HttpResponse("support set_population")

# salgado
def start_census_night(request):
    return HttpResponse("support start_census_night")

from django.shortcuts import render, HttpResponse

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

# salgado
def index(request):
    return HttpResponse("Hello from user backend")

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

# cristian
def get_form(request):
    return HttpResponse("user get_form")

# salgado
def save_form(request):
    return HttpResponse("user save_form")

# salgado
def end_form(request):
    return HttpResponse("user end_form")

# cristian
def confirm_form(request):
    return HttpResponse("user confirm_form")

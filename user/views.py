from django.shortcuts import render, HttpResponse

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from user.models import Code
from user.user_utils import save_form_data

from ecsBackend.ecs_decorators import ecs_login_required
from ecsBackend.ecs_utils import read_json

# salgado
def index(request):
    return HttpResponse("Hello from user backend")

# salgado
@csrf_exempt
def login(request):
    data = request.POST
    username = data["cfn"]
    password = data["ecn"]

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({"state": "false", "msg": "wrong user or password"})
    else:
        auth_login(request, user)
        return JsonResponse({"state": "true", "msg": "login successful"})

# salgado
@csrf_exempt                                                                     
@ecs_login_required
def logout(request):                                                             
    auth_logout(request)                                                         
    if request.user.is_authenticated:
        return JsonResponse({"state": "false", "msg": "error logout failed"})
    return JsonResponse({"state": "true", "msg": "logout successful"})

# cristian
def get_form(request):
    return HttpResponse("user get_form")

# salgado
@csrf_exempt                                                                     
def save_form(request):
    form_json = read_json("example.json")

    codes = form_json["codigo"]

    try:
        code = Code.objects.get(cfn=codes["cfn"], ecn=codes["ecn"])
    except Code.DoesNotExist:
        return JsonResponse({"state": "false", "msg": "code not found"})

    response = save_form_data(code.form, form_json)
    return JsonResponse(response)

# salgado
def end_form(request):
    return JsonResponse({})

# cristian
def confirm_form(request):
    return HttpResponse("user confirm_form")

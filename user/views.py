from django.shortcuts import render, HttpResponse

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from user.models import Code
from user.user_utils import save_form_data

from ecsBackend.ecs_decorators import ecs_login_required
from ecsBackend.ecs_utils import read_json, string_to_json
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
    form_json = string_to_json(request.body.decode("utf-8"))
    #import pdb; pdb.set_trace()
    codes = form_json["codigo"]

    try:
        code = Code.objects.get(cfn=codes["cfn"], ecn=codes["ecn"])
    except Code.DoesNotExist:
        return JsonResponse({"state": "false", "msg": "form not found"})

    response = save_form_data(code.form, form_json)
    return JsonResponse(response)

# salgado
@csrf_exempt                                                                     
def end_form(request):
    data = string_to_json(request.body.decode("utf-8"))
    #import pdb; pdb.set_trace()
    cfn = data["cfn"]
    ecn = data["ecn"]

    try:
        code = Code.objects.get(cfn=cfn, ecn=ecn)
        code.in_use = False
        code.save()
    except Code.DoesNotExist:
        return JsonResponse({"state": "false", "msg": "form not found"})
    except Exception:
        return JsonResponse({"state": "false", "msg": "error while finalizing form"})

    return JsonResponse({"state": "true", "msg": "Form finalized"})

# cristian
def confirm_form(request):
    return HttpResponse("user confirm_form")

from django.shortcuts import render, HttpResponse

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from django.db import IntegrityError

from collector.models import CollectorInfo
from user.models import Code

from ecsBackend.ecs_decorators import ecs_login_required, ecs_collector_only
from ecsBackend.ecs_utils import code_to_json
from collector.collector_utils import generate_code
from user.user_utils import create_form

# salgado
def index(request):
    return HttpResponse("Hello from collector backend")

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
@ecs_login_required
def logout(request):
    auth_logout(request)
    if request.user.is_authenticated:
        return JsonResponse({"state": "false", "msg": "error logout failed"})
    return JsonResponse({"state": "true", "msg": "logout successful"})

# silva
@csrf_exempt
@ecs_collector_only
@ecs_login_required
def generate_codes(request):
    data = request.GET

    number = int(data["number"])
    username = request.user.get_username()

    collector = CollectorInfo.objects.get(username=username)

    codes = []
    for i in range(number):
        try:
            cfn, ecn = generate_code(collector)

            code = Code(cfn=cfn, ecn=ecn, collector=collector)
            code.save()

            create_form(code)
            codes.append(code)
        except IntegrityError:
            return JsonResponse({"state": "false", "msg": "error creating codes"})

    response = {}
    response["codes"] = [code_to_json(code) for code in codes]

    return JsonResponse(response)

# silva
def get_info(request):
    return HttpResponse("collector get_info")

# silva
def notification(request):
    return HttpResponse("collector notification")

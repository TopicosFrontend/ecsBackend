from django.shortcuts import render, HttpResponse

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from collector.models import CollectorInfo
from user.models import Code, Form, Section, Item

from ecsBackend.ecs_decorators import ecs_login_required, ecs_collector_only

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
@ecs_collector_only
@ecs_login_required
def logout(request):
    auth_logout(request)
    if request.user.is_authenticated:
        return JsonResponse({"state": "false", "msg": "error logout failed"})
    return JsonResponse({"state": "true", "msg": "logout successful"})

# silva
@csrf_exempt
def generate_codes(request):
    collector = CollectorInfo.objects.get(username="jaimito")

    code = Code(cfn="1234567890123", ecn="123456789012", collector=collector)
    code.save()

    form = Form(code=code)
    form.save()

    section = Section(title="section1", form=form)
    section.save()

    item = Item(question="question1", section=section)
    item.save()

    return HttpResponse("collector generate_codes")

# silva
def get_info(request):
    return HttpResponse("collector get_info")

# silva
def notification(request):
    return HttpResponse("collector notification")

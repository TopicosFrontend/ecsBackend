from django.shortcuts import HttpResponse
from django.http import JsonResponse

from django.db import IntegrityError

from user.models import Code
from collector.models import CollectorInfo

from django.views.decorators.csrf import csrf_exempt
from ecsBackend.ecs_decorators import ecs_login_required, ecs_collector_only

from ecsBackend.ecs_json_utils import code_to_json, collector_to_json, form_to_json
from ecsBackend.ecs_authenticate import ecs_login, ecs_logout
from collector.collector_utils import generate_code
from user.user_utils import create_form

# salgado
def index(request):
    return HttpResponse("Hello from collector backend")

# salgado
@csrf_exempt
def login(request):
    if ecs_login(request):
        return JsonResponse({"state": True, "msg": "login successful"}, safe=False)
    else:
        return JsonResponse({"state": False, "msg": "wrong user or password"}, safe=False)

# salgado
@csrf_exempt
@ecs_login_required
def logout(request):
    if ecs_logout(request):
        return JsonResponse({"state": True, "msg": "logout successful"}, safe=False)
    else:
        return JsonResponse({"state": False, "msg": "error logout failed"}, safe=False)

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
            return JsonResponse({"state": False, "msg": "error creating codes"}, safe=False)

    response = {}
    response["codes"] = [code_to_json(code) for code in codes]
    response["state"] = True
    response["msg"] = "codes generated"

    return JsonResponse(response, safe=False)

# silva
@csrf_exempt
def get_info(request):
    username = request.user.get_username()

    try:
        collector = CollectorInfo.objects.get(username=username)
        response = collector_to_json(collector)
        response["state"] = True
        response["msg"] = "collector founded"

        return JsonResponse(response, safe=False)
    except CollectorInfo.DoesNotExist:
        return JsonResponse({"state": False, "msg": "collector not founded"})

# silva
def notification(request):
    return JsonResponse("collector notification", safe=False)

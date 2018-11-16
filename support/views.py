from django.shortcuts import HttpResponse
from django.http import JsonResponse

from django.db import IntegrityError

from django.contrib.auth.models import User
from user.models import Code
from collector.models import CollectorInfo
from support.models import SupportInfo
from support.models import CensusNigth

from django.views.decorators.csrf import csrf_exempt
from ecsBackend.ecs_decorators import ecs_login_required, ecs_support_only
from ecsBackend.ecs_json_utils import collector_to_json, form_to_json, string_to_json, json_to_string
from ecsBackend.ecs_authenticate import ecs_login, ecs_logout

# salgado
def index(request):
    return HttpResponse("Hello from support backend")

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

# salgado
@csrf_exempt
@ecs_login_required
@ecs_support_only
def register(request):
    data = string_to_json(request.body.decode("utf-8"))

    username = data["user"]
    password = data["password"]

    try:
        user = User.objects.create_user(username=username, password=password)
        user.save()
        support = SupportInfo(username=user.get_username())
        support.save()
    except IntegrityError:
        return JsonResponse({"state": False, "msg": "error creating support user"}, safe=False)

    return JsonResponse({"state": True, "msg": "user created"}, safe=False)

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
        return JsonResponse({"state": False, "msg": "user is not a collector member"}, safe=False)

    response = collector_to_json(collector)
    response["state"] = True
    response["msg"] = "collector founded"
    return JsonResponse(response, safe=False)

# salgado
@csrf_exempt
@ecs_login_required
@ecs_support_only
def show_collectors(request):    
    response = {}
    response["collectors"] = [collector_to_json(collector) for collector in CollectorInfo.objects.all()]
    response["state"] = True
    response["msg"] = "collectors founded"
    return JsonResponse(response, safe=False)

#salgado
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
        return JsonResponse({"state": False, "msg": "code not found"}, safe=False)

    response = form_to_json(form)
    response["state"] = True
    response["msg"] = "form founded"
    return JsonResponse(response, safe=False)

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
    response["state"] = True
    response["msg"] = "status calculated"

    return JsonResponse(response, safe=False)

# salgado
@csrf_exempt
@ecs_login_required
@ecs_support_only
def transfer_forms(request):
    if ecs_login(request) == False:
        return JsonResponse({"state": False, "msg": "wrong user or password"}, safe=False)

    forms_json = {}
    forms_json["forms"] = [form_to_json(code.form) for code in Code.objects.filter(in_use=False)]

    json_str = json_to_string(forms_json)

    response = HttpResponse(json_str, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=database.json'

    return response

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
        return JsonResponse({"state": True, "msg": "collectors created"}, safe=False)
    else:
        return JsonResponse({"state": False, "msg": "some users were not created: [%s]" % ", ".join(error_users)}, safe=False)

@csrf_exempt
@ecs_login_required
@ecs_support_only
def start_census(request):
    registers = CensusNigth.objects.all()
    registerCensusNigth = None
    if(len(registers) == 0):
        registerCensusNigth = CensusNigth.objects.create()
        return JsonResponse({"state": True, "msg": "se ha iniciado el censo correctamente"}, safe=False)
    return JsonResponse({"state": True, "msg": "Ya se inicio el censo"}, safe=False)

# salgado
@csrf_exempt
@ecs_login_required
@ecs_support_only
def start_census_night(request):
    if ecs_login(request) == False:
        return JsonResponse({"state": False, "msg": "wrong user or password"}, safe=False)

    try:
        for code in Code.objects.all():
            code.in_use = True
            code.save()
    except Exception:
        return JsonResponse({"state": False, "msg": "error activating codes"}, safe=False)

    return JsonResponse({"state": True, "msg": "codes activated"}, safe=False)
